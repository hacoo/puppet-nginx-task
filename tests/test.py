#! /usr/bin/env python
# Henry Cooney <hacoo36@gmail.com> <Github: hacoo>
#
# test.py
#
# Basic functional test for automated nginx server deployment.
# Uses Selenium to verify that the server at 'ip' serves the
# Puppet tester web page.

import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


default_url = "http://198.199.110.205:8000" # change this to set default



class NewVisitorTest(unittest.TestCase):

    def test_correct_title(self):
        """ Test that the page loads and has the correct title. """
        self.browser.get(self.server_url)
        self.assertEqual(u'Basic webpage for PSE Exercise',
                         self.browser.title)

    def test_PSE_text_exists(self):
        """ Check that the webpage contains the h1 text, 'PSE Exercise'''"""
        self.browser.get(self.server_url)
        h1_text = self.browser.find_elements_by_tag_name('h1')
        PSE_text_found = False
        for elem in h1_text:
            if u'PSE Exercise' in elem.text:
                PSE_text_found = True
        self.assertEqual(PSE_text_found, True)
                
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.server_url = default_url # Might make this
        # settable via command line later
        
    
    def tearDown(self):
        self.browser.quit()


if __name__ == '__main__':
    unittest.main()