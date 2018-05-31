# RenewExpiringNOIPHosts
A python script for Linux users that renews expiring NO-IP.com hosts

<------------------------------------------------------------------>

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
