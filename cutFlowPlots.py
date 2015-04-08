#!/usr/bin/env python
import ROOT
import pyplotter.plot_functions as plotter
from ROOT import gROOT
from ROOT import gStyle

cmsLumi = 19.7 * 1000

sampMap = { # file name : Fill Color : LumiCalc : Total DAS Events
    'ZH_ww125' : ('VHWW_lepdecay_125.root', 'ROOT.kOrange', 23066277.1029, 150000),
    'ZH_tt125' : ('VH_H2Tau_M-125.root', 'ROOT.kPink+9', 37721614.4851, 100000),
    'TTZ' : ('TTZJets.root', 'ROOT.kTeal+1', 1010384.61538, 210160),
    'GGToZZ2L2L' : ('ggZZ2L2L.root', 'ROOT.kMagenta+1', 33331088.9443, 400973),
    'ZZZ' : ('ZZZ.root', 'ROOT.kYellow', 40691876.2439, 224904),
    'WZZ' : ('WZZ.root', 'ROOT.kBlue+1', 11170477.6423, 219835),
    'WWZ' : ('WWZ.root', 'ROOT.kRed+1', 3834926.66091, 222234),
    'ZZ' : ('ZZJetsTo4L_pythia.root', 'ROOT.kGreen+1', 25710657.754, 4807893),
    'A300' : ('A300-Zh-lltt-MadGraph.root', 'xxx', 496751000.0, 496751), 
    }

dataMap = {'EE' : ('data_DoubleElectron_Run2012A_22Jan2013_v1.root',
               'data_DoubleElectron_Run2012B_22Jan2013_v1.root',
               'data_DoubleElectron_Run2012C_22Jan2013_v1.root',
               'data_DoubleElectron_Run2012D_22Jan2013_v1.root',),
       'MM' : ('data_DoubleMu_Run2012A_22Jan2013_v1.root',
               'data_DoubleMuParked_Run2012B_22Jan2013_v1.root',
               'data_DoubleMuParked_Run2012C_22Jan2013_v1.root',
               'data_DoubleMuParked_Run2012D_22Jan2013_v1.root')}

order = ['ZZZ', 'WZZ', 'WWZ', 'ZH_ww125', 'ZH_tt125', 'TTZ', 'GGToZZ2L2L', 'ZZ', 'A300', 'data']

binMap = {
        0 : 'All Events',
        1 : '4 Leptons',
        2 : 'Z Cuts',
        3 : 't1 Loose',
        4 : 't2 Loose',
        5 : 'dZ, dR',
        6 : 'LT',
        7 : 'Opp. Sign',
        8 : 't1 Tight',
        9 : 't2 Tight',
        10 : 'Passing' }

channels = ['MMMT']#, 'MMET', 'MMEM', 'MMTT', 'EEET', 'EEMT', 'EEEM', 'EETT']


masterStack = ROOT.THStack("Master Cut Flow", "Combined Cut Flow for all MC samples")
masterA300 = ROOT.THStack("A300", "Total for A300")
masterData = ROOT.THStack("data", "Total for Data")
for sampName in order:
    print sampName
    sampStack = ROOT.THStack("%s" % sampName, "%s" % sampName)
    bin2total = 0
    for channel in channels:
        c1 = plotter.getCanvas() # Use Kenneth's canvas setup
        pad1 = ROOT.TPad("pad1","",0,0,1,1)
        pad1.Draw()
        pad1.SetGridy(1)
        pad1.SetLogy()
        pad1.cd()
        #print channel
        if sampName != 'data':
            ifileName = "ZHAnalyze%s/%s" % (channel, sampMap[sampName][0])
            ifile = ROOT.TFile( ifileName, "READ")
            cutFlowHist = ifile.Get("os/All_Passed/cutFlow")
        else:
            ifile1 = "ZHAnalyze%s/%s" % (channel, dataMap[ channel[:2:] ][0])
            ifile2 = "ZHAnalyze%s/%s" % (channel, dataMap[ channel[:2:] ][1])
            ifile3 = "ZHAnalyze%s/%s" % (channel, dataMap[ channel[:2:] ][2])
            ifile4 = "ZHAnalyze%s/%s" % (channel, dataMap[ channel[:2:] ][3])
        bin2total += cutFlowHist.GetBinContent(2)
        cutFlowHist.Draw("%s_%s" % (sampName, channel) )
        cutFlowHist.SetBinContent( 1, sampMap[sampName][3] )
        cutFlowHist.SetLabelSize(0.02)
        cutFlowHist.SetLabelOffset( 0.01 )
        for i in range( 1, 12 ):
            cutFlowHist.GetXaxis().SetBinLabel( i, binMap[i-1][0] )
        cutFlowHist.GetYaxis().SetTitle("Expected Events per Category")
        if sampName != 'data' and sampName != 'A300':
          cutFlowHist.SetFillColor( eval( sampMap[sampName][1] ) )
          cutFlowHist.SetFillStyle( 1001 )
        if sampName == 'A300':
          cutFlowHist.SetLineWidth(5)
          cutFlowHist.SetLineColor(ROOT.kOrange+10)
        pad1.Close()
        c1.Close()
        gROOT.cd()
        cutFlowHist.Scale( cmsLumi / sampMap[sampName][2] )
        sampStack.Add( cutFlowHist.Clone() )
    print "Bin 2 total %f" % bin2total
    c5 = plotter.getCanvas() # Use Kenneth's canvas setup
    pad5 = ROOT.TPad("pad5","",0,0,1,1)
    pad5.Draw()
    pad5.SetGridy(1)
    pad5.SetLogy()
    pad5.cd()
    temp = sampStack.GetStack().Last().Clone()
    #sampStack.GetStack().Last().Draw('hist')
    temp.Draw('hist same')
    c5.SaveAs("cutFlow%s.png" % sampName)
    pad5.Close()
    c5.Close()
    gROOT.cd()
    if sampName == 'A300':
        masterA300.Add( temp, 'hist same' )
    else:
        masterStack.Add( temp, 'hist same' )

c9 = plotter.getCanvas() # Use Kenneth's canvas setup
pad9 = ROOT.TPad("pad9","",0,0,1,1)
pad9.Draw()
pad9.SetGridy(1)
pad9.SetLogy()
pad9.cd()
masterStack.Draw('hist')
masterA300.Draw('same')
c9.SaveAs("cutFlow.png")






