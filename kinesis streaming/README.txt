There are 2 scripts in this folder:

froms3tokinesis.py
froms3tokinesisfake.py

They are used to send data into kinesis.

Venmo transaction data is collected and stored in Amazon s3. 

Use froms3tokinesis.py with a year parameter (2010, 2011,..., 2016) to send Venmo transaction data to kinesis.

Use froms3tokinesisfake.py to send the simulated data. *

Moreover the Venmo transaction data does not contain the transaction amount, 
so for each transaction, we generate a random number as the transaction amount.

* For live demonstration purpose, we simulate 100 users and transactions between them,
so that we can see the change of data easily when we focus on these users. 
