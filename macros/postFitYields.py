#!/usr/bin/env python
#from ROOT import gROOT
# Tyler Ruggles
# 14 March 2015
# A function to return a dictionary of samples and their normalizations split by channel 

import ROOT

def getNormalization(cardsDir, mass=300):
        
    variable = "A_SVfitMass"
    title = ['Channel', 'Sample', 'Pre-Yield', 'Post-Yield', 'Pre/Post', 'Post/Pre']
    pre = ROOT.TFile("%s/shapes.root" % cardsDir, "r")
    ofile = open("PFCards/Normalization.txt", 'w')
    ofile.write("%12s %12s %14s %14s %14s %14s\n" % (title[0], title[1], title[2], title[3], title[4], title[5] ) )
    AllChannels = ['mmtt', 'eett', 'mmmt', 'eemt', 'mmet', 'eeet', 'mmme', 'eeem']
    
    normalization = {}
    for sample in ['ZH_ww125', 'ZH_tt125', 'TTZ', 'GGToZZ2L2L', 'ZZ', 'Zjets', 'ZZZ', 'WZZ', 'WWZ']:
    #    print sample
        inc = 0
        for channel in AllChannels:
    #        print channel
            sampAndChan = '%s_%s' % (sample, channel)
            writer = '%12s %12s' % (sample, channel)
            preHist = pre.Get("%s_zh/%s" % (channel, sample) )
            preInt = round( preHist.Integral(), 5)
    
            post = ROOT.TFile("%s/%s/%s/mlfit.root" % (cardsDir, channel, mass), "r")
            postHist = post.Get("shapes_fit_s/%s_zh/%s" % (channel, sample) )
            if postHist == None:
                postInt = 0
            else:
                postInt = round(postHist.Integral(), 5)
            if postInt > 0:
                preOverPost = round(preInt / postInt, 5)
                postOverPre = round( postInt / preInt, 5)
            else:
                preOverPost = "NAN"
                postOverPre = "NAN"
            ofile.write( "%s %14s %14s %14s %14s\n" % (writer, preInt, postInt, preOverPost, postOverPre) )
            normalization['%s' % sampAndChan] = [preInt, postInt, preOverPost, postOverPre]
    ofile.close()
    return normalization
