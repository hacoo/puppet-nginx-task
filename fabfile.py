
# Henry Cooney <hacoo36@gmail.com> <Github: hacoo>
#
# Fabfile for automated nginx server deployment. Will
# deploy the Puppet Lab's Exercise page and serve it from
# port 8000.

# Usage:

# If nginx is already installed on the server, run:
#
# > fab deploy:host=<user@host-server-url>
#
# If you want to install nginx on a new server, run:
#
# > fab newserver-deploy:host=<user@host-server-url>
#

from fabric.contrib.files import append, exists, sed, is_link
from fabric.api import env, local, run, sudo, put
from fabric.context_managers import settings
import sys

REPO_URL = 'https://github.com/puppetlabs/exercise-webpage.git'

# Automaticall assign site name to be the name of git repo:
for word in REPO_URL.split('/'):
    if '.git' in word:
        SITENAME = word.split('.')[0] 


def deploy():
    """ Standard deployment. Will configure nginx and fetch from repo.
    If nginx is not yet installed, will return and prompt user to do a
    first-time setup. """
    
    try:
        check_for_sudo()
        install_dependencies()
        check_dependencies()
        setup_dirs()
        pull_from_repo()
        configure_nginx()
        restart_nginx()

    except PackageNotInstalledException as e:
        print("Error -- The following package was not installed: " + e.args[0])
        print("Maybe you don't have sudo priviledges on this system?")

def check_for_sudo():
    """ Verifies the user can sudo, if not, prints and error and exits. """
    with(settings(warn_only=True)):
        result = sudo('cd ~')

    if result.succeeded == False:
        print("Error: You must have sudo priviledged to deploy the server. ")
        print("Please use an account with sudo priviledges. ")
        sys.exit(1)

def install_dependencies():
    """ Sets up a new server. Installs nginx, configures,
    and deploys. """
    with (settings(warn_only=True)): 
        if(package_installed('nginx') == False):
            print("Installing nginx: ")
            apt_get('nginx')
        if(package_installed('git') == False):
            print("Installing git: ")
            apt_get('git')

    

def setup_dirs():
    """ Sets up the content directory if it doesn't exist. """
    if(exists('/usr/share/web') == False):
        sudo('mkdir /usr/share/web')
    
    
    
def pull_from_repo():
    """ Pull latest version from the repo. If its there, fetch it;
    if not clone it. """
    if(package_installed('git') == False):
        raise PackageNotInstalledException("git is not installed.")

    source_folder = '/usr/share/web/' + SITENAME
    if(exists(source_folder) == False):
        print("Base directory for " + SITENAME + " not found. Cloning: ")
        sudo('git clone %s %s' % (REPO_URL, source_folder))
    else:
        print("Pulling from repo: ")
        sudo('cd %s && git pull' % (source_folder))


    
def configure_nginx():
    """ Configures nginx to serve the exercise webpage on
    port 8000. """

    available_path = '/etc/nginx/sites-available/' + SITENAME
    enabled_path = '/etc/nginx/sites-enabled/' + SITENAME

    if(package_installed('nginx') == False):
        raise PackageNotInstalledException("nginx is not installed.")

    print("Configuring nginx")
    if(exists(available_path) == False):
        put('nginx.template.conf', '~/nginx.template.conf')
        sudo('mv ~/nginx.template.conf ' + available_path)

    sed(available_path, 'SITENAME', SITENAME, use_sudo=True)
    
    if(is_link(enabled_path, use_sudo=True, verbose=True)):
        sudo('rm ' + enabled_path)
    sudo('ln -s ' + available_path + ' ' + enabled_path)

   
        
    
    
def check_dependencies():
    """ Raises an exception if git or nginx is missing. """
    if(package_installed('git') == False):
        raise PackageNotInstalledException("git")
    if(package_installed('nginx') == False):
        raise PackageNotInstalledException("nginx")


def restart_nginx():
    sudo('service nginx restart')
        
        
# helper functions

def package_installed(pkg_name):
    """ref: http:superuser.com/questions/427318/#comment490784_427339"""
    cmd_f = 'dpkg-query -l "%s" | grep -q ^.i'
    cmd = cmd_f % (pkg_name)
    with settings(warn_only=True):
        result = run(cmd)
    return result.succeeded


def apt_get(*packages):
    """ Installs packages via Apt, answers YES to ALL questions.
    Will not upgrade the package.
    ref: http://blog.muhuk.com/2010/05/22/how-to-install-mysql-with-fabric.html#.Vd9-95NVLVM """
    sudo('apt-get -y --no-upgrade install %s' % ' '.join(packages), shell=False)

class PackageNotInstalledException(Exception):
    pass