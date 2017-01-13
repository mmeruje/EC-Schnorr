# EC-Schnorr
This project is a python implementation of the Schnorr Zero-Knowledge Protocol over Elliptic Curves.

- ecc.py is a Python class that implements the Elliptic Curve operations needed;
- schnorr.py implements the Schnorr Zero-Knowledge Protocol over.

This project uses the following modules: sys, getopt, sys, PyCrypto, and socket.


Usage: ./schnorr.py [OPTION]... [ARGS]...

Authenticates someone using Schnorr Protocol over Elliptic Curves.   
Shows this message if none of options is used.  
  
Options:

  -gk, --generate-keys     Generates a Key Pair.  
  -a,  --authenticator     Uses a Public Key to authenticate a client.  
  -s,  --supplicant        Uses the Private Key to authenticate itself to a server.  


Usage example:

1. Keypair Generation:
```
mmeruje@mycomputer:~/$ ./schnorr.py -gk
*  Key Generation Mode Activated
*  Generating an a random number. (Private Key)
*  Generating an elliptic curve point. (Public Key)
--- BEGIN PRIVATE KEY ---
1742413906660797398263574261320583321084828220183690165741
--- BEGIN PUBLIC KEY ---
v(x,-) = 241010344193812168014432711399629693373018093471884903517
v(-,y) = 2306444403712286640989713776754269629962048798612334189144
```

2. Run Authenticator (Server):
```
mmeruje@server:~/$ ./schnorr.py -a 241010344193812168014432711399629693373018093471884903517 2306444403712286640989713776754269629962048798612334189144
```
3. Run Supplicant (Client)
```
mmeruje@client:~/$ ./schnorr.py -s 1742413906660797398263574261320583321084828220183690165741
```
