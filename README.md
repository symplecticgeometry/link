This project is done under the Insight Data Engineering Fellows program. The program is designed for people with strong knowledge of computer science fundamentals to transition to a career in data engineering.  Insight gives us space to get hands on experience building distributed platforms on AWS and using open source technologies. We built these platforms in 3 weeks.

## What is link?
link is a streaming data pipeline for a digital wallet. 

## Why link?
* It gives user better control of their finance, and
* It lowers transaction risks. 

## Main features:
* Users can check their net transactions with other users at real-time, and
* Users can check their financial bonds with other users at real-time.

## The data pipeline consists of the following:
1. Venmo data stored in S3 is sent to Kinesis,
2. Kinesis sends the data1 to Lambda,
3. Lambda queries historical data2 from Dynamodb,
4. Lambda processes the data2 using data 1, and stores the result back to Dynamodb, and
5. A web application built by Flask queries data from Dynamodb. 

## Running instructions:
1. Create a stream in Kinesis and run the script froms3tokinesisreal.py in the folder kinesis;
2. Upload the script balanceupdate.py in folder lambda to Amazon lambda;
3. Build three tables in Dynamodb as instructed in README in the folder dynamodb;
4. Run tornadoapp.py in the web page.

## Definition of net transation:
Let T(i,j,t) be the transaction amount (with unit in $) from user i to user j at time t. Then we define N(i,j) __the net transaction from user i to user j__ to be the sum of T(i,j,t) over all t.

__Remark:__
Note that since T(i,j,t) = -T(j,i,t), we have N(i,j)= - N(j,i).

## Definition of absolute transaction:
Let T(i,j,t) be the transaction amount (with unit in $) from user i to user j at time t. Then we define A(i,j) __the absolute transaction from user i to user j__ to be the sum of |T(i,j,t)| over all t, where |*| stands for the absolute value of *.

__Remark:__
Since A(i,j,t) = A(j,i,t), instead of saying the absolute transaction from user i to user j, we usually say the abolute transaction between user i and user j. 

## Definition of financial bond of degree one:
We define B(i,j,1) the __financial bonds of degree one__ between user i and user j to be A(j,i). 

__Example:__
Suppose there are two transactions between user i and user j in total: user i sends to user j $5 at t = 0, and user j sends to user j $5 at t=1. Then B(i,j) = 0 while A(i,j) = 10. From this example, we can see that A(i,j) provides a lot more information about the financial bonds between the two users. In particular, suppose in the future, user i is trying to send $1 to user j, the system can provide the information A(i,j)=10 to user i to assist her/him to judge the risk of this transaction.

## Definition of financial bond of degree n:
Consider a weighted graph G, whose vertices are all the users, and there is an edge E(i,j) connecting vertex i and vertex j if and only if there is a transaction from user i to user j or from user j to user i. The __weight__ for E(i,j) is defined to be A(i,j) the absolute transaction between user i and user j. Note that the edges are not directed. 

For fixed vertices i and j, and for a fixed natural number n, we consider all the paths in G connect i and j using less than or equal to n edges. We define a subgraph G(n) of G to be the union of these paths in the obvious sense. We will define the financial bond from vertices i to j to be the maximal flow from vertex i to vertex j. For this purpose, we consider the maximal flow problem:
Imagine that there is a source at vertex i and a sink at vertex j. Incompressible liquid can flow along the edges of the graph G(n). Each edge E(p,q) of G(n) alows a maximal flow of A(p,q) gallons per second. At each vertex other than vertex i and j, we require the flows going in is the same as the flow coming out. 
We define B(i,j,n) the __financial bond of degree n__ to be the maximal flow per second from source i to source j.

__Remark:__ 
One can easily see that the two definitions of financial bonds of degree one agree.

__Example:__
User i sends $5 to user j, user j sends $10 to user k. Then the financial bond of degree 2 between user i and user j is $10. For example, user j and user k are actually belong to the same real person (common for bitcoin), and this person transfers money between two accounts of her own. In a sense, the financial bond of degree two roughly group user i and user j as the same user without knowing that they are. 
