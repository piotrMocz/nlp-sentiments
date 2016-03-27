#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'dominikmajda'

from time import time
import atexit

from datetime import datetime

from royters import ReutersManager
from telegraph import TelegraphManager
from zarohedge import ZeroHedgeManager
from thestreet import TheStreetManager


DIR_DUMP = "./dump_zero2/"
DIR_LOG = "./log/"

######################
#      Variables     #
######################

LOG_NAME = DIR_LOG + "log" + str(datetime.now())
STOP_CONDITION = 400
i = 147;

# Crate all sites managerc

#telegraph = datetime(2016, 2, 14, 12, 44, 57, 557000)
zeroH = datetime(2016, 2, 13, 12, 44, 57, 557000)
#
#telegraphManager = TelegraphManager(date=telegraph)
#reutersManager = ReutersManager(date=routers)
# telegraphManager = TelegraphManager()
# reutersManager = ReutersManager()
zerohedgeManager = ZeroHedgeManager(date=zeroH)
#thestreetManager = TheStreetManager()

# Start logging
log = open(LOG_NAME, 'w')

######################
#       Methods      #
######################

def compare_dates(date1, date2):
    if date1.year==date2.year and date1.month==date2.month and date1.day==date2.day:
        return True
    else:
        return False

def log_url_failre(crawler):
    log.write("Failure at: " + crawler.url + "\n")

def time_log():
    print "\n" + str(i) + ' articles in ' + str(time()-start_time) + "\n\n"
    log.write("\n" + str(i) + ' articles in ' + str(time()-start_time) + "\n\n")

def close_all():
    log.write("Closing state:\n")

    # Dump crawlers state
   # log.write("Telegraph date: " + str(telegraphManager.date) + "\n")
    log.write("ZeroHedge date: " + str(zerohedgeManager.date) + "\n")
    #log.write("Routers date: " + str(roytersManager.date) + "\n")
   # log.write("TheStreet page: " + str(thestreetManager.page) + "\n")

    log.close()

def dump(manager, prefix):
    global i
    crawler = manager.get_next_link()
    if crawler.dump(DIR_DUMP + str(i) + prefix, verbose=True, add_links=True):
        # Increase stop condition
        i+=1

        #print "error"
        #log_url_failre(crawler)


######################
# It all starts here #
######################

# Make time start - for testing purpose
start_time = time()
crawlers_date = datetime.now()

# Create log file and exit hook
atexit.register(close_all)
log = open(LOG_NAME, 'w')

# Start here
while (i<STOP_CONDITION):
    #dump(telegraphManager, "_telegraph")
    #dump(reutersManager, "_routers")
    dump(zerohedgeManager, "_zero")
    # downloaded_files(thestreetManager, "_thestreet")

    # Testing time
    if i%10==0:
        time_log()


