# Model Danksharding

*This document is a work in progress!*

**Getting Started**

Enter in CLI: &nbsp;&nbsp;&nbsp;&nbsp; pip install -r requirements.txt

Working Directory and command to execute:             
./Model-Danksharding$ &nbsp;&nbsp;    python ./src/main.py



## Project Summary 
Model Danksharding is a project that intends to simulate the architectural designs and logic behind Danksharding. The goal is to gain a deep understanding of the mathematics and networking that underpin this topic.  I plan on implementing functionality in layers, iterating on each with increasing complexity.





This project is based off of Vitalik's [post](https://hackmd.io/@vbuterin/sharding_proposal).
*Add other resources!*

## What is Danksharding?

Danksharding is the major scaling solution within Ethereum's roadmap that allows for vast improvements with regards to the amount of information (transactions) the layer 1 blockchain can come to consensus on.  It is built under the vision of the [rollup-centric roadmap](https://ethereum-magicians.org/t/a-rollup-centric-ethereum-roadmap/4698), where computation of transactions are moved off-chain while settlement of these transactions are kept on-chain.

This style of scaling solution introduces a weakness to the system: a rollup could accidentally/intentionally freeze transactions off-chain, keeping participants from withdrawing.  
To prevent this, these rollups must publish state transitions on chain in the form of a blob of data. Blobs have to be verified as downloadable in order to make it on chain (a blob that hides too much information to recover the state difference of the rollup is useless).  

*Explain what blobs actually are.  Link resources!*  

How do we come to consensus on what blobs are available without each person having to download the entire blob (which reduces scalability- the whole point of Danksharding!)?  Data Availability Sampling over peer to peer networks!

Mental Model of Danksharding:

                                     Danksharding
                                      /         \
                                     /           \
                                    /             \
                             P2P Networking    Data Availability
                               /      \            Sampling
                              /        \           /      \
                             /          \         /        \
                          WIP           WIP    Erasure    KZG Commitments
                                               Coding




## What is Data Availability Sampling? 

Data availability sampling allows for independent actors to come to consensus on whether some set of data is available, without requiring any individual to download all of said data. The idea is that if enough nodes/actors can each verify and attest that their subset of samples are available, the network of peers can decide whether a data set (blob) is available to be downloaded, if necessary.

This process is fragile though... (Link Data Availability Problem here)
  1.  How can we prevent a bad actor, hosting the blob, from hiding a small piece of data?  
      Right now, unless the network of peers collectively check EVERY SINGLE BIT of information, the actor has a chance of hiding/perverting data without the network detecting foul play.  
      
      **It is important that the entire blob is available**.  In blockchain world, if a single bit of information is incorrect or withheld the entire system could be broken.  Think: "Alice mints 1,000,000 Eth"

      Erasure coding allows for the entire network to come to consensus on data availability without having to check for each individual piece of the blob. 
      More on this later :)


  2. *Ask question insinuating how KZG commitments come into play!*




## What is erasure coding?

Data <-> Bytes <-> Integers &nbsp;&nbsp;&nbsp; (:

Erasure coding is the process of extending a data set of m chunks into n chunks, so any m of n chunks can be used to reconstruct the original data set. The technique converts chunks to points [(1, chunk_1), (2, chunk_2) ... (m, chunk_m)] and creates a unique, lowest degree, polynomial that goes through each point via lagrange interpolation.  One can then evaluate this polynomial at an arbitrary number of points to extend the data.

If you know ANY m points, you can use those points to reconstruct the entire set of original data.

*This is a naive implementation of erasure coding.  In order to make this work in real life, we must utilize [Fast Fourier transforms](https://vitalik.ca/general/2019/05/12/fft.html) to make erasure coding efficient.  More on this later...*

Let's say we expand the chunks by a factor of 2.  ANY 50% of the chunks could be used to reconstruct the original data.  Now all of a sudden, if a bad actor wanted to withhold any information, they'd have to withhold over 50% of the data.  
So... if a network of peers wanted to check for the availability of a blob (how the network prevents assets/transactions from being frozen) they would be able to verify availability if 50% of different samples were attested. 

"It gives us a way to turn 50% availability into 100% availability."
                                              -Vitalik
                                              
**This makes data availability sampling much more robust!**

My favorite article explaining the math:
 https://blog.ethereum.org/2014/08/16/secret-sharing-erasure-coding-guide-aspiring-dropbox-decentralizer/

More detailed explanation of use cases and importance here: https://hackmd.io/@vbuterin/sharding_proposal





## What are KZGs?

*WIP*




## How do peers communicate about data availability?

*WIP*



# Project Plan 

Start out with lots of assumptions, black boxing complex tasks, then implement functionality/remove assumptions as the project gets implemented further.

There will be benchmarks for the different levels of this project. 
Each level increases the scope and complexity of the system.

For now, the encoding and networking logic will all be contained locally.



# Project Update


I was in the midst of mocking a horizontal subnet (p2p subnetwork where validators talk to one another about availability of a blob) when the Ethereum Protocol Fellowship began.

So... there is a naively implemented [Kademlia DHT](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf) routing table (tells nodes in a peer to peer network who they should talk to) waiting for a hash table data structure to be created.

However, I'm taking a step back to reassess the direction of the project.  
Setting thoughtful benchmarks requires understanding the entirety of Danksharding.
Continuing to update the readme will help weave together concepts and conceptualize the system.

**TO DO:**
1. Summarize within readme:
      - KZG Commitments
      - Peer to Peer Networking
      - Fast Fourier Transformations
      - How they all link together
    
2. Continue research on peer to peer networks. 

&nbsp;&nbsp;&nbsp;*The following steps may change.  Will have a broader plan within the next week(ish)!*

3. Create HashTable class for nodes
4. Create a new lagrange function which utilizes [Fast Fourier Transforms](https://https://vitalik.ca/general/2019/05/12/fft.html) (Makes lagrange viable).
5. Create KZG commitments for proofs of samples' availability 