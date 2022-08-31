**Getting Started**
Enter in CLI:    pip install -r requirements.txt

**Summary of Project**
Based off of Vitalik's blog post:
https://blog.ethereum.org/2014/08/16/secret-sharing-erasure-coding-guide-aspiring-dropbox-decentralizer/

This project attempts to create a script that separates and encodes a file into n chunks, such that any 
m of n chunks can recreate the original file.  This technique is called erasure coding and has a bunch 
of cool use cases in the blockchain world. 

The original file can be represented as an integer, then separated into chunks.  The integer chunks that are the file can then be used as the 
y-coordinates of specific points that map to create a UNIQUE polynomial, abstractly representing the data to be stored. The process of creating 
this unique polynomial to given points is called lagrange interpolation. 

If you know the x coordinates that map to the original file (the y coordinates), 
you can reconstruct the file by first recreating the polynomial with any m of n chunks that have been distributed among a network, 
then evaluating the polynomial at the file's known x coordinates!

**TO DO:**
- Encorperate cryptography
- Write more tests
- Create CLI tool for users to send file to be encoded