import sys
import getopt

def bit_length(self):
   """This function returns the number of bits of self"""
   s = bin(self)       # binary representation:  bin(-37) --> '-0b100101'
   s = s.lstrip('-0b') # remove leading zeros and minus sign
   return len(s)       # len('100101') --> 6

def modInverse(a, n):
   """This function calculates the inverse of a modulo n"""
   i = n
   v = 0
   d = 1
   while a > 0 :
      t = i/a
      x = a
      a = i % x
      i = x
      x = d
      d = v - t*x
      v = x

   v %= n
   if v < 0 :
      v = (v+n)%n
   return v

class ECcurve:
   """A class defining a curve for elliptic curve crypto"""
   # brainpool192r1 - Brainpool curve over a 192 bit prime field
   p = int("C302F41D932A36CDA7A3463093D18DB78FCE476DE1A86297",16)
   a = int("6A91174076B1E0E19C39C031FE8685C1CAE040E5C69A28EF",16)
   b = int("469A28EF7C28CCA3DC721D044F4496BCCA7EF4146FBF25C9",16)
   xi = int("C0A0647EAAB6A48753B033C56CB0F0900A2F5C4853375FD6",16)
   yi = int("14B690866ABD5BB88B5F4828C1490002E6773FA2FA299B8F",16)
   q = int("C302F41D932A36CDA7A3462F9E9E916B5BE8F1029AC4ACC1",16)
   i = int("1",16)
   fieldSize = 192


class ECPoint:
   """A class defining a point for the EC"""
   x = 0
   y = 0
   ec = ECcurve()

   def __init__(self, x, y):
      self.x = x
      self.y = y

   def doublePoint(self):
      s = ((3 * (self.x * self.x)) + self.ec.a ) * (modInverse(2 * self.y, self.ec.p)) % self.ec.p
      x3 = (s * s - self.x - self.x) % self.ec.p
      y3 = (s * (self.x - x3) - self.y) % self.ec.p
     
      return ECPoint(x3,y3)

   def sum(self,p2):
      if self.x == p2.x:
         if self.y == p2.y:
            return self.doublePoint()
         return ECPoint(null, null)
       
      #
      s  = ((p2.y - self.y) * modInverse(p2.x - self.x + self.ec.p, self.ec.p))  % self.ec.p 
      x3 = (s**2 - self.x - p2.x        )     % self.ec.p 
      y3 = (s * (self.x - x3) - self.y  )     % self.ec.p 
      #
      
      return ECPoint(x3,y3)


   def multiplyPointByScalar(self, n):
      nbits = n.bit_length()
      result = ECPoint(self.x,self.y) # t<-a

      #  
      for i in range (1, nbits):
        result = result.doublePoint() # t = t + a mod p
        bit = ( n >> (nbits-i-1) ) & 1
        if bit == 1:
          result=result.sum(self)
      #  

      return result;

   def simmetric(self):
      return ECPoint(self.x, -self.y + ECcurve().p)

def main():
  p1 = ECPoint(int("188DA80EB03090F67CBF20EB43A18800F4FF0AFD82FF1012",16),int("07192B95FFC8DA78631011ED6B24CDD573F977A11E794811", 16))
  print hex(p1.doublePoint().x)
  print hex(p1.doublePoint().y)
  p2 = p1.doublePoint()
  p3 = p2.sum(p1)


  print "p1+p1+p1"
  print hex(p2.sum(p1).x)
  print hex(p2.sum(p1).y)

  print "3*p1"
  print hex(p1.multiplyPointByScalar(3).x)
  print hex(p1.multiplyPointByScalar(3).y)

  print "p1+p1+p1+p1"
  print hex(p3.sum(p1).x)
  print hex(p3.sum(p1).y)

  print "4*p1"
  print hex(p1.multiplyPointByScalar(4).x)
  print hex(p1.multiplyPointByScalar(4).y)

  print "5*p1"
  print hex(p1.multiplyPointByScalar(5).x)
  print hex(p1.multiplyPointByScalar(5).y)

  print "6*p1"
  print hex(p1.multiplyPointByScalar(6).x)
  print hex(p1.multiplyPointByScalar(6).y)

  print "7*p1"
  print hex(p1.multiplyPointByScalar(7).x)
  print hex(p1.multiplyPointByScalar(7).y)


if __name__ == "__main__":
    main()
