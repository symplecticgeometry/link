We are from the Insight Data Engineering Fellows program. The program is designed for people with strong knowledge of computer science fundamentals to transition to a career in data engineering.  Insight gives us space to get hands on experience building distributed platforms on AWS and using open source technologies. We built these platforms in 3 weeks.

What is link?
link is a streaming data pipeline for a digital wallet. 

Why link?
It gives user better control of their finance.
It lowers transaction risks. 

Main features:
1. Users can check their net transactions with other users at real-time.
2. Users can check their financial bonds with other users at real-time.

Definition of net transation:
Let T(i,j,t) be the transaction amount (with unit in $) from user i to user j at time t. Then we define N(i,j) the net transaction from user i to user j to be the sum of T(i,j,t) over all t.

Remark: Note that since T(i,j,t) = -T(j,i,t), we have N(i,j)= - N(j,i).

Definition of absolute transaction:
Let T(i,j,t) be the transaction amount (with unit in $) from user i to user j at time t. Then we define A(i,j) the absolute transaction from user i to user j to be the sum of |T(i,j,t)| over all t, where |*| stands for the absolute value of *.

Remark: Since A(i,j,t) = A(j,i,t), instead of saying the absolute transaction from user i to user j, we usually say the abolute transaction between user i and user j. 

Definition of financial bond of degree one:
We define B(i,j,1) the financial bonds of degree one between user i and user j to be A(j,i). 

Example:
Suppose there are two transactions between user i and user j in total: user i sends to user j $5 at t = 0, and user j sends to user j $5 at t=1. Then B(i,j) = 0 while A(i,j) = 10. From this example, we can see that A(i,j) provides a lot more information about the financial bonds between the two users. In particular, suppose in the future, user i is trying to send $1 to user j, the system can provide the information A(i,j)=10 to user i to assist her/him to judge the risk of this transaction.

Definition of financial bond of degree n:
Consider a weighted graph G, whose vertices are all the users, and there is an edge E(i,j) connecting vertex i and vertex j if and only if there is a transaction from user i to user j or from user j to user i. The weight for E(i,j) is defined to be A(i,j) the absolute transaction between user i and user j. Note that the edges are not directed. 

For fixed vertices i and j, and for a fixed natural number n, we consider all the paths in G connect i and j using less than or equal to n edges. We define a subgraph G(n) of G to be the union of these paths in the obvious sense. Now we consider the maximal flow problem:
There is a source at vertex i, there is a sink at vertex j. Incompressible liquid can flow along the edges of the graph G(n). Each edge E(p,q) of G(n) alows a maximal flow of A(p,q) gallons per second, now we define  the maximal flow from source i to source
