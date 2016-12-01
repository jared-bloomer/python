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
import request, json, hashlib, base64, time, hmac

## import script specific libraries
import sys, logger, argparse


class LogicMonitor_API(object):
	def __init__(self):
		self.accessID=''
		self.accessKey=''
		self.company=''
		self.apiBaseURL='https://'+ company + '.logicmonitor.com/santaba/rest'

	def getRequest(self, method, resource, data):
		apiURL=self.apiBaseURL+resource
		epoch = str(int(time.time() * 1000))
		requestVars = method + epoch + data + resource
		signature = base64.b64encode(hmac.new(self.accessKey,msg=requestVars,digestmod=hashlib.sha256).hexdigest())
		auth = 'LMv1 ' + self.accessId + ':' + signature + ':' + epoch
		headers = {'Content-Type':'application/json','Authorization':auth}
		response = requests.post(apiURL, data=data, headers=headers)

		return response

	def getDashboardData(self, groupId, name, description, sharable, owner, groupName):
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
			owner=accessID
		if groupName is None:
			groupName="undefined"

		data='{"groupId":"' + groupId + '","name":"' + name + '","description":"' + description + '","sharable":"' + sharable + '","owner":"' + owner + '","groupName":"' + groupName +"}'

		return data


def main():
	## Setup Log
	loggerFormat= '%(asctime)s | %(clientip)s | %(user)s - %(message)s'
	logging.basicConfig(format=FORMAT)
	log=logger.getLogger('createStoreDashboard')

	log.info('   _____              _         __     _____  __                __ ')
	log.info('  / ___/ _____ _____ (_)____   / /_   / ___/ / /_ ____ _ _____ / /_')
	log.info('  \__ \ / ___// ___// // __ \ / __/   \__ \ / __// __ `// ___// __/')
	log.info(' ___/ // /__ / /   / // /_/ // /_    ___/ // /_ / /_/ // /   / /_  ')
	log.info('/____/ \___//_/   /_// .___/ \__/   /____/ \__/ \__,_//_/    \__/  ')
	log.info('                    /_/                                            ')
	log.info('')

	## parse script arguments
	parser = argparse.ArgumentParser(description='Parse text file to create Store Dashboards in LogicMonitor')
	parser.add_argument('-f', action='store', nargs=1, type=argparse.FileType('r'), required=True, dest='storeList',
                    help='Name of text file with list of store numbers.')

	## Open text file for parsing
	with open(storeList) as sl:
		for line in sl:
			storeNum=line
			## Setup Variables needed for Data JSON call
			dbName="Store Dashboard - " + storeNum
			dbDecription="Dashboard for Store " + storeNum
			groupName="Store Dashboards"

			log.info('Generating API Data JSON for store number %s' % storeNum)
			try:
				data=LogicMonitor_API.getDashboardData("1", dbName, dbDecription, "True", owner="", groupName)
				log.info('JSON is %s' % data)
			except:
				log.error("Unexpected error:", sys.exc_info()[0])
				raise

			log.info('Executing API call to create LogicMonitor Dashboard for store %s' % storeNum)
			try:
				LogicMonitor_API.getRequest('POST', '/dashboard/dashboards', data)
				log.info('Dashboard for store %s created successfully' % storeNum)
				log.info('LogicMonitor API response was:')
				log.info(response.content)
			execpt:
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
	log.info('')

## Call main method to execute script
try:
	main()
	sys.exit(0)
except:
	print("Unexpected error:", sys.exc_info()[0])
	raise
