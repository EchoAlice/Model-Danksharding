# Model Data Availability Sampling

**Getting Started**

Enter in CLI:                      
pip install -r requirements.txt

Working Directory and command to execute:             
./Model-DAS$     python ./src/main.py



**Summary** 
Model DAS is a project that intends to simulate a local (for now) model of Data Availability Sampling.

The major areas of DAS are:
    - Erasure coding data
    - Peer to peer networking   

This project is based off of Vitalik's [post](https://hackmd.io/@vbuterin/sharding_proposal).

\
What is erasure coding?
-----------------------
Erasure/Reed Solomon coding is a technique where data is separated into m chunks and encoded into n chunks, such that any m of n chunks can be used 
to recreate the original data.  
Let's say we expand the chunks by a factor of 2, ANY 50% of the chunks could be used to reconstruct the original data.
This makes it almost impossible for a bad actor to withhold even a single bit of data without randomly sampling peers being able to easily detect foul play.  

"It gives us a way to turn 50% availability into 100% availability."
                                              -Vitalik

Erasure coding uses polynomial interpolation to make this reconstruction happen. 

More details on the math:
  https://blog.ethereum.org/2014/08/16/secret-sharing-erasure-coding-guide-aspiring-dropbox-decentralizer/
  
  
\
How is it useful?
-----------------
Because of this technique, you can have sets of peers each download a portion of the data and proof, attest to its availability, then see if a certain percentage of attestations were available, instead of having to download the entirety of the data to verify its 
availability on the chain.  This increases scalability.

The concept is employed by Ethereum to make rollups' state changes available on the base layer.  If a rollup goes offline or intentionally
withholds data, anyone on the base layer could reconstruct the state of the rollup with this available data and prevent assets/data from being
withheld.

More detailed explanation of use cases and importance here: \
    https://hackmd.io/@vbuterin/sharding_proposal


\
How do peers communicate with one another about data availability?
------------------------------------------------------------------
This is the part of the project that is much less solidified.  People are still thinking about the best ways to have peers communicate with one
another about a blob's availability.

Discussions on the matter:
    *Link discussions here*



\
  Project Update
===================
I'm mocking a horizontal subnet (p2p subnetwork where validators talk to one another about availability of a blob).   
This involves building out the [Kademlia DHT](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf) for the network. I have built a naive routing table for the nodes of the network.  
The next step is to create hash tables that store the information of the k-nodes closest to them.

**TO DO:**
1. Summarize within readme:
      - Erasure coding
      - Fast Fourier Transformations
      - Kate Commitments
      - How they all link together
      
2. Continue research into costs/benefits of different peer to peer networking schemas.  See what the pros are thinking about implementing.

3. Create HashTable class for nodes

4. Create a new lagrange function which utilizes [Fast Fourier Transforms](https://https://vitalik.ca/general/2019/05/12/fft.html) (Makes lagrange viable).
  
5. Create KZG commitments for proofs that the blob will use 