from ROOT import gROOT, TCanvas, TF1, TMath
import ROOT
import time
import math
 
gROOT.Reset()
c1 = TCanvas( 'c1', 'Example with Formula', 200, 10, 700, 500 )
 
fun5 = TF1( 'fun5', 'cos( TMath::ATan( x / [0]) )*cos( TMath::ATan( x / [0]) )', 0, 100 )
fun10 = TF1( 'fun10', 'cos( TMath::ATan( x / [0]) )*cos( TMath::ATan( x / [0]) )', 0, 100 )
fun50 = TF1( 'fun50', 'cos( TMath::ATan( x / [0]) )*cos( TMath::ATan( x / [0]) )', 0, 100 )

fun5.SetParameter(0, 5)
fun10.SetParameter(0, 10)
fun50.SetParameter(0, 50)

c1.SetGridx()
c1.SetGridy()
fun5.Draw()
fun10.Draw('same')
fun50.Draw('same')
c1.Update()
c1.SaveAs("initial_draw.png")
c1.Close()

c2 = TCanvas( 'c2', 'Example with Formula', 200, 10, 700, 500 )
c2.SetGridx()
c2.SetGridy()

hist = ROOT.TH1F('h1','test', 100, 0 ,100)
hist.FillRandom('fun5',20000)
hist.Draw()
f1 = gROOT.GetFunction('fun5')
f1.SetParameter( 0, 800 )
hist.Fit('fun5')
c2.Update()


time.sleep(3)
