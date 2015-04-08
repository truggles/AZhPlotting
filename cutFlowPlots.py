#!/usr/bin/env python
import ROOT
import pyplotter.plot_functions as plotter
from ROOT import gROOT
from ROOT import gStyle

scale = 15
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
    'data' : ('xxx', 'xxx', 999, 999) 
    }

dataEEevents = 12964286 + 23571931 + 33843769 + 34526899
dataMMevents = 5636274 + 38006513 + 36820243 + 29308627
print dataEEevents + dataMMevents


dataMap = {'EE' : ('data_DoubleElectron_Run2012A_22Jan2013_v1.root',
               'data_DoubleElectron_Run2012B_22Jan2013_v1.root',
               'data_DoubleElectron_Run2012C_22Jan2013_v1.root',
               'data_DoubleElectron_Run2012D_22Jan2013_v1.root',),
       'MM' : ('data_DoubleMu_Run2012A_22Jan2013_v1.root',
               'data_DoubleMuParked_Run2012B_22Jan2013_v1.root',
               'data_DoubleMuParked_Run2012C_22Jan2013_v1.root',
               'data_DoubleMuParked_Run2012D_22Jan2013_v1.root')}

order = ['data', 'ZZZ', 'WZZ', 'WWZ', 'ZH_ww125', 'ZH_tt125', 'TTZ', 'GGToZZ2L2L', 'ZZ', 'A300']

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

channels = ['MMEM']#, 'MMMT', 'MMET', 'MMTT', 'EEET', 'EEMT', 'EEEM', 'EETT']


masterStack = ROOT.THStack("Master Cut Flow", "Combined Cut Flow for all MC samples")
masterA300 = ROOT.THStack("A300", "Total for A300")
masterData = ROOT.THStack("data", "Total for Data")
for sampName in order:
    print sampName
    sampStack = ROOT.THStack("%s" % sampName, "%s" % sampName)
    #bin2total = 0
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
            #cutFlowHist.SetBinContent( 1, sampMap[sampName][3] )
            #cutFlowHist.Scale( cmsLumi / sampMap[sampName][2] )
        else:
            ifile1n = "ZHAnalyze%s/%s" % (channel, dataMap[ channel[:2:] ][0])
            ifile1 = ROOT.TFile( ifile1n, "READ")
            cutFlowHist1 = ifile1.Get("os/All_Passed/cutFlow")
            ifile2n = "ZHAnalyze%s/%s" % (channel, dataMap[ channel[:2:] ][1])
            ifile2 = ROOT.TFile( ifile2n, "READ")
            cutFlowHist2 = ifile2.Get("os/All_Passed/cutFlow")
            ifile3n = "ZHAnalyze%s/%s" % (channel, dataMap[ channel[:2:] ][2])
            ifile3 = ROOT.TFile( ifile3n, "READ")
            cutFlowHist3 = ifile3.Get("os/All_Passed/cutFlow")
            ifile4n = "ZHAnalyze%s/%s" % (channel, dataMap[ channel[:2:] ][3])
            ifile4 = ROOT.TFile( ifile4n, "READ")
            cutFlowHist4 = ifile4.Get("os/All_Passed/cutFlow")
            cutFlowHistX = ROOT.THStack()
            cutFlowHistX.Add( cutFlowHist1 )
            cutFlowHistX.Add( cutFlowHist2 )
            cutFlowHistX.Add( cutFlowHist3 )
            cutFlowHistX.Add( cutFlowHist4 )
            cutFlowHist = ROOT.TH1F()
            cutFlowHist = cutFlowHistX.GetStack().Last().Clone()
            #print eval( "data%sevents" % channel[:2:] )
            #bin2total += cutFlowHist.GetStack().Last().GetBinContent(2)
        cutFlowHist.Draw("%s_%s" % (sampName, channel) )
        #bin2total += cutFlowHist.GetBinContent(2)
        cutFlowHist.SetLabelSize(0.02)
        cutFlowHist.SetLabelOffset( 0.01 )
        for i in range( 1, 12 ):
            cutFlowHist.GetXaxis().SetBinLabel( i, binMap[i-1] )
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
        sampStack.Add( cutFlowHist.Clone() )
    #print "Bin 2 total %f" % bin2total
    c5 = plotter.getCanvas() # Use Kenneth's canvas setup
    pad5 = ROOT.TPad("pad5","",0,0,1,1)
    pad5.Draw()
    pad5.SetGridy(1)
    pad5.SetLogy()
    pad5.cd()
    temp = sampStack.GetStack().Last().Clone()
    temp.SetTitle("%s" % sampName)
    #sampStack.GetStack().Last().Draw('hist')
    temp.Draw('hist same')
    if sampName == 'A300':
        temp.SetBinContent( 1, sampMap[sampName][3] )
        temp.Scale( cmsLumi / sampMap[sampName][2] )#* scale )
    elif sampName == 'data':
        temp.SetBinContent( 1, dataMMevents )#dataEEevents + dataMMevents )
    else:
        temp.SetBinContent( 1, sampMap[sampName][3] )
        temp.Scale( cmsLumi / sampMap[sampName][2] )
    c5.SaveAs("cutFlow%s.png" % sampName)
    pad5.Close()
    c5.Close()
    gROOT.cd()
    if sampName == 'A300':
        masterA300.Add( temp, 'hist same' )
    elif sampName == 'data':
        masterData.Add( temp, 'hist same' )
    else:
        masterStack.Add( temp, 'hist same' )

c9 = plotter.getCanvas() # Use Kenneth's canvas setup
pad9 = ROOT.TPad("pad9","",0,0,1,1)
pad9.Draw()
pad9.SetGridy(1)
pad9.SetLogy()
pad9.cd()
masterData.Draw('e2')
masterStack.Draw('hist same')
masterA300.Draw('same')
masterData.GetYaxis().SetTitle("Expected Events per Category")
dataMin = masterData.GetStack()[0].GetBinContent( 11 )
stackMin = masterStack.GetStack().Last().GetBinContent( 11 )
A300Min = masterA300.GetStack().Last().GetBinContent( 11 )
minVal = min( dataMin, stackMin, A300Min )
masterData.SetMinimum( minVal * 0.5 )

''' Build the legend explicitly so we can specify marker styles '''
legend = ROOT.TLegend(0.72, 0.55, 0.93, 0.89)
legend.SetMargin(0.3)
legend.SetBorderSize(0)
legend.AddEntry( masterData, "Data", "lep")
legend.AddEntry( masterA300, "A300", 'l')
for j in range(0, masterStack.GetStack().GetLast() + 1):
    last = masterStack.GetStack().GetLast()
    legend.AddEntry( masterStack.GetStack()[ last - j], masterStack.GetStack()[last - j].GetTitle(), 'f')
legend.Draw()
#plotter.printLumi(c9, 19.7, 8, "left") 
masterData.SetTitle("Cut Flow showing signal selection progression")
ROOT.gStyle.SetTitleOffset(1.15, "x")
ROOT.gPad.Modified()
ROOT.gPad.Update()

c9.SaveAs("cutFlow.png")






