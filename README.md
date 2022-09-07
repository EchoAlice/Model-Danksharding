**Getting Started**

Enter in CLI:                      
pip install -r requirements.txt

Working Directory and command to execute:             
./erasure-coding$     python ./src/main.py

**Importance of Erasure/Reed Solomon Coding**

Based off of Vitalik's blog post: \
https://blog.ethereum.org/2014/08/16/secret-sharing-erasure-coding-guide-aspiring-dropbox-decentralizer/

Erasure/Reed Solomon coding is a technique that separates data of m chunks and encodes these into n chunks, such that any m of n chunks can be used 
to recreate the original data.  This concept is employed by Ethereum to make data availability sampling of blobs feasible for sharding.  Erasure
coding makes it impossible for an individual to withhold even a single bit of information without anyone requesting this information to be able to
detect foul play.
My project implements this technique. 

**Summary of Project**

A string of numbers is passed in as the data we wish to encode.  This string is broken up into m chunks and then converted into points (the string ints
we care about are the y-coordinates, each cooresponding x-coordinates consisting of integers 1 -> m) that a can 
be used to represent a UNIQUE polynomial equation that passes through said points, abstractly representing the data to be stored.
This process of creating a unique polynomial which maps directly to given points is called lagrange interpolation.   

***The polynomial created from the original string is the only polynomial that passes through these points***

Because of this mathematical truth, one can evaluate the polynomial at x-coordinates m -> n to expand the data and reconstruct the original polynomial
from any m of n chunks!

Within the code, I display how this works in practice by splitting up the extended data chunks among nodes, then randomly select chunks from the set
of nodes to recreate the polynomial.  By knowing the x coordinates for the points representing the original file, I can evaluate the reconstructed
polynomial at these x coordinates to recover the original file!

**TO DO:**
- Create conditional statements for user input
- Incorperate encryption of data before sending it to nodes
- Optimize the heck out of this
- Allow small files to be encoded