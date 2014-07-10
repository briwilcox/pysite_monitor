#
#    Original Version of Software by Brian M Wilcox
#    Please visit http://brianmwilcox.com for documentation
#

#
#    pysite_monitor (site_monitor.py) is a python site up time monitor.
#    It is capable of alerting you through email and sms regarding the
#    status of your website.
#

#
#    Copyright 2014 Brian M Wilcox
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

import requests
import smtplib
import argparse
import sys


class SiteCheck:
    """
    Class pertaining to HTTP requests and URL status checks
    """
    def __init__(self, url):
        self.url = url
        self.errors = ''
        self.site_request = None
        self.sms_ready_url = self.email_friendly_url()

    def make_request(self):
        try:
            self.site_request = requests.get(self.url)
        except requests.exceptions.ConnectionError:
            #Connection Failed
            return 'Connection failed to site ' + self.sms_ready_url
        except requests.exceptions.HTTPError:
            #Invalid HTTP Response
            return 'Invalid HTTP response from URL ' + self.sms_ready_url
        except requests.exceptions.Timeout:
            #Connection Timed Out
            return 'Connection timed out for URL ' + self.sms_ready_url
        except requests.exceptions.TooManyRedirects:
            #Too many redirects
            return 'To many redirects when accessing URL ' + self.sms_ready_url
        except requests.exceptions.RequestException:
            #Misc Requests Error
            return 'Unknown requests lib error when accessing ' + self.sms_ready_url

    def check_status(self):
        if self.site_request.status_code is 200:
            return 'Success! Your site ' + self.sms_ready_url + ' is up.'
        else:
            return 'Failure - Your site ' + self.sms_ready_url + ' returned HTTP error code ' \
                   + self.site_request.status_code.__str__()

    def email_friendly_url(self):
        # For whatever reason certain characters do not get past the email gateways, this appears to solves that
        if '://' in self.url:  # Likely redundant, urllib3 (in requests) should throw if this is invalid
            split_url_string = self.url.split('://')
            return split_url_string[1]
        else:
            raise Exception('Invalid URL string entered')


class AlertsEmailAndSMS:
    """
    Class pertaining to sending alerts via email and Short Message Service
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.server = None

    def login_gmail(self):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(self.username, self.password)

    def login_yahoo(self):
        self.server = smtplib.SMTP("smtp.mail.yahoo.com", 465)
        self.server.starttls()
        self.server.login(self.username, self.password)

    def email_alert(self, destination_email, message):
        self.server.sendmail(self.username, destination_email, message)

    #
    # These appear to be current as of June 28th 2014, I have added a few popular united states SMS carrier
    # gateways. If you would like your gateway here please add it.
    #
    # I have not tested with the carriers I do not have, and the carriers may change these at any time
    # so your mileage may vary.
    #
    def sms_alert_to_tmobile(self, phone_number, message):
        self.server.sendmail(self.username, phone_number + '@tmomail.net', message)

    def sms_alert_to_sprint(self, phone_number, message):
        self.server.sendmail(self.username, phone_number + '@messaging.sprintpcs.com', message)

    def sms_alert_to_att(self, phone_number, message):
        self.server.sendmail(self.username, phone_number + '@txt.att.net', message)

    def sms_alert_to_verizon(self, phone_number, message):
        self.server.sendmail(self.username, phone_number + '@vtext.com', message)


#Parse the user's arguments, check if specified website is up, notify user if they provide way(s) to do so
def main():
    #Parser Logic
    parser = argparse.ArgumentParser()
    parser.add_argument("website_url",
                        help="Website to check")
    parser.add_argument("email_from",
                        help="Email address to log in to")
    parser.add_argument("email_password",
                        help="Email address password")
    parser.add_argument("--email_send_to",
                        help="Send an email to this email address")
    parser.add_argument("--sms_verizon",
                        help="Send a text to this Verizon number.")
    parser.add_argument("--sms_att",
                        help="Send a text to this AT&T number.")
    parser.add_argument("--sms_tmobile",
                        help="Send a text to this T-Mobile number.")
    parser.add_argument("--sms_sprint",
                        help="Send a text to this Sprint number.")
    parser.add_argument('--alert_on_success', action='store_true')

    #Parse Arguments
    args = parser.parse_args()

    #Get HTTP Status Code
    site_check = SiteCheck(args.website_url)
    site_check.make_request()
    status_message = site_check.check_status()

    #If unsuccessful or if the user always wants alerts proceed
    if 'Success!' not in status_message or args.alert_on_success:
        alerts = AlertsEmailAndSMS(args.email_from, args.email_password)

        #Attempt to log into user's gmail account
        if '@gmail.com' in args.email_from.lower():
            alerts.login_gmail()

        #Attempt to log into user's yahoo account
        elif '@yahoo.com' in args.email_from.lower():
            alerts.login_yahoo()

        #Only so much time for programming in one day
        else:
            print('Unsupported Email. Currently this application only supports gmail and yahoo.')
            sys.exit(-1)

        #If user provided an email to notify do so
        if args.email_send_to is not None:
            alerts.email_alert(args.email_send_to, status_message)

        #If user provided a verizon phone number to text do so
        if args.sms_verizon is not None:
            alerts.sms_alert_to_verizon(args.sms_verizon, status_message)

        #If user provided an at&t phone number to text do so
        if args.sms_att is not None:
            alerts.sms_alert_to_att(args.sms_att, status_message)

        #If user provided a t-mobile phone number to text do so
        if args.sms_tmobile is not None:
            alerts.sms_alert_to_tmobile(args.sms_tmobile, status_message)

        #If user provided a sprint phone number to text do so
        if args.sms_sprint is not None:
            print(args.sms_sprint, status_message)
    exit(0)

main()
