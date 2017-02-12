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

stream = "streamingtran"
kinesis = boto3.client('kinesis')
transactionid = 1
tag = 1

while tag == 1:
	i = random.randint(0,100)
	j = random.randint(0,100)
	amount = random.randint(1,100)
	if i != j:
		newstring = '9999' + str(i) + ' 9999' + str(j) + ' ' + str(amount) + ' ' + str(transactionid)
		print newstring,'\n'
		time.sleep(0.02)
		kinesis.put_record(StreamName=stream, Data=json.dumps(newstring), PartitionKey= str(i))		
							
	transactionid = transactionid + 1
	
