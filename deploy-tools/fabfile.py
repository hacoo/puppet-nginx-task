
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

REPO_URL = 'https://github.com/puppetlabs/exercise-webpage.git'

# Automaticall assign site name to be the name of git repo:
for word in REPO_URL.split('/'):
    if '.git' in word:
        SITENAME = word.split('.')[0] 


def deploy():
    """ Standard deployment. Will configure nginx and fetch from repo.
    If nginx is not yet installed, will return and prompt user to do a
    first-time setup. """

    if (package_installed('nginx') == False):
        print("Error: ")
        print(" Nginx does not appear to be installed.")
        print(" Please run first time setup with the command: ")
        print(" > fab newserver-deploy:host=<user@host-server-url>")
        return

    try:
        check_dependencies()
        setup_dirs()
        pull_from_repo()
        configure_nginx()
        
    except PackageNotInstalledException as e:
        print("Error: " + e.args[0])
        print(" A required package does not appear to be installed.")
        print(" Please run first time setup with the command: ")
        print(" > fab newserver-deploy:host=<user@host-server-url>")
        return



def newserver_deploy():
    """ Sets up a new server. Installs nginx, configures,
    and deploys. """

    if(package_installed('nginx') == False):
        print("Installing nginx: ")
        apt_get('nginx')
    if(package_installed('git') == False):
        print("Installing git: ")

    deploy()
    

def setup_dirs():
    """ Sets up the content directory if it doesn't exist. """
    if(exists('~/content/') == False):
        run('mkdir ~/content')
    
    
    
def pull_from_repo():
    """ Pull latest version from the repo. If its there, fetch it;
    if not clone it. """
    if(package_installed('git') == False):
        raise PackageNotInstalledException("git is not installed.")

    source_folder = '~/content/' + SITENAME
    if(exists('~/content/' + SITENAME) == False):
        print("Base directory for " + SITENAME + " not found. Cloning: ")
        run('git clone %s %s' % (REPO_URL, source_folder))
    else:
        print("Fetching from repo: ")
        run('cd %s && git fetch' % (source_folder))


    
def configure_nginx():
    """ Configures nginx to serve the exercise webpage on
    port 8000. """

    available_path = '/etc/nginx/sites-available/' + SITENAME
    enabled_path = '/etc/nginx/sites-enabled/' + SITENAME

    if(package_installed('nginx') == False):
        raise PackageNotInstalledException("nginx is not installed.")

    print("Configuring nginx")
    put('nginx.template.conf', '~/nginx.template.conf')
    sudo('mv ~/nginx.template.conf ' + available_path)

    sed(available_path, 'USERNAME', env.user, use_sudo=True)
    sed(available_path, 'SITENAME', SITENAME, use_sudo=True)
    
    if(is_link(enabled_path, use_sudo=True, verbose=True)):
        sudo('rm ' + enabled_path)

    sudo('ln -s ' + available_path + ' ' + enabled_path)
    sudo('service nginx restart')
   
        
    
    
def check_dependencies():
    """ Raises an exception if git or nginx is missing. """
    if(package_installed('git') == False):
        raise PackageNotInstalledException("git is not installed.")
    if(package_installed('nginx') == False):
        raise PackageNotInstalledException("nginx is not installed.")
        
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