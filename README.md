pysite_monitor
==============

PySite Monitor is a python up time monitor and alert tool. Receive email and sms / text alerts when your website is down. 

# Usage

usage: pysite_monitor.py website_url email_from email_password

	Optional Arguments: 
	[-h] 
	[--email_send_to EMAIL_SEND_TO] 
	[--sms_verizon SMS_VERIZON] 
	[--sms_att SMS_ATT] 
	[--sms_tmobile SMS_TMOBILE] 
	[--sms_sprint SMS_SPRINT]  
	[--alert_on_success]

Example:

python pysite_monitor.py http://brianmwilcox.com example@gmail.com your_password –email_send_to=email_address_to_alert@brianmwilcox.com –sms_att=5555555555

Note: Without indicating any optional arguments you will not be alerted if your website is down. You must specify at least one phone number to text, or email address to send an email to. 

# How does it work?

Pysite Monitor will first request your web page and return the HTTP return code, or the type of connection error it gets when requesting your URL. Then if there is an issue (HTTP code other than 200) Pysite Monitor will log into your email account (currently gmail and yahoo are supported) and send an email alert to an address you specify or send you a sms / text alert when your website is down.

To use the SMS Alert feature you must specify your service provider, currently Sprint, T-Mobile, Verizon, and AT&T are supported.

# What license is this under?

Pysite Monitor is licensed under GNU GENERAL PUBLIC LICENSE (version 3), and by extension all the terms of the license apply. Please read the entire license carefully.

# How do I run this every day / hour / minute?

I recommend Crontab.

# Misc

To contact the author visit http://brianmwilcox.com
