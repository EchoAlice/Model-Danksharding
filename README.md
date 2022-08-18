Based off of Vitalik's blog post:
https://blog.ethereum.org/2014/08/16/secret-sharing-erasure-coding-guide-aspiring-dropbox-decentralizer/

This project attempts to create a script that separates and encodes a file into n chunks, such that any m of n chunks can recreate the original file.  This technique is called erasure coding and allows for decentralized data storage (Ethereum uses this technique for data availability sampling). 

For more details on erasure encoding, check out Vitalik's blog post!