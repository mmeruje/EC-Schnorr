#!/usr/bin/python
# -*- coding: utf-8 -*-


# Schnorr Protocol over Elliptic Curves
# Sistemas de Software Seguro
# Computer Science MSc
# Universidade da Beira Interior
# Manuel Luis Gama Meruje, m6620



import sys
import ecc
import Crypto.Util.number
import socket 

host = 'localhost' 
port = 6666
dataSize = 2048

p = ecc.ECcurve().p
q = ecc.ECcurve().q

# --generate_keys
def generate_keys():
	""" 
	Supplicant Mode - Key Generation
	""" 
	# ##############################################
	#
	# 	o seguinte pedaço de código está comentado 
	# 	devido à sua complexidade (a nível temporal)
	# 	e o protocolo para que este pudesse ser implementado
	#
	# ##############################################
	# # gerar primo P
	# p = Crypto.Util.number.getStrongPrime(size) 
	# while 1:
	# 	# gerar primo Q que divida P-1
	# 	q = Crypto.Util.number.getPrime(size)
	# 	if ((p-1)%q == 0):
	# 		break
	# ##############################################
	
	# selecionar uma curva eliptica - definida em ECcurve
	ec=ecc.ECcurve()

	# a = r <- {0, ..., Q − 1} [Alice calcula a chave privada a.]
	print "*  Generating an a random number. (Private Key)"
	a = Crypto.Util.number.getRandomRange(0, (q-1))

	# v = −a.G(modP) [Alice calcula a chave pública v (um ponto na curva elíptica).]
	# v = (-a*ec_G) % p

	# atenção à coordenada y! G = (xi, xf)
	print "*  Generating an elliptic curve point. (Public Key)"
	pbp = ecc.ECPoint(ec.xi, ec.yi)
	pbp = pbp.multiplyPointByScalar(a)
	pbp = pbp.simmetric()

	print "--- BEGIN PRIVATE KEY ---"
	print a
	print "--- BEGIN PUBLIC KEY ---"
	print "v(x,-) = " + str(pbp.x)
	print "v(-,y) = " + str(pbp.y)
	
	return [a,pbp.x,pbp.y]



# --suplicant
def supplicant(a):
	""" 
	Alice / Supplicant / Client Mode
	""" 

	#host = 'localhost' 
	#port = 8888 
	#dataSize = 1024 
	print "*  Opening socket"
	print "*   - host: " + str(host)
	print "*   - port: " + str(port)
	
	aChannel = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	aChannel.connect((host,port)) 
	
	print "\n*  Connected to Bob (Authenticator)."
	
	# GERA UM NUMERO R para usar em  x=r.G(modP) para calcular um ponto na curva eliptica
	print "*  Generating a r random number."
	ec= ecc.ECcurve()
	r = Crypto.Util.number.getRandomRange(0, (q-1))
	print "*  Number r generated."
	print "\tr = " + str(r)
	print "*  Getting point X on the elliptic curve."
	x = ecc.ECPoint(ec.xi, ec.yi)
	x = x.multiplyPointByScalar(r)

	# enviar V
	#print "\nVx: " + hex(x.x)
	#print "Vy: " + hex(x.y)
	#aChannel.send(str(x.x))
	#aChannel.send(str(x.y))

	# enviar x
	# print "\n<- sending X."
	print "\tXx: " + hex(x.x)
	print "\tXy: " + hex(x.y)
	aChannel.send(str(x.x)) 
	aChannel.send(str(x.y))
	print "\n<- X sent."

	# receber e
	#print "\n-> Receiving e."
	e = aChannel.recv(dataSize)
	e = int(e)
	print "\n-> e received."
	print "\te: " + hex(e)

	if e<2**80:
		print "*  e is valid."
	else:
		print "*  e is not valid."
		return


	# Alice verifica que o valor de e está no intervalo apropriado


	# calcular Y
	#print "\n*  Calculating y."
	y = a*e + r
	print "\n*  y was calculed."
	print "\ty: " + hex(y)

	# enviar y
	# print "\n<- sending y."
	aChannel.send(str(y))
	print "\n<- y sent."

	aChannel.close()
	print "*  Connection closed.\n"

# --authenticator
def authenticator(v):

	""" 
	Bob / Authenticator / Server Mode
	""" 

	#host = '' 
	#port = 8888 
	nClients = 5
	#dataSize = 1024 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.bind((host,port)) 
	s.listen(nClients) 
	bChannel, address = s.accept()

	print "*  Alice is connected."

	# receber v
	#vx = bChannel.recv(dataSize)
	#vy = bChannel.recv(dataSize)
	#v  = ecc.ECPoint(int(vx), int(vy))
	#print "\n-> V received with the following values: "
	#print "\tVx: " + hex(v.x)
	#print "\tVy: " + hex(v.y)

	# receber x
	xx = bChannel.recv(dataSize) 
	xy = bChannel.recv(dataSize) 
	x  = ecc.ECPoint(int(xx), int(xy))
	print "\n-> x received with the following values: "
	print "\txx: " + hex(x.x)
	print "\txy: " + hex(x.y)

	# gera e
	e = Crypto.Util.number.getRandomRange(0, 2**80)
	print "\n*  e generated.\n\t e: " + hex(e)
	# envia e
	bChannel.send(str(e))
	print "\n<- e sent."

	# receber y
	y = bChannel.recv(dataSize) 
	y = int(y)
	print "\n-> y received with the following value: "
	print "\ty: " + hex(y)


	# calcular z
	ec= ecc.ECcurve()
	z = ecc.ECPoint(ec.xi, ec.yi)
	z = z.multiplyPointByScalar(y)
	v = v.multiplyPointByScalar(e)
	
	z = z.sum(v)
	
	# verifiar z e x
	print "\n\n*  Final Result: \n"
	if z.x == x.x and z.y == x.y:
		print "\t\tSuccess!"
	else:
		print "\t\tFail!"
	print "\n"

	bChannel.close()
	print "*  Connection closed\n"

def main():

	if (("--generate-keys" in sys.argv) or ("-gk") in sys.argv) and (len(sys.argv)==2):
		# chamar generate_keys()
		print "*  Key Generation Mode Activated"
		keys=generate_keys()
		
		# ##############################################################
		#
		# o seguinte pedaço de código não é executado
		# uma vez que a chave pública é inserida aquando
		# da execução do aplicativo em modo --authenticator
		# pelo que o autenticador (Bob) deve ter acesso à chave 
		# pública directamente em algum sítio, e.g., conversa
		# de café; "download" no site pessoal internet do cliente; ...
		#
		# ##############################################################
 		#
		# # chamar supplicant()
		#a = keys[0]
	 	#print "\n*  Alice Mode Activated."
	 	#print "*  a = " + str(a)
		#supplicant(keys[0])
		# ##############################################################

	elif (("--supplicant" in sys.argv) or ("-s" in sys.argv)) and (len(sys.argv)==3) :
		# chamar supplicant()
		a = int(sys.argv[2])
	 	print "*  Alice Mode Activated (Supplicant Mode)"
	 	print "*  a = " + str(a)
		supplicant(a)

	elif (("--authenticator" in sys.argv) or ("-a" in sys.argv)) and (len(sys.argv)==4) :
		# chamar authenticator()
	 	print "*  Bob Mode Activated (Authenticator Mode)"
	 	print "*  This will be the public key used in the authentication:"
		vx = int(sys.argv[2])
		vy = int(sys.argv[3])
		v = ecc.ECPoint(vx,vy)
	 	print "  v(x,-) = " + str(v.x)
	 	print "  v(-,y) = " + str(v.y)
	 	print "*  Trying to listen to Alice."
		authenticator(v)

	else:
		# caso contrŕario mostrar mensagem de erro / ajuda
		usage='''
 Usage: ./schnorr [OPTION]... [ARGS]...
 Authenticates someone using Schnorr Protocol over Elliptic Curves
 Shows this message if none of options is used.

 Mandatory arguments to long options are mandatory for short options too.
  -gk,\t--generate-keys\tGenerates a Key Pair.
  -a,\t--authenticator\tUses a Public Key to authenticate a client.
  -s,\t--supplicant\tUses the Private Key to authenticate itself to a server.\n
		'''
		print usage


if __name__ == "__main__":
	main()
