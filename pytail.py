#!/usr/bin/env python

"""
Script Name: pytail

Author: Jared Bloomer

Description:
        This script is designed to colorize the output of Zenoss Logs

"""
##########################################################################
"""
Import Libraries
"""
import os, sys, string, select, itertools, getopt


##########################################################################
"""
Define Classes and Functions
"""
class pytail_file:

        def __init__(self, path, num=10, showheaders=0):
                path = sys.argv[-1]
                self.file=open(path,'r')
                self.text=self.file.readlines()
                tlen=len(self.text)
                start=int(tlen)-int(num)
                self.appl=self.text[start:tlen]
                if showheaders:
                        self.printheader()
                s0=open(path).readlines()[-num:]
                s1=[ x for x in itertools.chain.from_iterable( x.split('\n') for x in s0 ) ]
                self.colorprint(s1)

        def printheader(self):
                print '<< '+self.file.name+' >>'

        def colorprint(self, lines):
                pattern=[]
                for x in lines:
                        if x.find('INFO') >= 0:
                                print '\033[0m'+str(x)
                        if x.find('ERROR') >= 0:
                                print '\033[0;31m'+str(x)
                        if x.find('WARN') >= 0:
                                print '\033[0;33m'+str(x)
                        if x.find('DEBUG') >= 0:
                                print '\033[0;96m'+str(x)

        def fileno(self):
                return self.file.fileno()

        def founddata(self, showheaders):
                s=self.file.read()
                if s != '':
                        s2=string.split(s,'\n')
                        if showheaders is '1':
                                self.printheader()
                        self.colorprint(s2)

##########################################################################
"""
Call Main Logic
"""
if __name__ == '__main__':
        slist=[]
        opt,args=getopt.getopt(sys.argv[1:],'qn:')

        showheaders=0
        num=10
        appl=0

        for x in opt:
                if x[0] == 'n':
                        num=x[1]
                if x[0] == 'q':
                        showheaders=1

        for x in args:
                s=pytail_file(x, num, showheaders)
                slist.append(s)

        while 1:
                wr,ww,we=select.select(slist,[],[])
                for x in wr:
                        x.founddata(showheaders)
