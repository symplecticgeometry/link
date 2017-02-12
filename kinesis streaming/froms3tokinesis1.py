import os
import boto
import sys
import codecs
import re
import copy
from copy import copy
import random
import boto3
import json
import time

# data is send to the kinesis in the form of a string, userid1 userid2 transaction_amount transaction id\n.

aws_access_key = os.getenv('AWS_ACCESS_KEY_ID', 'default')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'default')

waiting_time = 0.05


stream = "streamingtran"
kinesis = boto3.client('kinesis')

bucket_name = "venmo-json"
transactionid = 1
for y in range(2010,2014):
	for m in range(1,13):
		for num in range(1,40):
			if m < 10:
				monthindex = '0' + str(m)
			else: 
				monthindex = str(m)
			if num < 10:
				numindex = '0' + str(num)
			else:
				numindex = str(num)
				
			folder_name = str(y) + '_' + monthindex + '/'
			file_name = 'venmo_' + str(y) + '_' + monthindex + '_' + numindex + '.json'
			
			conn = boto.connect_s3(aws_access_key, aws_secret_access_key)
			bucket = conn.get_bucket(bucket_name)
			key = bucket.get_key(folder_name + file_name)
			if key == None:
				print file_name, 'does not exist'
			else:
				print file_name, 'OK'
				
				string = key.get_contents_as_string()
				
				list = re.findall(r'\"id\"\:\s\"(\d+)\"',string)

				newstring = ''
				marker = 1
				preword = ''
				for word in list:
					randomnumber = random.randint(0,100)
					if word != preword:
						if marker == 1:
							newstring = word
						else:
							newstring = newstring + ' ' + word + ' ' \
							+ str(randomnumber) + ' ' + str(transactionid)
							
							transactionid = transactionid + 4
							print newstring,'\n'
							time.sleep(waiting_time)
							kinesis.put_record(StreamName=stream, Data=json.dumps(newstring), PartitionKey=preword)							
						marker = marker * (-1)
					preword = word



