from ROOT import gROOT, TCanvas, TF1, TMath
import time
import math
 
gROOT.Reset()
c1 = TCanvas( 'c1', 'Example with Formula', 200, 10, 700, 500 )
 
#
# Create a one dimensional function and draw it
#

#def myFunc(x):
#    y = math.sin(x)
#    return y

#c = 1.5
#fun1 = TF1( 'fun1', 'abs(sin(x)/x) + [0]*x', 0, 10 )
#funX = TF1( 'funX', 'cos( ( x / [0]) )*cos( ( x / [0]) )', 0, 10 )
fun5 = TF1( 'fun5', 'cos( TMath::ATan( x / [0]) )*cos( TMath::ATan( x / [0]) )', 0, 100 )
fun10 = TF1( 'fun10', 'cos( TMath::ATan( x / [0]) )*cos( TMath::ATan( x / [0]) )', 0, 100 )
fun50 = TF1( 'fun50', 'cos( TMath::ATan( x / [0]) )*cos( TMath::ATan( x / [0]) )', 0, 100 )
#funZ = TF1( 'funZ', 'TMath::ATan(x)', 0, 10 )
#fun2 = TF1( 'fun2', 'abs(cos(x)/x)', 0, 10 )
#fun1 = TF1( 'fun1', 'myFunc(x)', 0, 10 )
fun5.SetParameter(0, 5)
fun10.SetParameter(0, 10)
fun50.SetParameter(0, 50)
c1.SetGridx()
c1.SetGridy()
fun5.Draw()
fun10.Draw('same')
fun50.Draw('same')
#fun2.Draw('same')
c1.Update()
time.sleep(3)
