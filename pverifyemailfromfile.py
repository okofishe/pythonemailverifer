#This program verifies email addressess from a given file. verify email is saved as givenemailfile_filter.txt
# Validate -api test domain mx before making contact to the apilayer ,so no need to restest mx again

import multiprocessing
#from tld import get_tld
from multiprocessing import Pool
#from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process, Lock
import tqdm
from onascoEmailValidation import *
#import onascoEmailValidation
import os.path
import argparse
import itertools
from datetime import datetime, timedelta

lock = Lock()
##########################################################################################################
def func_star(a_b):
    checkEmail_API(*a_b)


def checkEmail_API(content,filename_filter):

    data = onascoEmailValidation('ff2169f1370463b4bdfcb50f3e1d140d')
    email = content.strip()

    validemail = data.validateEmailAPI(email,)
    try:
        if (validemail['smtp_check'] == True):
            lock.acquire()
            with open(filename_filter, 'a') as f:  # write filter email to file
                f.write(str(email))
                f.write("\n")
            lock.release()
    except:
        pass


def validatewith_API(filename):  # this routine use mailboxlayer API

    filename_filter = filename.split(".")[0]
    filename_filter = filename_filter + "_filter.txt"
    with open(filename) as f:
        content = f.read().splitlines()
    # count the total number of email in file
    with open(filename) as f:
        num_lines = sum(1 for _ in f)
    print 'Input file: ', filename
    print 'Number of Emails: ', num_lines
    content = set(content)  # remove duplicate emails
    list(content)
    print"[*] Validating email with maillayer API checking whether email exist"
    # check if filter_name exist,if it exist delete file name
    if os.path.exists(filename_filter):
        os.remove(filename_filter)

    tasks = range(len(content))

    pool = Pool(20)
    for _ in tqdm.tqdm(pool.imap_unordered(func_star,itertools.izip(content, itertools.repeat(filename_filter))), total=len(tasks)):
            pass

    print"[*] Writing valid emails to file"




            # count number of filter email
    try:
        with open(filename_filter) as f:
            num_lines_filter = sum(1 for _ in f)
        print 'Output file name for filter emails : ', filename_filter
        print 'Number of Emails Saved: ', num_lines_filter
        print'Total emails filtered(remove) is: ', num_lines - num_lines_filter
        print 'Done'
    except:
        print "[*] No Email Validated"


############################################################################################################


def validatewith_myAPI(filename):  # this routine use your local computer as smtp server.

    filename_filter = filename.split(".")[0]
    filename_filter = filename_filter + "_filter.txt"
    with open(filename) as f:
        content = f.read().splitlines()
    # count the total number of email in file
    with open(filename) as f:
        num_lines = sum(1 for _ in f)
    print 'Input file: ', filename
    print 'Number of Emails: ', num_lines
    content = set(content)  # remove duplicate emails
    list(content)
    print"[*] Validating email with maillayer API checking whether email exist"
    # check if filter_name exist,if it exist delete file name
    if os.path.exists(filename_filter):
        os.remove(filename_filter)

    tasks = range(len(content))

    pool = Pool(20)
    for _ in tqdm.tqdm(pool.imap_unordered(func_star,itertools.izip(content, itertools.repeat(filename_filter))), total=len(tasks)):
            pass

    print"[*] Writing valid emails to file"




            # count number of filter email
    try:
        with open(filename_filter) as f:
            num_lines_filter = sum(1 for _ in f)
        print 'Output file name for filter emails : ', filename_filter
        print 'Number of Emails Saved: ', num_lines_filter
        print'Total emails filtered(remove) is: ', num_lines - num_lines_filter
        print 'Done'
    except:
        print "[*] No Email Validated"


############################################################################################################


def func_star_mx(a_b):
    checkEmail_MX(*a_b)

def checkEmail_MX(content,filename_filter):
    lock.acquire()
    data = onascoEmailValidation('588b5596b510a0c75756ef1591bc2688')    #access key
    email = content.strip()
    validemail = data.validateEmailMX(email)
    try:
        if (validemail['mx'] == True):
               #lock.acquire()
                with open(filename_filter, 'a') as f:  # write filter email to file
                    f.write(str(email))
                    f.write("\n")
                #lock.release()
    except:
        pass
    lock.release()
def validatewith_MX(filename):

    filename_filter = filename.split(".")[0]
    filename_filter = filename_filter + "_filter.txt"
    with open(filename) as f:
        content = f.read().splitlines()
    # count the total number of email in file
    with open(filename) as f:
        num_lines = sum(1 for _ in f)
    print 'Input file: ', filename
    print 'Number of Emails: ', num_lines
    content = set(content)  # remove duplicate emails
    list(content)

    print"[*] Validating email with DNS checking if email domain exist"

    if os.path.exists(filename_filter):
        os.remove(filename_filter)

    tasks = range(len(content))

    pool = Pool(20)
    for _ in tqdm.tqdm(pool.imap_unordered(func_star_mx,itertools.izip(content, itertools.repeat(filename_filter))), total=len(tasks)):
            pass

    print"[*] Writing valid emails to file"


            # count number of filter email
    try:
        with open(filename_filter) as f:
            num_lines_filter = sum(1 for _ in f)
        print 'Output file name for filter emails : ', filename_filter
        print 'Number of Emails Saved: ', num_lines_filter
        print'Total emails filtered(remove) is: ', num_lines - num_lines_filter
        print 'Done'
    except:
        print "[*] No Email Validated"



if __name__ == '__main__':
    multiprocessing.freeze_support()
    print "#### Multi Threaded Email verifier written independently by olumide onafowope for educational purposes only ####"
    print ''
    date_future = "5/31/2019"
    #pdate_future = datetime.strptime(date_future, "%d/%m/%Y")
    pdate_future = datetime.strptime(date_future, "%m/%d/%Y")
    present = datetime.now()
    #if present < pdate_future:
    try:
                parser = argparse.ArgumentParser(description='Validate emails using MX(if domain exist) or API(if email address exist)')
                parser.add_argument("targets",help="textfile list of email to validate in txt format")
                parser.add_argument("-api",help="validate with maillayer API returning email with that are still valid",action="store_true")
                parser.add_argument("-mx", help="validate with DNS returning email with valid domains",action="store_true")
                args = parser.parse_args()
                if args.api:
                    validatewith_API(args.targets)
                if args.mx:
                    validatewith_MX(args.targets)
    except KeyboardInterrupt:
                exit()
    #else:
    #    exit()





