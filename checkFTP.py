#!/usr/bin/env python

import commands, re, sys, datetime, subprocess, shlex
from time import sleep
from subprocess import Popen, PIPE, STDOUT
from optparse import OptionParser

#options.LIST=False

# Add Script Options

usage = "usage: %prog [options] arg1 arg2"

parser = OptionParser(usage=usage)

parser.add_option("-l", "--listdir",
                                        action="store_true",
                                        dest="LIST",
                                        help="Use this if you just want to see if you can list a directory")
parser.add_option("-c", "--host",
                                        action="store",
                                                                                type="string",
                                        dest="HOST",
                                        help="Enter connect string (host/url) to connect to")
parser.add_option("-d", "--dir",
                                        action="store",
                                        type="string",
                                        dest="DIR",
                                        help="Directory to check in for file existance")
parser.add_option("-f", "--fileprefix",
                                        action="store",
                                        type="string",
                                        dest="FILENAME",
                                        help="Filename sans prefixed date")

parser.add_option("-s", "--start",
                                        action="store",
                                        type="string",
                                        dest="START",
                                        help="Start of timeframe the check should actually be run")

parser.add_option("-e", "--end",
                                        action="store",
                                        type="string",
                                        dest="END",
                                        help="End of timeframe the check should be run")

(options, args) = parser.parse_args()

USER=""
PASS=""
DATE=datetime.datetime.now().strftime("%Y%m%d")
MILDATE=datetime.datetime.now().strftime("%H%M")

def runlistingtest(USER, PASS, HOST, DIR):
        FTPCOMMANDS=[]
        FTPCOMMANDS.append("dir " + DIR)
        FTPCOMMANDS.append("bye")
        FTPCOMMANDS.append("EOF")
        CMD='time -p /usr/bin/lftp -u ' + USER + ',' + PASS + ' sftp://' + HOST + ' <<EOF\n' + str('\n'.join(FTPCOMMANDS))
        output = subprocess.Popen(shlex.split(CMD), stdin=PIPE, stdout=PIPE, stderr=subprocess.PIPE)
        for line in '\n'.join(FTPCOMMANDS):
                output.stdin.write(line)
        sleep(10)
        if output.poll() is None:
                output.kill()
                returnCode = 1
        else:
                results = output.communicate()[1]
                returnCode = output.poll()

        if returnCode == 0:
                runTime = re.search('real\s\d+.\d+', results)
                time = re.sub('real ','',runTime.group(0))
                print 'OK | time=' + time
        else:
                print 'FAILED'


def runfiletest(USER, PASS, HOST, DIR, DATE, FILENAME):
        FTPCOMMANDS=[]
        FTPCOMMANDS.append("cd " + DIR)
        FTPCOMMANDS.append("find " + DATE + FILENAME)
        FTPCOMMANDS.append("bye")
        FTPCOMMANDS.append("EOF")
        CMD='time -p /usr/bin/lftp -u ' + USER + ',' + PASS + ' sftp://' + HOST + ' <<EOF\n' + str('\n'.join(FTPCOMMANDS))
        output = subprocess.Popen(shlex.split(CMD), stdin=PIPE, stdout=PIPE, stderr=subprocess.PIPE)
        for line in '\n'.join(FTPCOMMANDS):
                output.stdin.write(line)
        sleep(10)
        if output.poll() is None:
                output.kill()
                returnCode = 1
        else:
                results = output.communicate()[1]
                returnCode = output.poll()

        if returnCode == 0:
                runTime = re.search('real\s\d+.\d+', results)
                time = re.sub('real ','',runTime.group(0))
                print 'OK | time=' + time
        else:
                print 'FAILED'

HOST=options.HOST
DIR=options.DIR

if options.LIST is True:
        runlistingtest(USER, PASS, HOST, DIR)
else:
        if options.START:
                if options.STOP:
                        pass
                else:
                        print "If STARTTIME is set you need to set STOPTIME (the -e command line argument)"
                        sys.exit()
                if MILDATE >= options.START and MILDATE <= options.END:
                        runfiletest(HOST, DIR, DATE, FILENAME)
                else:
                        print "OK"
                        sys.exit()
        else:
                runfiletest(HOST, DIR, DATE, FILENAME)
