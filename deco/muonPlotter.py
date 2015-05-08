import os
from ROOT import gROOT, gStyle
import ROOT
from array import array

nBins = 50
nMax = 100

mapper = { 'HTC_A510' : ('1', '2'),
           'SPH-D710VMUB' : ('1', 'small'),
           'RAZR' : ('1', '2', '3', '4'),
           #'SAMSUNG-SGH' : ('1')
}

for key in mapper.keys():
  print key

  #Set bin widths and max bins for each cell phone
  #if 'HTC' in key:
  #  nBins = 7
  #  nMax = array( 'f', [0,10,20,30,40,60,80,100] )
  #if 'SPH' in key:
  #  nBins = 5
  #  nMax = array( 'f', [0,10,20,30,50,70] )
  #if 'RAZR' in key:
  #  nBins = 10
  #  nMax = array( 'f', [0,2.5,5,7.5,10,12.5,15,20,25,30,40] )
  if 'HTC' in key:
    nBins = 10
    nMax = 100
    lenMax = 30
  if 'SPH' in key:
    nBins = 10
    nMax = 70
    lenMax = 30
  if 'RAZR' in key:
    nBins = 10
    nMax = 40 
    lenMax = 20

  ofile = open('muons_%s.txt' % key, 'w')
  ofile.write('Image : Eccentricites : Len1 : Len 2\n')
  lHistAll = ROOT.TH1F('%slength1' % key, '%s, Length of Muon Tracks, ecc = All' % key, nBins, 0, nMax)
  lHist90 = ROOT.TH1F('%slength2' % key, '%s, Length of Muon Tracks, ecc > 0.9' % key, nBins, 0, nMax)
  lHist95 = ROOT.TH1F('%slength3' % key, '%s, Length of Muon Tracks, ecc > 0.95' % key, nBins, 0, nMax)
  lHist99 = ROOT.TH1F('%slength4' % key, '%s, Length of Muon Tracks, ecc > 0.99' % key, nBins, 0, nMax)
  lenVsEcc = ROOT.TH2I('lenVsEcc', 'Length vs. Eccentricity', 100, 0.0, lenMax, 100, 0, 1)
  lenVsEcc2 = ROOT.TH2I('lenVsEcc2', 'Length vs. Eccentricity2', 100, 0.0, lenMax, 100, 0.5, 1)
  #lHistAll = ROOT.TH1F('%slength1' % key, '%s, Length of Muon Tracks, ecc = All' % key, nBins, nMax)
  #lHist90 = ROOT.TH1F('%slength2' % key, '%s, Length of Muon Tracks, ecc > 0.9' % key, nBins, nMax)
  #lHist95 = ROOT.TH1F('%slength3' % key, '%s, Length of Muon Tracks, ecc > 0.95' % key, nBins, nMax)
  #lHist99 = ROOT.TH1F('%slength4' % key, '%s, Length of Muon Tracks, ecc > 0.99' % key, nBins, nMax)

  #print len(mapper[key])
  for i in mapper[key]:
    #print mapper[key]
    print i
    name = '%s%s' % (key, i)
    #print name
    ifile = open('%s_log.out' % name, 'r')
    
    for line in ifile:
        if 'majA' not in line: continue
        info = line.split(' ')
        #print info
        fst = str( info[0] )[0]
        ecc = float( info[12] )
        l1 = float( info[18] )
        l2 = float( info[21] )
        area = float( info[15] )
        majA = float( info[3] )
        minA = float( info[6] )
        #print "majA: %f minA: %f area: %f" % (majA, minA, area)
        ofile.write('%10s %10f %10f %10f' % (info[0], ecc, l1, l2) )
        #if l1 > l2: len = l1
        #else: len = l2
        len_ = l2

        # Give me some info on the low length high ecc events
#        if len_ < 10 and ecc > 0.99:
#            print "Evt: %s, Len: %f, Ecc: %f" % (str(info[0]), len_, ecc)
        # Always fill the length vs eccentricity plot
        lenVsEcc.Fill( len_, ecc)
        lenVsEcc2.Fill( len_, ecc)
 
        # Does the candidate pass the lower eccentricity / vertical candadate cut?
        passing = False
#        if 'SPH' in key and mapper[key][1] == 'small':
#            print "%f, %f" % (len_, ecc)
        if ecc > 0.9:
            if area < 30:
                if l1 / l2 < 3: passing = True

        lHistAll.Fill( len_ )
        if float( ecc ) > 0.99 or passing:
            lHist99.Fill( len_ )
        if float( ecc ) > 0.95 or passing:
            lHist95.Fill( len_ )
        if float( ecc ) > 0.90:
            lHist90.Fill( len_ )

  # Fitting now
#  def myfunc( x ):
#    scale = 1
#    depth = 10
#    return (scale * cos( TMath.ATan( x / depth ) )**2 )

    
  ofile.close()
  
  c1 = ROOT.TCanvas("c1","title",1200,400)
  c1.Divide(4,1)
  c1.cd(1)
  pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
  pad1.Draw()
  pad1.Close()
  lHistAll.Draw('hist e1')
  c1.cd(2)
  pad2 = ROOT.TPad("pad2", "", 0, 0, 1, 1)
  pad2.Draw()
  pad2.Close()
  lHist90.Draw('hist e1')
  c1.cd(3)
  pad3 = ROOT.TPad("pad3", "", 0, 0, 1, 1)
  pad3.Draw()
  pad3.Close()
  lHist95.Draw('hist e1')
  c1.cd(4)
  pad4 = ROOT.TPad("pad4", "", 0, 0, 1, 1)
  pad4.Draw()
  pad4.Close()
  lHist99.Draw('hist e1')  

  c1.SaveAs('muonsPlot_%s.png' % key)
  c1.Close()
  c2 = ROOT.TCanvas("c1","title",600,600)
  lHist99.Draw('hist e1')
  if not 'SPH' in key:
    lHist99.SetBinContent(1, 0)
    lHist99.SetBinError(1, 0)
#  lHist99.SetBinContent(2, 0)
#  lHist99.SetBinError(2, 0)
#  lHist99.SetMaximum( lHist99.GetMaximum() * 10)

  funx = ROOT.TF1( 'funx', '[0]*cos( TMath::ATan( x / [1]) )*cos( TMath::ATan( x / [1]) )', 0, 100 )
  f1 = gROOT.GetFunction('funx')
  f1.SetParName( 0, "vert count" )
  f1.SetParName( 1, "depth" )
  f1.SetParameter( 0, 999 )
  f1.SetParameter( 1, 999 )
  lHist99.Fit('funx')
  fitResult = lHist99.GetFunction("funx")
  fitResult.Draw('same')
  c2.Update()
  c2.SaveAs('finalFit%s.png' % key)
  c2.Close()

  c3 = ROOT.TCanvas("c3","title",1000,500)
  c3.Divide(2,1)
  c3.cd(1)
  lenVsEcc.Draw('COLZ')
  c3.cd(2)
  lenVsEcc2.Draw('COLZ')
  gStyle.SetOptStat( 0 )
  c3.SaveAs('lenVsEcc_%s.png' % key)
  c3.Close()

  gROOT.cd()







