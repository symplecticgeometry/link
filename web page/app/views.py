from __future__ import print_function
import base64
import boto3
import json
import decimal
import re
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from flask import request
from flask import render_template
from app import app
import sys


@app.route('/')
def searchinput():
	return render_template("searchinput.html")

@app.route("/", methods=['POST'])
def transactionsearch_post():
	user_id = request.form["userid"]
	user1_id = request.form["user1id"]
	user2_id = request.form["user2id"]
	choice = request.form["choice"]


	dynamodb = boto3.resource('dynamodb')
	table_t = dynamodb.Table('alltransactions')
	table_u = dynamodb.Table('allusers3')
	table_ub = dynamodb.Table('userbalance')
	
	print (user1_id, user2_id)
	
	# query balance below


	try:
		response_bal = table_ub.get_item(
			Key={
				'userid': user_id,
			}
		)
	except ClientError as e:
		print('user is not found')
		user_id = "NA"
		Balance = "NA"
		print("get balance wrong")
	else: 
		balance = response_bal['Item']['balance']
		Balance = str(balance/100)
		print("get balance okay")
	
	
	# query net and absolute transactions below
	
	try:
		response_bal = table_u.get_item(
			Key={
				'user1id': user1_id,
				'user2id': user2_id
			}
		)
	except ClientError as e:
		user1_id = "NA"
		user2_id = "NA"
		str_abs_tran = "NA"
		str_net_tran = "NA"
		print("get transaction wrong")

	else: 
		abs_tran = response_bal['Item']['abs_transaction']
		net_tran = response_bal['Item']['net_transaction']
		str_abs_tran = str(abs_tran /100)
		str_net_tran = str(net_tran /100)


	if choice == "where does my money go":
		try:
			response = table_u.query(
				KeyConditionExpression = Key('user1id').eq(user_id)
			)

		except ClientError as e:
			print('user ', user_id, ' is not found.')
			list = ["NA"]

		else: 
			print(response['Items'])
			list = response['Items']



	# query transactions below
	
	if choice == "transactions":

		try:
			response = table_t.query(
				KeyConditionExpression = Key('user1id').eq(user_id)
			)

		except ClientError as e:
			print('user ', user_id, ' is not found.')
			list = ["NA"]

		else: 
			list = response['Items']


	
	if choice == "balance":
		jsonresponse = [{"userid": user_id, "user1id": user1_id, "user2id": user2_id, "balance": Balance, "str_abs_tran": str_abs_tran, "str_net_tran": str_net_tran}]
		return render_template("searchresults.html", output=jsonresponse)
	
	elif choice == "where does my money go":
		jsonresponse = [{"user1id": user_id, "user2id": item['user2id'], "abs_transaction": str(item['abs_transaction']), "net_transaction": str(item['net_transaction'])} for item in list]
		return render_template("otherusers.html", output=jsonresponse)

	elif choice == "transactions":
		jsonresponse = [{"user1id": user_id, "user2id": item['user2id'], "transactionid": str(item['transactionid']), "transactionamount": str(item['transaction_amount'])} for item in list]
		return render_template("alltransactions.html", output=jsonresponse)
