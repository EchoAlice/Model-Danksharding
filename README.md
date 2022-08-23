Based off of Vitalik's blog post:
https://blog.ethereum.org/2014/08/16/secret-sharing-erasure-coding-guide-aspiring-dropbox-decentralizer/

This project is based off of Vitalik's blog post. It attempts to create a script that separates and encodes a file into n chunks, such that any 
m of n chunks can recreate the original file.  This technique is called erasure coding and has a bunch of cool use cases in the blockchain world. 

The original file can be represented as an integer, then separated into chunks.  The integer chunks can then be used to create a UNIQUE polynomial,
abstractly representing the data to be stored. Create the polynomial via systems of equations or lagrange interpolation. 

** LAGRANGE INTERPOLATION IS UNDER CONSTRUCTION **
** SYSTEMS OF EQUATIONS IS BUNK FOR NOW**

If you know the x coordinates that map to original file (the y coordinates), 
you can reconstruct the file by first recreating the polynomial with any m of n chunks that have been distributed among a network, 
then evaluating the polynomial at the x coordinates!

Within the code, equations are represented as a list of coefficients followed by the y
coordinate transposed to the left side of the equation (y isn't represented within polynomial).
Here's an example of how equations are represented. 

file = [1,3,2,1]
System of equations:
                              [coefficients, -y_coordinate]
  1a^3 + 1b^2 + 1c^1 + d  = 1   --> [1, 1, 1, 1, -1]

  2a^3 + 2b^2 + 2c^1 + d  = 3   --> [8, 4, 2, 1, -3] 
  
  3a^3 + 3b^2 + 3c^1 + d  = 2   --> [27, 9, 3, 1, -2] 
  
  4a^3 + 4b^2 + 4c^1 + d  = 1   --> [64, 16, 4, 1, -1] 

Polynomial:
  0.5x^3 + -4.5x^2 + 12.0x + -7.0 = y   --> [0.5, -4.5, 12.0, -7.0] 