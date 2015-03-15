''' Tyler Ruggles
    13 March 2015
    Useful statistical tools '''


#    Return the Chi Squared Probability for a given Chi Squared 
#    value 'ChiSq_' and a number of samples 'n_'
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

#    Set us up to run a KS test AND Chi Squared test on mvamet
#    if KSTest_ and (run_map[key][i][0] == 'mva_metEt'):
def runKSandChiSqTest(variable, data, mcHists, varBin, varRange, numBins, KSRebin): 
    import ROOT
    import pyplotter.plot_functions as plotter
    import math
#    from macros.stats import ChiSqProb
    print "Starting a KS routine on variable %s" % variable
    ksTester = ROOT.TH1F("ksTester", "ksTester, mva metEt", varBin+1, 0, varRange+varRange/varBin )
    ksTestMC = ROOT.TH1F("ksTester mc", "MC CDF", varBin+1, 0, varRange+varRange/varBin)
    ksTestData = ROOT.TH1F("ksTester data", "Data CDF", varBin+1, 0, varRange+varRange/varBin)
    ks_dataT = 0
    ks_mcT = 0
    for kkk in range (1, numBins +2):
        ks_dataT += data.GetBinContent(kkk)
        ks_mcT += mcHists.GetStack().Last().GetBinContent(kkk)
    print "total mc: %f total data: %f" % (ks_mcT, ks_dataT)
    ChiSq = 0
    ks_data = 0
    ks_mc = 0
    maxDiff = 0
    for jjj in range (1, numBins +2):
        dataNum = data.GetBinContent(jjj)
        mcNum = mcHists.GetStack().Last().GetBinContent(jjj)
        ks_mc += (mcNum/ks_mcT)
        ks_data += (dataNum/ks_dataT)
        ksTestMC.SetBinContent(jjj, ks_mc)
        ksTestData.SetBinContent(jjj, ks_data)
        ChiSq += (dataNum - mcNum)**2 / mcNum
        if (math.fabs( ks_mc - ks_data ) > maxDiff):
            maxDiff = math.fabs( ks_mc - ks_data )
        print "bin : %i mc: %f data: %f MaxDiff: %f" % (jjj, ks_mc, ks_data, maxDiff)
    print "D = %f" % maxDiff
    print "D*SQRT(N) = %f * %f = %f" % (maxDiff, math.sqrt(ks_dataT), maxDiff * math.sqrt(ks_dataT))
    zKS = ( math.sqrt( ks_dataT ) + 0.12 + ( 0.11/math.sqrt( ks_dataT ) ) ) * maxDiff
    print "Z = %f" % zKS
    print "Chi Squared = %f" % ChiSq
    Q_ks = 0
    qqq = 1
    keepGoing = True
    while keepGoing:
        Q_ks += 2 * ( (-1)**(qqq - 1) ) * math.exp( -2*qqq*qqq*zKS*zKS )
        print "qqq: %i Q_ks: %f" % (qqq, Q_ks)
        qqq += 1
        if qqq > 5 and Q_ks < 1: keepGoing = False
    ksTestMC.SetMinimum( 0 )
    ksTestData.SetMinimum( 0 )
    c7 = plotter.getCanvas() # Use Kenneth's canvas setup
    pad7 = ROOT.TPad("pad7","",0,0,1,1) # compare distributions
    pad7.Draw()
    pad7.SetGridy(1)
    pad7.cd()
    #ksTestMC.SetTitle("K-S Test CDFs of MC & Data;%s (GeV)" % (variable) )
    ksTestMC.SetLineColor( ROOT.kRed )
    ksTestData.SetLineColor( ROOT.kBlue )
    ksTestMC.Draw("hist")
    ksTestData.Draw("hist same")
    ROOT.gPad.Update()
    leg = pad7.BuildLegend(0.60, 0.50, 0.93, 0.58)
    leg.SetMargin(0.3)
    #leg.SetFillColor(0)
    #leg.SetBorderSize(0)
    leg.Draw()
    ksTestMC.GetXaxis().SetTitle("%s (GeV)" % (variable))
    pad7.SetTitle("xxx")
    txt = ROOT.TText(.9, 1.07, "CMS Preliminary, K-S Test CDFs of MC & Data" )
    txt.SetTextSize(.04)
    txt.Draw()
    txtB = ROOT.TPaveText(150, 0.19, 300, .45)
    txtB.AddText("KS & ChiSq Statistics Summary:")
    txtB.AddText("N = %i" % ks_dataT)
    txtB.AddText("D = %f" % maxDiff)
    txtB.AddText("Z = %f" % zKS)
    txtB.AddText("p Value = %f" % Q_ks)
    txtB.AddText("Chi Squared = %f" % ChiSq)
    ChiProb = ChiSqProb( ChiSq, ks_dataT )
    print "Chi Squared Probability = %f" % ChiProb
    txtB.AddText("Chi Squared Probability = %f" % ChiProb )
    txtB.Draw()
    ROOT.gPad.Update()
    fileNameKS = "KS_%s_N_%i_Bin_%i" % (variable, ks_dataT, 5*KSRebin)
    c7.SaveAs("plots/KS-Testing/%s.png" % fileNameKS)
    c7.Close()
