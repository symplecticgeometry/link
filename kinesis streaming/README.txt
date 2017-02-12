There are 5 scripts in this folder:

froms3tokinesis1.py, 
froms3tokinesis2.py, 
froms3tokinesis3.py, 
froms3tokinesis4.py, 
froms3tokinesisfake.py

They are used to send data into kinesis.

Venmo transaction data is collected and stored in Amazon s3. 

froms3tokinesis1.py sends the transaction data for year 2010-2013.
froms3tokinesis2.py sends the transaction data for year 2014.
froms3tokinesis3.py sends the transaction data for year 2015.
froms3tokinesis4.py sends the transaction data for year 2016.
froms3tokinesisfake .py sends sends the simulated data. *

Moreover the Venmo transaction data does not contain the transaction amount, 
so for each transaction, we generate a random number as the transaction amount.

* For live demonstration purpose, we simulate 100 users and transactions between them,
so that we can see the change of data easily when we focus on these users. 
