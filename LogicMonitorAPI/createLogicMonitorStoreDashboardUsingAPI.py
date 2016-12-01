#! python

''' Description:
				Takes a list of store numbers as input (text file) and makes a LogicMonitor Store Dashboard for each store number listed in the file. 
'''

__author__ = "Jared Bloomer"
__copyright__ = "Copyright 2016"
__credits__ = ["Jared Bloomer"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jared Bloomer"
__email__ = ""
__status__ = "Production"


''' 
	---------------------------------
	| Flow of events in this script |
	---------------------------------
	
	1. Parse arguments to get text file name
	2. Open text file for read only access
	3. read text file line by line to get store number
		a. Store store number from text file as variable
		b. Set other store variables needed for API call later
		c. Get Data JSON for API Call (LogicMonitor_API.getDashboardData method)
		d. make API Call (LogicMonitor_API.getRequest method)
		e. Parse and log API call results
	4. Move to next line of text file and repete step 3 until EOF. 
'''

## import libraries required by LogicMonitor API
import requests, json, hashlib, base64, time, hmac

## import script specific libraries
import sys, logging, argparse


class LogicMonitor_API(object):
	def __init__(self):
		self.accessID=''
		self.accessKey=''
		self.company=''
		self.apiBaseURL='https://'+ self.company + '.logicmonitor.com/santaba/rest'
		
	def getRequest(self, method, resource, data):
		apiURL=self.apiBaseURL+resource
		epoch = str(int(time.time() * 1000))
		requestVars = method + epoch + data + resource
		signature = base64.b64encode(hmac.new(self.accessKey,msg=requestVars,digestmod=hashlib.sha256).hexdigest())
		auth = 'LMv1 ' + self.accessID + ':' + signature + ':' + epoch
		headers = {'Content-Type':'application/json','Authorization':auth}
		response = requests.post(apiURL, data=data, headers=headers)
		
		return response.content
		
	def getDashboardData(self, groupId, name, description, sharable, groupName):
		owner=''
		if groupId is None:
			groupId="1"
		if name is None:
			print "Error DashBoard Name is Required!"
			sys.exit(1)
		if description is None:
			description="Automated Creation of Dashboard without Description defined"
		if sharable is None:
			sharable="False"
		if owner is None:
			owner=self.accessID
		if groupName is None:
			groupName="undefined"
			
		data='{"groupId":"' + str(groupId) + '","name":"' + str(name) + '","description":"' + str(description) + '","sharable":"' + str(sharable) + '","owner":"' + str(owner) + '","groupName":"' + str(groupName) + '"}'
		
		return data
	

def main():
	## Setup Log
	loggerFormat=logging.Formatter('%(asctime)s - %(message)s')
	log=logging.getLogger(__name__)
	log.setLevel(logging.DEBUG)
	#  create file handler which logs even debug messages
	fh = logging.FileHandler(__file__+'.log')
	fh.setLevel(logging.DEBUG)
	# create console handler with a higher log level
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)
	fh.setFormatter(loggerFormat)
	ch.setFormatter(loggerFormat)
	# add the handlers to the logger
	log.addHandler(fh)
	log.addHandler(ch)
	
	log.info('   _____              _         __     _____  __                __ ')
	log.info('  / ___/ _____ _____ (_)____   / /_   / ___/ / /_ ____ _ _____ / /_')
	log.info('  \__ \ / ___// ___// // __ \ / __/   \__ \ / __// __ `// ___// __/')
	log.info(' ___/ // /__ / /   / // /_/ // /_    ___/ // /_ / /_/ // /   / /_  ')
	log.info('/____/ \___//_/   /_// .___/ \__/   /____/ \__/ \__,_//_/    \__/  ')
	log.info('                    /_/                                            ')
	log.info(' ')
	
	## parse script arguments
	storeList=''
	parser = argparse.ArgumentParser(description='Parse text file to create Store Dashboards in LogicMonitor')
	parser.add_argument('-f', action='store', nargs=1,  required=True, dest='storeList',
                    help='Name of text file with list of store numbers.')
	args = parser.parse_args()
	
	## Open text file for parsing
	with open(str(args.storeList[0])) as sl:
		for line in sl:
			storeNum=line
			## Setup Variables needed for Data JSON call
			dbName="Store Dashboard - " + storeNum
			dbDecription="Dashboard for Store " + storeNum
			groupName="Store Dashboards"
			
			log.info('Generating API Data JSON for store number %s' % storeNum)
			try:
				data=LogicMonitor_API.getDashboardData(LogicMonitor_API(), 1, dbName, dbDecription, True, groupName)
				log.info('JSON is %s' % data)
			except:
				log.error("Unexpected error:", sys.exc_info()[0])
				raise
			
			log.info('Executing API call to create LogicMonitor Dashboard for store %s' % storeNum)
			try:
				LogicMonitor_API.getRequest(LogicMonitor_API(), 'POST', '/dashboard/dashboards', data)
				log.info('Dashboard for store %s created successfully' % storeNum)
			except:
				log.error("Unexpected error:", sys.exc_info()[0])
				raise

	## Close text file
	sl.close()

	log.info('   _____              _         __     ______            __')
	log.info('  / ___/ _____ _____ (_)____   / /_   / ____/____   ____/ /')
	log.info('  \__ \ / ___// ___// // __ \ / __/  / __/  / __ \ / __  / ')
	log.info(' ___/ // /__ / /   / // /_/ // /_   / /___ / / / // /_/ /  ')
	log.info('/____/ \___//_/   /_// .___/ \__/  /_____//_/ /_/ \__,_/   ')
	log.info('                    /_/                                    ')
	log.info(' ')
	
## Call main method to execute script
try:
	main()
	sys.exit(0)
except Exception, e:
	print(Exception)
	sys.exit(1)
