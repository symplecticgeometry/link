from __future__ import print_function
import base64
import boto3
import json
import decimal
import re
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)



def UpdateUserTable(list):

	[user_id1, user_id2, trans_id, trans_amnt, table_ub, table_u] = list

	# we update the userbalance table
	try:
		response = table_ub.put_item(
			Item={
				'userid':user_id1,
				'balance': 0,
			},
			ConditionExpression='attribute_not_exists(userid)'
		)
	except ClientError as e:
		print(e.response['Error']['Message'])
	else: print('put the 0 item to table userbalance is OK')

	
	heisenberg = 0  # this tag is used to detect whether the data in dynamodb is changed after read and before write
	while heisenberg == 0:
	
		response_bal = table_ub.get_item(
			Key={
				"userid": user_id1,
				}
		)
		old_balance = response_bal['Item']['balance']
		new_balance = old_balance + trans_amnt
		
		try:
			response_bal2 = table_ub.update_item(
				Key={
					'userid': user_id1
				},
				UpdateExpression="set balance = :amnt2",
				ConditionExpression="balance = :amnt1",
				ExpressionAttributeValues={
					':amnt1': old_balance,
					':amnt2': new_balance
				},
				ReturnValues="UPDATED_NEW"
			)
		except ClientError as e:
			print(e.response['Error']['Message'])
		
		else: 
			heisenberg = 1
	
	# now we update the allusers3 table
	try:
		response1 = table_u.put_item(
			Item={
				'user1id':user_id1,
				'user2id':user_id2,
				'abs_transaction': 0,
				'net_transaction': 0
			},
			ConditionExpression='attribute_not_exists(user1id)'
		)
	except ClientError as e:
		print(e.response['Error']['Message'])
	else: 
		print(' put the 0 item to the table allusers3 is OK')

	
	waterwhite = 0   # this tag is used to detect whether the data in dynamodb is changed after read and before write
	while waterwhite == 0:
		
		response_abs_net = table_u.get_item(
			Key={
				"user1id": user_id1,
				"user2id": user_id2
				}
		)
		
		old_abs_tran = response_abs_net['Item']['abs_transaction']
		old_net_tran = response_abs_net['Item']['net_transaction']
		
		new_abs_tran = old_abs_tran + abs(trans_amnt)
		new_net_tran = old_net_tran + trans_amnt
		
		try:
			response_abs_net2 = table_u.update_item(
				Key={
					'user1id': user_id1,
					'user2id': user_id2
				},
				UpdateExpression="set net_transaction = :new_amntn, abs_transaction = :new_amnta",
				ConditionExpression="(net_transaction = :old_amntn) AND (abs_transaction = :old_amnta)",
				ExpressionAttributeValues={
					':old_amnta': old_abs_tran,
					':old_amntn': old_net_tran,
					':new_amntn': new_net_tran,
					':new_amnta': new_abs_tran
				},
				ReturnValues="UPDATED_NEW"
			)
		except ClientError as e:
			print(e.response['Error']['Message'])
		
		else: 
			waterwhite = 1	


def lambda_handler(event, context):

	dynamodb = boto3.resource('dynamodb')
	table_t = dynamodb.Table('alltransactions')
	table_u = dynamodb.Table('allusers3')
	table_ub = dynamodb.Table('userbalance')
	
	# load data from stream
	for record in event['Records']:
		#Kinesis data is base64 encoded so decode here
		payload=base64.b64decode(record["kinesis"]["data"])
		print("Decoded payload: " + payload)
		trans_data_raw = re.findall(r'(\d+)\s(\d+)\s(\d+)\s(\d+)',payload)
		if trans_data_raw != []:
			trans_data = trans_data_raw[0]
			print ('length0 of trans_data is',  len(trans_data))
			print (trans_data)

			if len(trans_data) == 4:
				user_id1 = str(trans_data[0])
				user_id2 = str(trans_data[1])
				trans_amnt = int(trans_data[2])
				trans_id = str(trans_data[3])
				
				# write the original transaction to the alltransactions table

				table_t.put_item(
					Item={
						'user1id': user_id1,
						'transactionid': trans_id,
						'user2id':user_id2,
						'transaction_amount': trans_amnt
					}
				)

				# we build a mirror transaction to this transaction
				
				muser_id1 = user_id2
				muser_id2 = user_id1
				mtrans_id = '-' + trans_id
				mtrans_amnt = (-1) * trans_amnt
				
				# write the mirror transaction to the alltransactions table
				
				table_t.put_item(
					Item={
						'user1id': muser_id1,
						'transactionid': mtrans_id,
						'user2id': muser_id2,
						'transaction_amount': mtrans_amnt
					}
				)
								
				UpdateUserTable([user_id1, user_id2, trans_id, trans_amnt, table_ub, table_u])
				
				UpdateUserTable([muser_id1, muser_id2, mtrans_id, mtrans_amnt, table_ub, table_u])
