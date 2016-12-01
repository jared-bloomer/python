#!/usr/bin/python


import traceback, commands, re, getopt, sys


opts, args = getopt.getopt(sys.argv[1:],"p:s:D:b:w:h:")


for o, a in opts:
 if o == "-D":
  bindDN = a
 elif o == "-b":
  baseDN = a
 elif o == "-w":
  password = a
 elif o == "-h":
  server = a
 elif o == "-s":
  search = a
 elif o == "-p":
  port = a

# Check to make sure everything has been passed to us, if not exit

output = commands.getstatusoutput('time -p /usr/bin/ldapsearch -x -l 60 -w \'' + password + '\' -D \'' +  bindDN +  '\' -b \'' + baseDN + '\' -H \'ldaps://' + server + ':' +  port + '\' ' + search )

returnCode = output[0]

try:
        if returnCode == 0:
         runTime = re.search('real\s\d+.\d+', output[1])
         runTime = re.sub('real ','',runTime.group(0))
         entries = re.search('numEntries:\s\d+', output[1])
         entries = re.sub('numEntries: ','',entries.group(0))

         print "OK | time="+runTime + " result="+entries
        else:
         print "FAILED | msg="+output[1]
         sys.exit(2)
except Exception, err:
        traceback.print_exc()

sys.exit(returnCode)
