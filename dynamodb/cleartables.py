from __future__ import print_function # Python 2/3 compatibility
import boto3
from boto3.dynamodb.conditions import Key, Attr
import base64
import boto3
import json
import decimal
import re
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import sys

'''This function delete all elements in the dynamodb talbe alltransactions, allusers3, userbalance '''

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('alltransactions')

table2 = dynamodb.Table('allusers3')

table3 = dynamodb.Table('userbalance')

	

for a in '0123456789':
	try:
		response = table3.scan(
			FilterExpression=Key('userid').begins_with(a)
		)
		items = response['Items']

		for item in items:
			key = {}
			key['userid']=item['userid']
			response = table3.delete_item(Key = key)
	except:
		pass


for a in '0123456789':
	try:
		response = table.scan(
			FilterExpression=Key('user1id').begins_with(a)
		)
		items = response['Items']

		for item in items:
			key = {}
			key['user1id']=item['user1id']
			key['transactionid']=item['transactionid']
			response = table.delete_item(Key = key)
	except:
		pass




for a in '0123456789':
	try:
		response = table2.scan(
			FilterExpression=Key('user1id').begins_with(a)
		)
		items = response['Items']
	
		for item in items:
			key = {}
			key['user1id']=item['user1id']
			key['user2id']=item['user2id']
			response = table2.delete_item(Key = key)
	except:
		pass

