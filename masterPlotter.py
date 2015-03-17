#!/usr/bin/env python
from ROOT import gROOT
from ROOT import gStyle
from ROOT import TGraphErrors
import ROOT
import os
import pyplotter.plot_functions as plotter
import math
import numpy
from macros.postFitYields import getNormalization
from macros.stats import runKSandChiSqTest

#AZhSample = 'AZh350'
AZhSample = 'AZh300'

#Cards = 'Official'
#Cards = 'hSVFit'
#Cards = 'Current'
#KSTest = False
#KSTest = True
KSRebin = 12
blind = False
#blind = True
A300Scaling = 15
ROOT.gROOT.SetBatch(True)
txtLabel = True

products_map = {'mmtt' : ('m1', 'm2', 't1', 't2'), 
                'eett' : ('e1', 'e2', 't1', 't2'),
                'mmmt' : ('m1', 'm2', 'm3', 't'),
                'eemt' : ('e1', 'e2', 'm', 't'),
                'mmet' : ('m1', 'm2', 'e', 't'),
                'eeet' : ('e1', 'e2', 'e3', 't'),
                'mmme' : ('m1', 'm2', 'e', 'm3'),
                'eeem' : ('e1', 'e2', 'e3', 'm')
}
# maps sample to marker color and marker fill style
#samples = { 'TTZ' : ("kGreen-7", "kCyan-2", 21),
#            'ZH_ww125' : ("kRed-7", "kYellow-2", 21),
#            'ZH_tt125' : ("kMagenta-7", "kMagenta-2", 21),
#            'ZZ' : ("kBlue-7", "kGreen+2", 21),
#            'ZZZ' : ("kOrange+9", "kGreen+2", 21),
#            'WZZ' : ("kOrange+7", "kGreen+2", 21),
#            'WWZ' : ("kOrange+2", "kGreen+2", 21),
#            'GGToZZ2L2L' : ("kCyan-7", "kRed-2", 21), 
#            'Zjets' : ("kYellow-7", "kMagenta+1", 21),
#            AZhSample : ("kBlue", "kBlue", 21),
#            'data_obs' : ("","")
#}
samples = { 'Zjets' : ("kCyan+1", "kMagenta+1", 21),
            'ZZ' : ("kGreen+1", "kGreen+2", 21),
            'WWZ' : ("kRed+1", "kGreen+2", 21),
            'WZZ' : ("kBlue+1", "kGreen+2", 21),
            'ZZZ' : ("kYellow", "kGreen+2", 21),
            'GGToZZ2L2L' : ("kMagenta+1", "kRed-2", 21), 
            'TTZ' : ("kTeal+1", "kCyan-2", 21),
            'ZH_tt125' : ("kPink+9", "kMagenta-2", 21),
            'ZH_ww125' : ("kOrange", "kYellow-2", 21),
            AZhSample : ("kBlue", "kBlue", 21),
            'data_obs' : ("","")
}

#variables = ['Pt','Mass','DR','LT_Higgs','mva_metEt','A_SVfitMass','SVfitMass']

AllChannels = ['mmtt', 'eett', 'mmmt', 'eemt', 'mmet', 'eeet', 'mmme', 'eeem']
ZChannelsEE = ['eett', 'eemt', 'eeet', 'eeem']
ZChannelsMM = ['mmtt', 'mmmt', 'mmet', 'mmme']
hChannelsEM = ['eeem', 'mmme']
hChannelsET = ['eeet', 'mmet']
hChannelsMT = ['eemt', 'mmmt']
hChannelsTT = ['eett', 'mmtt']


#            Channel str     Channel List, List for varialbes_map and title for the associated histo
run_map = { "AllChannels" : (AllChannels, ('Mass', 'Visible Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('Mass', 'Visible Mass_{#tau^{+}#tau^{-}}', 'h'),
                                          ('Mass', 'Mass_{l^{+}l^{-}}', 'z'),
                                          ('LT_Higgs', 'L_{T} #tau_{1} #tau_{2}', 'all'),
                                          ('mva_metEt', 'mva metEt', 'all'),
                                          ('A_SVfitMass', 'Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('SVfitMass', 'Mass_{#tau^{+}#tau^{-}}', 'h'),
                                          ('Pt', '#tau_{1} P_{T}', 2),
                                          ('Pt', '#tau_{2} P_{T}', 3),
                                          ('Pt', 'Lepton_{1} P_{T}', 0),
                                          ('Pt', 'Lepton_{2} P_{T}', 1),
                                          ('Pt', 'Vector Sum P_{T}_{#tau^{+}#tau^{-}}', 'h'),
                                          ('Pt', '#Sigma #vec{P_{T}} l^{+}l^{-}', 'z'), ),
            "ZChannelsEE" : (ZChannelsEE, ('Mass', 'Visible Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('Mass', 'Mass_{l^{+}l^{-}}', 'z'),
                                          ('mva_metEt', 'mva metEt', 'all'),
                                          ('A_SVfitMass', 'Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('Pt', 'Lepton1 Pt', 0),
                                          ('Pt', 'Lepton2 Pt', 1),
                                          ('Pt', 'Vector Sum Pt_{l^{+}l^{-}}', 'z'), ),
            "ZChannelsMM" : (ZChannelsMM, ('Mass', 'Visible Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('Mass', 'Mass_{l^{+}l^{-}}', 'z'),
                                          ('mva_metEt', 'mva metEt', 'all'),
                                          ('A_SVfitMass', 'Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('Pt', 'Lepton1 Pt', 0),
                                          ('Pt', 'Lepton2 Pt', 1),
                                          ('Pt', 'Vector Sum Pt_{l^{+}l^{-}}', 'z'), ),
            "hChannelsEM" : (hChannelsEM, ('Mass', 'Visible Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('Mass', 'Visible Mass_{#tau^{+}#tau^{-}}', 'h'),
                                          ('LT_Higgs', 'L_{T} #tau1 #tau2', 'all'),
                                          ('mva_metEt', 'mva metEt', 'all'),
                                          ('A_SVfitMass', 'Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('SVfitMass', 'Mass_{#tau^{+}#tau^{-}}', 'h'),
                                          ('Pt', '#tau1 Pt', 2),
                                          ('Pt', '#tau2 Pt', 3),
                                          ('Pt', 'Vector Sum Pt_{#tau^{+}#tau^{-}}', 'h'), ),
            "hChannelsET" : (hChannelsET, ('Mass', 'Visible Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('Mass', 'Visible Mass_{#tau^{+}#tau^{-}}', 'h'),
                                          ('LT_Higgs', 'L_{T} #tau1 #tau2', 'all'),
                                          ('mva_metEt', 'mva metEt', 'all'),
                                          ('A_SVfitMass', 'Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('SVfitMass', 'Mass_{#tau^{+}#tau^{-}}', 'h'),
                                          ('Pt', '#tau1 Pt', 2),
                                          ('Pt', '#tau2 Pt', 3),
                                          ('Pt', 'Vector Sum Pt_{#tau^{+}#tau^{-}}', 'h'), ),
            "hChannelsMT" : (hChannelsMT, ('Mass', 'Visible Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('Mass', 'Visible Mass_{#tau^{+}#tau^{-}}', 'h'),
                                          ('LT_Higgs', 'L_{T} #tau1 #tau2', 'all'),
                                          ('mva_metEt', 'mva metEt', 'all'),
                                          ('A_SVfitMass', 'Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('SVfitMass', 'Mass_{#tau^{+}#tau^{-}}', 'h'),
                                          ('Pt', '#tau1 Pt', 2),
                                          ('Pt', '#tau2 Pt', 3),
                                          ('Pt', 'Vector Sum Pt_{#tau^{+}#tau^{-}}', 'h'), ),
            "hChannelsTT" : (hChannelsTT, ('Mass', 'Visible Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('Mass', 'Visible Mass_{#tau^{+}#tau^{-}}', 'h'),
                                          ('LT_Higgs', 'L_{T} #tau1 #tau2', 'all'),
                                          ('mva_metEt', 'mva metEt', 'all'),
                                          ('A_SVfitMass', 'Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}', 'all'),
                                          ('SVfitMass', 'Mass_{#tau^{+}#tau^{-}}', 'h'),
                                          ('Pt', '#tau1 Pt', 2),
                                          ('Pt', '#tau2 Pt', 3),
                                          ('Pt', 'Vector Sum Pt_{#tau^{+}#tau^{-}}', 'h'), ),
}

def makePlots(ChanKey_ = 'AllChannels', PostFit_=False, KSTest_=False, KSRebin_=4, Cards_='Official', **normMap):
  runSummary = "Run Summary:\n\tChannels = %s\n\tPost Fit = %r\n\tKSTest = %r\n\tKSRebin = %i\n\tCards = %s" % (ChanKey_, PostFit_, KSTest_, KSRebin_, Cards_)
  print runSummary
  print chan_map['%s' % ChanKey_]
  print "\n"
  #print normMap
  variables_map = {'LT_Higgs' : (10, 200, "L_{T} #tau1 #tau2", "(GeV)", "x"),
                   'Mass' : (20, 800, "Visible Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}", "(GeV)", "x"),
                   'mva_metEt' : (60/KSRebin_, 300, "mva metEt", "(GeV)", "x"),
                   'A_SVfitMass' : (20, 800, "Mass_{l^{+}l^{-}#tau^{+}#tau^{-}}", "(GeV)", "x"),
                   'SVfitMass' : (15, 300, "#tau1 #tau2 Mass", "(GeV)", "h"),
                   'DR' : (20, 10, "dR of lepton1 lepton2", "radians", "z"),
                   'Pt' : (15, 300, "temp", "(GeV)", 0)}

  for key in run_map.keys():
      if key == "AllChannels": pass
      else: break
      #print key
      nPlots = len( run_map[key] )
      for i in range(1, nPlots):
          variable = run_map[key][i][0]
          print "%s %s" % (variable, run_map[key][i][2]) 
          if KSTest_ and not variable == "mva_metEt": continue
          else: pass 
#          if not (variable == 'A_SVfitMass'): continue # or variable == 'Mass'): continue
          if variable == 'Mass' and run_map[key][i][2] == 'h':
              varRange = 300
              varBin = 10
          elif variable == 'Mass' and run_map[key][i][2] != 'all':
              varRange = 300
              varBin = 30
          else:
              varRange = variables_map[variable][1]
              varBin = variables_map[variable][0]
          #print "varRange %i varBin %i" % (varRange, varBin)
          my_total = ROOT.THStack("my_total", "CMS Preliminary, Red + Irr bgk & Data, 19.7 fb^{-1} at S=#sqrt{8} TeV")
          if Cards_ == 'Official':
            my_shapes = ROOT.TFile("cardsOfficial/shapes.root", "r")
          elif Cards_ == 'hSVFit':
            my_shapes = ROOT.TFile("cardshSVFit/shapes.root", "r")
          elif Cards_ == 'Current':
            my_shapes = ROOT.TFile("cards/shapes.root", "r")
          my_data = ROOT.TH1F("my_data", "Data", varBin, 0, varRange)
          my_ZH_ww125 = ROOT.TH1F("my_ZH_ww125", "ZH_ww125", varBin, 0, varRange)
          my_ZH_tt125 = ROOT.TH1F("my_ZH_tt125", "ZH_tt125", varBin, 0, varRange)
          my_TTZ = ROOT.TH1F("my_TTZ", "TTZ", varBin, 0, varRange)
          my_GGToZZ2L2L = ROOT.TH1F("my_GGToZZ2L2L", "GGToZZ2L2L", varBin, 0, varRange)
          my_ZZ = ROOT.TH1F("my_ZZ", "ZZ", varBin, 0, varRange)
          my_ZZZ = ROOT.TH1F("my_ZZZ", "ZZZ", varBin, 0, varRange)
          my_WZZ = ROOT.TH1F("my_WZZ", "WZZ", varBin, 0, varRange)
          my_WWZ = ROOT.TH1F("my_WWZ", "WWZ", varBin, 0, varRange)
          my_Zjets = ROOT.TH1F("my_Zjets", "Zjets", varBin, 0, varRange)
          my_A300 = ROOT.TH1F("my_A300", "%i x A300, xsec=1fb" % A300Scaling, varBin, 0, varRange)
          
          for sample in ['ZH_ww125', 'ZH_tt125', 'TTZ', 'GGToZZ2L2L', 'ZZZ', 'WZZ', 'WWZ', 'ZZ', 'Zjets', AZhSample, 'data_obs']:
              #print sample
              my_red_combined = ROOT.THStack("%s combined" % sample, "%s combined" % sample)
          
              for channel in chan_map[ChanKey_]:
                  if run_map[key][i][2] == "all":
                      if variable == 'A_SVfitMass': sampVar = sample
                      else: sampVar = sample + "_" + variable
                  elif run_map[key][i][2] == "z":
                      first = products_map[channel][0]
                      second = products_map[channel][1]
                      sampVar = "%s_%s_%s_%s" % (sample, first, second, variable)
                  elif run_map[key][i][2] == "h":
                      first = products_map[channel][2]
                      second = products_map[channel][3]
                      sampVar = "%s_%s_%s_%s" % (sample, first, second, variable)
                  else:
                      first = products_map[channel][ run_map[key][i][2] ]
                      sampVar = "%s_%s%s" % (sample, first, variable)
                  my_red = my_shapes.Get("%s_zh/%s" % (channel, sampVar) )

                  ''' Create the post fit section that scales histos by their
                  maximum likelihood.  From normMap: 0 = preFit, 1 = postFit
                  2 = pre over post, 3 = post over pre '''
                  if PostFit_:
                      if sample == AZhSample or sample == 'data_obs': pass
                      else:
                        #print "%s %s Pre Int: %f" % (sample, channel, my_red.Integral() )
                        #print "Pre from normMap: %f" % normMap['%s_%s' % (sample, channel)][0]
                        scale = normMap['%s_%s' % (sample, channel)][3]
                        #print "scale: %s" % scale
                        if scale == 'NAN':
                            continue
                        scale = float( scale )
                        my_red.Scale( scale ) 
                        #print "Post Int: %f" % my_red.Integral()
                        #print "Post from normMap: %f" % normMap['%s_%s' % (sample, channel)][1]

                  c1 = plotter.getCanvas()
                  pad1 = ROOT.TPad("pad1","",0,0,1,1)
                  pad1.Draw()    
                  pad1.cd() 
                  pad1.SetGrid()
                  #print "sampVar: %s, channel %s" % (sampVar, channel)
                  my_red.Draw("%s_%s" % (sampVar, channel) )
  
                  ''' Rebin for better viewing! '''
                  if run_map[key][i][0] == 'Pt': my_red.Rebin(4)
                  if run_map[key][i][0] == 'mva_metEt': my_red.Rebin( KSRebin_ )
                  if run_map[key][i][0] == 'Mass' and run_map[key][i][2] == 'all': my_red.Rebin(2)
                  #if run_map[key][i][0] == 'Mass' and run_map[key][i][2] == 'h': my_red.Rebin(2)
                  if run_map[key][i][0] == 'SVfitMass' and run_map[key][i][2] == 'h': my_red.Rebin(2)
                  if run_map[key][i][0] == 'A_SVfitMass' and run_map[key][i][2] == 'all': my_red.Rebin(2)
                  if run_map[key][i][0] == 'LT_Higgs': my_red.Rebin(2)
                  if variable == 'Mass' and run_map[key][i][2] == 'h': my_red.Rebin(3)
                  my_red.GetXaxis().SetTitle("%s (GeV), %s" % (variable, channel) )
          
                  pad1.Close()
                  c1.Close()
                  gROOT.cd()
                  new_my_red = my_red.Clone()
                  my_red_combined.Add(new_my_red)
              
              c2 = plotter.getCanvas()
              plotter.setTDRStyle() 
              pad2 = ROOT.TPad("pad2","",0,0.2,1,1)
              pad2.Draw()
              pad2.cd()
              my_red_combined.GetStack().Last().Draw()
  
              ROOT.gStyle.SetTitleOffset(1.15, "x")
              ROOT.gPad.Modified()
              ROOT.gPad.Update()
              pad2.Close()
              c2.Close()
              gROOT.cd()
          
              if sample == 'data_obs':
                  tempHistD = ROOT.TH1F("my_temp_data", "%s" % sample, variables_map[variable][0], 0, variables_map[variable][1])
                  tempHistD = my_red_combined.GetStack().Last().Clone()
                  my_data.Add( tempHistD.Clone() )
                  #print "# of Bins: %i" % my_data.GetSize()
                  #print "Bin Width %i" % my_data.GetBinWidth(1)
                  #print "Max: %i" % ( (my_data.GetSize() - 2) * my_data.GetBinWidth(1) )

                  ''' This is where we blind our data if it is desired.  We only blind A sv Fit Mass and A visible Mass '''
                  if (variable == 'Mass' or variable == 'A_SVfitMass') and not (run_map[key][i][2] == 'h' or run_map[key][i][2] == 'z') and blind:
                      print "Var: %s append %s" % (variable, run_map[key][i][2] )
                      print "We made it to blind section"
                      numBins = my_data.GetSize() - 2
                      print "numBins = %i" % numBins 
                      binWidth = my_data.GetBinWidth(1)
                      print "Bin Width = %i" % binWidth
                      # we will blind 240 - 360 GeV for SVFitMass
                      if variable == 'A_SVfitMass':
                          lowBlind = int(((240/binWidth) + 1)) # +1 b/c of overflow low bin
                          highBlind = int((360/binWidth)) # +1 b/c of overflow low bin
                      # we will blind 160 - 280 GeV for Visible Mass
                      if variable == 'Mass':
                          lowBlind = int(((160/binWidth) + 1)) # +1 b/c of overflow low bin
                          highBlind = int((280/binWidth)) # +1 b/c of overflow low bin
                      print "low: %s, high: %s" % (lowBlind, highBlind)
                      binsToNull = []
                      for j in range (lowBlind, highBlind + 1):
                          binsToNull.append(j)
                      print binsToNull
                      for bin in binsToNull:
                          print "bin: %i" % bin
                          my_data.SetBinError(bin, 0)
                          my_data.SetBinContent(bin, 0)
              if sample == AZhSample:
                  my_A300.Add( my_red_combined.GetStack().Last().Clone() )
                  my_A300.Scale( A300Scaling )
              if sample != 'data_obs' and sample != AZhSample:
                  color = "ROOT.%s" % samples[sample][0]
                  fillColor = "ROOT.%s" % samples[sample][1]
                  my_red_combined.GetStack().Last().SetFillColor( eval(color) )
                  my_red_combined.GetStack().Last().SetLineColor( eval(color) )
                  call = "my_%s.Add ( my_red_combined.GetStack().Last().Clone() )" % sample
                  eval( call )
                  call = "my_%s.SetFillColor( eval(color) )" % sample
                  eval( call )
                  call = "my_%s.SetFillStyle( 1001 )" % sample
                  eval( call )
                  call = "my_%s.Clone()" % sample
                  my_total.Add( eval( call ), "hist" )
          
          c3 = plotter.getCanvas() # Use Kenneth's canvas setup
          pad5 = ROOT.TPad("pad5","",0,0,1,1)
          pad5.Draw()
          pad5.SetGridy(1)
          pad5.cd()

          ''' Error bar work '''
          if PostFit_:
            nBins = my_total.GetStack().Last().GetXaxis().GetNbins()
            binWidth = my_total.GetStack().Last().GetBinWidth( 1 )
            xPos = []
            yPos = []
            for binnn in range( 0, nBins ):
              xPos.append( (binWidth / 2) + (binnn * binWidth) )
            errorX = [binWidth / 2] * nBins
            errorY = []
            for g in range(1, nBins + 1 ):
              binArray = []
              for j in range(0, my_total.GetStack().GetLast() + 1):
                #print "s: %s bin: %i val %f" % (my_total.GetStack()[i], j, my_total.GetStack()[i].GetBinError(j) )
                binArray.append( my_total.GetStack()[j].GetBinError(g) )
                my_total.GetStack()[j].SetBinError(g, 0)
              toRoot = 0
              for k in binArray:
                toRoot += k**2
              my_total.GetStack().Last().SetBinError(g, math.sqrt( toRoot ) )
              my_total.GetStack().Last().SetMarkerSize( 0 )
              errorY.append( math.sqrt( toRoot ) )
              yPos.append( my_total.GetStack().Last().GetBinContent(g) )
            xPos = numpy.array( xPos, dtype='float' ).flatten('C')
            yPos = numpy.array( yPos, dtype='float' ).flatten('C')
            errorX = numpy.array( errorX, dtype='float' ).flatten('C')
            errorY = numpy.array( errorY, dtype='float' ).flatten('C')
            errorPlot = ROOT.TGraphErrors( nBins, xPos, yPos, errorX, errorY)
            errorPlot.SetTitle("Uncert.")
            errorPlot.SetMarkerStyle( 0 )
            errorPlot.SetFillColorAlpha(ROOT.kGray+2, 0.35) 
            my_total.Draw("hist")
            errorPlot.Draw("e2 same")
            pad5.Update()
          else: my_total.Draw("hist")

          my_total.GetYaxis().SetTitle("Events / %i GeV" % (variables_map[variable][1]/variables_map[variable][0]) )
          my_total.GetXaxis().SetTitle("%s %s" % (run_map[key][i][1], variables_map[variable][3]) )
          my_A300.SetLineWidth(2)
          my_A300.SetLineColor(ROOT.kOrange+10)
          #my_A300.SetLineColor(ROOT.kOrange)
          my_A300.Draw("hist same")
  
          ''' Used for calculating Signal / Background, lots of print out
          so it's commented out now days. '''
          numBins = my_A300.GetXaxis().GetNbins()
          #iii_A300 = 0
          #iii_backGrnd = 0
          #iii_data = 0
          #for iii in range (1, numBins + 2):
          #  #print "A300 bin %i: %f" % (iii, my_A300.GetBinContent(iii)/A300Scaling )
          #  #print "Back bin %i: %f" % (iii, my_total.GetStack().Last().GetBinContent(iii) )
          #  A_300 = my_A300.GetBinContent(iii)/A300Scaling
          #  backGrnd = my_total.GetStack().Last().GetBinContent(iii)
          #  data_ = my_data.GetBinContent(iii)
          #  iii_data += data_
          #  iii_A300 += A_300
          #  iii_backGrnd += backGrnd
          #  if backGrnd > 0.0:
          #    print "Bin %2i : %6.4f / %8.4f = %6.4f" % (iii, A_300, backGrnd, 100*A_300/backGrnd )
          #print "Total Signal to Background: %6.4f / %8.4f = %8.4f   ---   data: %i" % (iii_A300, iii_backGrnd, 100*iii_A300/iii_backGrnd, iii_data)
  
          ''' Set maximum considering error bar height on data '''
          cmsLumiScale = 1 # this is to adjust the histo max so that the data doesn't cover the 'CMS Prelim'
          dataMax = my_data.GetMaximum()
          dataMaxBin = my_data.GetMaximumBin()
          if float( dataMaxBin ) < (0.35 * my_data.GetXaxis().GetNbins() ):
              cmsLumiScale = 1.2
          dataError = my_data.GetBinError( dataMaxBin )
          dataMaxPlusError = dataMax + dataError
          bkgMax = my_total.GetMaximum()
          if dataMax > bkgMax:
              my_total.SetMaximum( 1.3 * dataMax )
          else: my_total.SetMaximum( 1.3 * bkgMax )
          if my_total.GetMaximum() < dataMaxPlusError:
              my_total.SetMaximum( dataMaxPlusError * cmsLumiScale )

          my_A300.SetStats(0)
          #print "My Total Int: %f" % my_total.GetStack().Last().Integral()
          my_data.Draw("e1 same")
          my_data.SetMarkerStyle(21)
          my_data.SetMarkerSize(.8)

          ''' Build the legend explicitly so we can specify marker styles '''
          legend = ROOT.TLegend(0.66, 0.55, 0.93, 0.89)
          legend.SetMargin(0.3)
          legend.SetBorderSize(0)
          legend.AddEntry( my_data, "Data", "lep")
          legend.AddEntry( my_A300, "%i x A%s, xsec=1fb" % (A300Scaling, AZhSample[-3::]), 'l')
          for j in range(0, my_total.GetStack().GetLast() + 1):
              last = my_total.GetStack().GetLast()
              legend.AddEntry( my_total.GetStack()[ last - j], my_total.GetStack()[last - j].GetTitle(), 'f')
          legend.AddEntry( errorPlot, errorPlot.GetTitle(), "f") 
          legend.Draw()

          ''' Name our histo something unique with relavent info '''
          postFit = ''
          if PostFit_: postFit = 'pf_'
          fileName = "%s%s_%s_%s" % ( postFit, ChanKey_, run_map[key][i][2], run_map[key][i][0] )
  
          if run_map[key][i][0] == 'Mass':
              my_total.GetXaxis().SetRange(1, 35)
          if run_map[key][i][0] == 'Mass' and run_map[key][i][2] == "z":
              my_total.GetXaxis().SetRange(5, 15)
          if run_map[key][i][0] == 'Mass' and run_map[key][i][2] == 'h':
              my_total.GetXaxis().SetRange(1, 10)
          plotter.printLumi(c3, 19.7, 8, "left") 
  
 #         c3.cd()
 #         if txtLabel:
 #             #txtLow = 5
 #             txtLow = my_data.GetXaxis().GetBinUpEdge(1)
 #             print txtLow
 #             txtChan = ROOT.TText(txtLow, my_data.GetMaximum()*1.2, "Channels: %s" % ChanKey_ )
 #             txtChan.Draw()
 #         c3.Update()

          ''' Adjusts the location of the X axis title,
          this is difficult because you can't accest a THStacks'
          axis titles '''
          ROOT.gStyle.SetTitleOffset(1.15, "x")
          ROOT.gPad.Modified()
          ROOT.gPad.Update()
  
          c3.SaveAs("plots/background/pdf/%s.pdf" % fileName)
          c3.SaveAs("plots/background/root/%s.root" % fileName)
          c3.SaveAs("plots/background/png/%s.png" % fileName)
          if KSTest_:
            c3.SaveAs("plots/KS-Testing/png/%s%s_N_%i_Bin_%i.png" % (postFit, variable, iii_data, 5*KSRebin_))
            c3.SaveAs("plots/KS-Testing/pdf/%s%s_N_%i_Bin_%i.pdf" % (postFit, variable, iii_data, 5*KSRebin_))
#          if run_map[key][i][0] == 'mva_metEt':
#              pad5.SetLogy()
#              if my_data.GetMaximum() > my_total.GetMaximum():
#                my_total.SetMaximum( 15 * my_data.GetMaximum() )
#              else: my_total.SetMaximum( 15 * my_total.GetMaximum() )
#              my_total.SetMinimum( 0.01 )
#              c3.SaveAs("plots/background/%s_log.root" % fileName)
  
          ''' Set us up to run a KS test AND Chi Squared test on mvamet '''
          if KSTest_:
            runKSandChiSqTest( variable, my_data, my_total, varBin, varRange, numBins, KSRebin_)

chan_map = { 'AllChannels' : ('mmtt', 'eett', 'mmmt', 'eemt', 'mmet', 'eeet', 'mmme', 'eeem'),
         'ZChannelsEE' : ('eett', 'eemt', 'eeet', 'eeem'),
         'ZChannelsMM' : ('mmtt', 'mmmt', 'mmet', 'mmme'),
         'hChannelsEM' : ('eeem', 'mmme'),
         'hChannelsET' : ('eeet', 'mmet'),
         'hChannelsMT' : ('eemt', 'mmmt'),
         'hChannelsTT' : ('eett', 'mmtt')}
  
def makeKSandChiSqPlots():
  KSTest = True
  for binning in [1, 2, 3, 4, 6, 12]:
    makePlots( KSTest, binning, 'Official')
    makePlots( KSTest, binning, 'hSVFit')

norm = getNormalization('PFCards/cards', '300')
#print norm.keys()
#chan = ['eeem', 'mmme']
makePlots('ZChannelsMM', True, **norm)
makePlots('AllChannels', True, **norm)
#for combo in chan_map.keys():
#    makePlots( combo , True, **norm)







