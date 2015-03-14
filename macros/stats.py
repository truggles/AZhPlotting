''' Tyler Ruggles
    13 March 2015
    Useful statistical tools '''


def ChiSqProb( ChiSq_, n_ ):
  import math
  from scipy import special
  from scipy.integrate import quad
  n = n_
  ChiSq = ChiSq_
  def integrand(x):
    return ( 2**(-n/2) * math.sqrt( x )**(n - 2) * math.exp( -x / 2 ) ) / special.gamma( n / 2 )

  ans, err = quad(integrand, ChiSq, 1000)
  return ans

#print ChiSqProb( 41.38, 28 ) 
