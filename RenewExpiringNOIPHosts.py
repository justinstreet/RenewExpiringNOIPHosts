#!/usr/bin/python
# -*- coding: utf-8 -*-

""" RenewExpiringNOIPHosts.py

This code is placed in the public domain by the author.
Written by Justin Street (justinstreet@gmail.com).

The free version of NO-IP.com allows three dynamic hostnames per account but they
must be renewed every 30 days or will expire and be deleted. Only hosts expiring
in a week or less can be renewed.

This module will attempt to login to your account and renew the hostnames and then
log its success or failure to the syslog. It is recommended to run the module
every ten days via crontab. Be sure to check your syslog for success/failure.

CONFIGURATION:
    Set the USERNAME and PASSWORD variables (below) to your NO-IP login credentials.

DEPENDENCIES:
    The module uses Selenium and Firefox running in headless mode. If you don't
    have Selenium install it with "pip install -U selenium". To install Firefox's
    'geckodriver', download it from https://github.com/mozilla/geckodriver/releases
    and extract it to your /usr/local/bin folder.

"""

import syslog
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

USERNAME = "<your no-ip username>"
PASSWORD = "<password>"


class Connect:
    """ This class sets up Firefox and establishes the connection to NO-IP.com  """
    def __init__(self):
        """ Initialize Firefox instance """
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_options=opts)

        self.initiate()

    def initiate(self):
        """ Establish connection with NO-IP's website """
        self.driver.get('https://www.noip.com/login')

    def quit(self):
        """ Exit procedure """
        self.__del__()

    def __del__(self):
        """ Close Firefox instance """
        self.driver.quit()


def log(msg):
    """ Log to stdout and syslog """
    print(msg)
    syslog.syslog(msg)


def main():
    """ Main procedure that navigates NO-IP's website """
    noip.driver.find_element_by_name("username").send_keys(USERNAME)
    noip.driver.find_element_by_name("password").send_keys(PASSWORD)

    noip.driver.find_element_by_name("Login").click()
    assert "My No-IP" in noip.driver.title

    noip.driver.find_element_by_class_name("host-data-widget").click()
    hosts = noip.driver.find_elements_by_class_name("table-striped-row")

    for host in hosts:
        if len(host.find_elements_by_class_name("btn-manage")) > 0:
            log("Host: {} ({})".format(host.find_element_by_class_name("text-info").text,
                                       host.find_element_by_class_name("no-link-style").text))
        if len(host.find_elements_by_class_name("btn-confirm")) > 0:
            try:
                host.find_element_by_class_name("btn-confirm").click()
                log("Host: {} (RENEWED SUCCESSFULLY)".format(host.find_element_by_class_name("text-info").text))
            except Exception:
                log("Host: {} (RENEWAL FAILED)".format(host.find_element_by_class_name("text-info").text))


if __name__ == "__main__":
    log("--- Checking NO-IP For Expiring Hosts ---")
    noip = Connect()

    try:
        main()
    except AssertionError:
        log("Error: Unable to login to No-IP.com ...")
    except Exception as e:
        log("Error: {}".format(str(e)))
    finally:
        noip.quit()
