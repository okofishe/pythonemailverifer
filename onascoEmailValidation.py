
# Validate -api test domain mx before making contact to the apilayer ,so no need to restest mx again
import requests
import json
import DNS
#from validate_email import validate_email
#from tld import get_tld


import smtplib
#from email.utils import parseaddr
import re
import socket




class onascoEmailValidation:
    def __init__(self, accesskey):

        self.accesskey = accesskey

    def isValidEmail(self,email):
        response = {"filter_email": False}
        addressToVerify = email.lower()
        # Simple Regex for syntax checking
        regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
        # Email address to verify
        # Syntax check
        match = re.match(regex, addressToVerify)
        if match == None:
            # print('Bad Syntax')
            # raise ValueError('Bad Syntax')
            return response
        # filter out unwanted domains
        if any(s in addressToVerify for s in ('editor','editorial','security','ebay','amazon','jobs','donotreply','press','abuse@','admin@','billing@','compliance@','devnull@','dns@','ftp@','hostmaster@','inoc@','ispfeedback@','ispsupport@','list-request@','list@','maildaemon@','noc@',\
        									   'no-reply@','noreply@','null@','phish@','phishing@','postmaster@','privacy@','registrar@','root@','security@','spam@','support@','sysadmin@','tech@','undisclosed-recipients@',\
        									   'unsubscribe@','usenet@','uucp@','webmaster@','www@','feedback','.edu','admin','support','postmaster','.gov','org','@gov','@fbi','webmaster','ebay','newegg','vwr','overstock',\
                                              'staples','bhphotovideo','frys','neweggbusiness','thestoke.ca','macrumors.com',\
                                              'pcmag.com','gearbest.com','domain','microsoft','ucalgary.ca','paypal','support','officedepot','help',\
                                              "gmail","yahoo","hotmail","aol","outlook","test","example","accessibility","advertise","ads","add","agent","affilate","advertising","agents","bounces","books","content","licensing","copyright","careers","affilates","auditions","ask","auctions","blog","channel","dmca","deliverystatus","hello","mail","legal","leads","lead","notices","order","orders","news","new","return","reservation","research","training","ticket")):
            return response
        #remove any domain that does not have .com

        response={"filter_email":True}
        return response

    def validateEmailMyAPI(self, email):
        response = {"smtp_check": False}
        valid_email=self.isValidEmail(email)
        if (valid_email['filter_email'] == True):
            addressToVerify=email

            try:
                is_valid = self.olusco(addressToVerify)
            except:
                return response
            if is_valid:
                response = {"smtp_check": True}
                return response
            else:
                return response
        else:
            return response

    def olusco(self,email):
        pemail=email
        # Get local server hostname
        host = socket.gethostname()
        #get mx record
        try:
            domainToVerify = pemail.split("@")[1]  # verify if domain has mx record, i.e if it exist
            # remove any domain that does not have .com
            name, ext = domainToVerify.split('.')[-2:]
            if (ext != "com" and ext != "us"):
                return False
        except:
            print pemail
            print "index out of range"
            return False
        try:
            DNS.DiscoverNameServers()
            records = DNS.mxlookup(domainToVerify)
            mxRecord = records[0][1]
            mxRecord = str(mxRecord)
        except:
            return False
        # SMTP lib setup (use debug level for full output)
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        # SMTP Conversation
        server.connect(mxRecord)
        server.helo(host)
        server.mail(pemail)
        code, message = server.rcpt(str(pemail))
        server.quit()
        # Assume 250 as Success
        if code == 250:
            return True
        else:
            return False


    def validateEmailAPI(self, email):
        response = {
            "email": "support@apilayer.com",
            "did_you_mean": "",
            "user": "support",
            "domain": "apilayer.net",
            "format_valid": True,
            "smtp_check": False,
            "role": True,
            "disposable": False,
            "free": False,
            "score": 0.8
        }
        #response = {"smtp_check": False}
        valid_email=self.isValidEmail(email)
        if (valid_email['filter_email'] == True):
            addressToVerify = email
            try:
                domainToVerify = addressToVerify.split("@")[1]  # verify if domain has mx record, i.e if it exist


            except:
                #print addressToVerify
                #print "index out of range"
                return response
            try:
                # remove any domain that does not have .com
                #name, ext = domainToVerify.split('.')[-2:]
                #if (ext != "com" and ext != "us"):
                #    return response

                DNS.DiscoverNameServers()
                records = DNS.mxlookup(domainToVerify)
                mxRecord = records[0][1]
                mxRecord = str(mxRecord)
                if mxRecord:
                    response['mx'] = True
                    # print "found mx record"
                    # return response
                    try:

                        access_key = self.accesskey
                        email = addressToVerify
                        params = {'email': email, 'access_key': access_key}
                        response = requests.get('http://apilayer.net/api/check', params=params);
                        # response = requests.get('http://emailpie.com/v1/check', params=params)
                        response = json.loads(response.content)
                        return response
                    except:
                        return response
            except Exception as e:
                #print(e.message)
                return response

            else:
                return response
        else:
            return response



    def validateEmailMX(self, email):
        response = {"mx": False}
        valid_email=self.isValidEmail(email)
        if (valid_email['filter_email'] == True):
            addressToVerify = email
            try:
                domainToVerify = addressToVerify.split("@")[1]  # verify if domain has mx record, i.e if it exist


            except:
                #print addressToVerify
                #print "index out of range"
                return response
            try:
                # remove any domain that does not have .com
                name, ext = domainToVerify.split('.')[-2:]
                if (ext != "com" and ext !="us"):
                    return response

                DNS.DiscoverNameServers()
                records = DNS.mxlookup(domainToVerify)
                mxRecord = records[0][1]
                mxRecord = str(mxRecord)
                if mxRecord:
                    response['mx'] = True
                    #print "found mx record"
                    return response
            except Exception as e:
                #print(e.message)
                return response

        else:
            return response


