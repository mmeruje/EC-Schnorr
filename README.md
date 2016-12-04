# EC-Schnorr
This project is a python implementation of the Schnorr Zero-Knowledge Protocol over Elliptic Curves.

- ecc.py is a Python class that implements the Elliptic Curve operations needed;
- schnorr.py implements the Schnorr Zero-Knowledge Protocol over.

This project uses the following modules: sys, getopt, sys, PyCrypto, and socket.


Usage: ./schnorr [OPTION]... [ARGS]...

Authenticates someone using Schnorr Protocol over Elliptic Curves.   
Shows this message if none of options is used.  
  
Options:

  -gk, --generate-keys     Generates a Key Pair.  
  -a,  --authenticator     Uses a Public Key to authenticate a client.  
  -s,  --supplicant        Uses the Private Key to authenticate itself to a server.  
