from __future__ import print_function
import base64
import boto3
import json
import decimal
import re

	
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):

	dynamodb = boto3.resource('dynamodb')
	table1 = dynamodb.Table('alltransactions')
	table2 = dynamodb.Table('allusers')
	
	# load data from stream
	for record in event['Records']:
		#Kinesis data is base64 encoded so decode here
		payload=base64.b64decode(record["kinesis"]["data"])
		print("Decoded payload: " + payload)
		transalist = re.findall(r'(\d+)\s(\d+)\s(\d+)\s(\d+)',payload)
		if transalist != []:
			print ('length0 of transalist is',  len(transalist[0]))
			print (transalist[0])

			if len(transalist[0]) == 4:
				print (" length is 4")
				user_id1 = str(transalist[0][0])
				print("user1 id", user_id1)
				user_id2 = str(transalist[0][1])
				print("user2 id", user_id2)
				transactionid = str(transalist[0][2])
				print('transactionid',transactionid)
				transactionamount = str(transalist[0][3])
				print('transactionamount', transactionamount)
				
				
				# write the original transaction to the alltransactions table

				response = table1.put_item(
					Item={
						'user1id': user_id1,
						'transactionid': transactionid,
						'user2id':user_id2,
						'transactionamount': transactionamount
					}
				)

				print("PutItem succeeded:")
				
				
				
				# start from here we deal with the original transaction. Later on, I should build a module
				# get data from the allusers table
				
				absolutenet = table2.get_item(
					Key={
						"user1id": user_id1,
						}
				)
				
				if 'Item' not in absolutenet: # we generate the item
					print('Item is not there')
					tempabsolutenet= table2.put_item(
							Item={
									 'user1id': user_id1,
									 'balance': '0',
									 '(user2id,net$,abs$),...,()':{
										user_id2: ['0','0']
									 }
							}
					)
					
					absolutenet = table2.get_item(
						Key={
							"user1id": user_id1,
							}
					)
				
				
				if user_id2 not in absolutenet['Item']['(user2id,net$,abs$),...,()']:
					print('two users have not done transaction before')
					absolutenet['Item']['(user2id,net$,abs$),...,()'][user_id2] = ['0','0']
				
				# we recalculate the balance, net about, absolute amount, and update the allusers table
				sbalance = absolutenet['Item']['balance']
				print('sbalance=', sbalance)
				ibalance = int(sbalance) + int(transactionamount)
				print('ibalance=', ibalance)
				
				absolutenet['Item']['balance'] = str(ibalance)
				print(absolutenet['Item']['balance'])
				
				[snetamount, sabsoluteamount] = absolutenet['Item']['(user2id,net$,abs$),...,()'][user_id2]
				
				inetamount = int(snetamount) + int(transactionamount)
				
				iabsoluteamount = int(sabsoluteamount) + abs(int(transactionamount))
				
				absolutenet['Item']['(user2id,net$,abs$),...,()'][user_id2] = [str(inetamount), str(iabsoluteamount)]
				oldabsolutenet= table2.put_item(
							Item=absolutenet['Item']
					)
				
				
				print('this is what absolutenet looks like:', absolutenet)
				
				# starting from here, we repeat the above update to the mirror transaction
				
				# we build a mirror transaction to this transaction
				
				muser_id1 = user_id2
				muser_id2 = user_id1
				mtransactionid = '-' + transactionid
				mtransactionamount = '-' + transactionamount
				
				
				# write the mirror transaction to the alltransactions table
				
				mresponse = table1.put_item(
					Item={
						'user1id': muser_id1,
						'transactionid': mtransactionid,
						'user2id': muser_id2,
						'transactionamount': mtransactionamount
					}
				)
				# get data from the allusers table
				
				mabsolutenet = table2.get_item(
					Key={
						"user1id": muser_id1,
						}
				)
				
				if 'Item' not in mabsolutenet: # we generate the item
					print('Item is not there')
					tempmabsolutenet= table2.put_item(
							Item={
									 'user1id': muser_id1,
									 'balance': '0',
									 '(user2id,net$,abs$),...,()':{
										muser_id2: ['0','0']
									 }
							}
					)
					mabsolutenet = table2.get_item(
						Key={
								"user1id": muser_id1,
						}
					)
				

				if muser_id2 not in mabsolutenet['Item']['(user2id,net$,abs$),...,()']:
					print('two users have not done transaction before')
					mabsolutenet['Item']['(user2id,net$,abs$),...,()'][muser_id2] = ['0','0']
				
				# we recalculate the balance, net about, absolute amount, and update the allusers table
				msbalance = mabsolutenet['Item']['balance']
				print('msbalance=', msbalance)
				mibalance = int(msbalance) + int(mtransactionamount)
				print('mibalance=', mibalance)
				
				mabsolutenet['Item']['balance'] = str(mibalance)
				print(mabsolutenet['Item']['balance'])
				
				[msnetamount, msabsoluteamount] = mabsolutenet['Item']['(user2id,net$,abs$),...,()'][muser_id2]
				
				minetamount = int(msnetamount) + int(mtransactionamount)
				
				miabsoluteamount = int(msabsoluteamount) + abs(int(mtransactionamount))
				
				mabsolutenet['Item']['(user2id,net$,abs$),...,()'][muser_id2] = [str(minetamount), str(miabsoluteamount)]
				moldabsolutenet= table2.put_item(
							Item=mabsolutenet['Item']
				)