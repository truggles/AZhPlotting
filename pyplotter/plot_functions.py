#!/usr/bin/env python
import ROOT as ROOT
import CMS_lumi, tdrstyle
import argparse

def getHistFromFile (plot_info):
    file = ROOT.TFile(plot_info["file_name"])
    if not file:
        print 'Failed to open %s' % plot_info["file_name"]
        exit(0)
    tree = file.Get(plot_info["tree_folder"] + plot_info["tree_name"])
    hist = ROOT.TH1F("hist", "Test", 1000, 0, 1500)    
    tree.Draw(plot_info["tree_var"] + ">>hist")
    if not hist:
        print 'Failed to get hist from file'
        exit(0)
    hist.SetDirectory(ROOT.gROOT) # detach "hist" from the file
    return hist
def setHistAttributes (hist, plot_info, line_color, fill_color):
    hist.SetFillColor(fill_color)
    hist.SetLineColor(line_color)
    hist.SetLineWidth(2)
    if plot_info["rebin"] != 0:
        if type(hist) != "<class '__main__.TH2F'>":
            hist.Rebin(plot_info["rebin"])
        else:
            print 'Rebin only defined for 1D hist. Use --rebin2D instead.'
    hist.Draw()
    if plot_info["xmin"] < plot_info["xmax"]:
        hist.GetXaxis().SetRangeUser(plot_info["xmin"], plot_info["xmax"])
    if plot_info["ymin"] < plot_info["ymax"]:
        hist.GetYaxis().SetRangeUser(plot_info["ymin"], plot_info["ymax"])
    hist.GetYaxis().SetTitle(plot_info["ylabel"])
def addHistToStack (hist_stack, plot_info, hist_opts, line_color, fill_color):
    hist = getHistFromFile(plot_info)
    setHistAttributes(hist, plot_info, line_color, fill_color)
    hist_stack.Add(hist, hist_opts)
def makePlot (hist, hist_opts, plot_info):
    #legend = ROOT.TLegend(.5 ,.65 ,.885 ,.875)
    canvas = getCanvas()
    setTDRStyle(canvas, 1, 13, plot_info["printCMS"]) 
    if plot_info["logy"]:
        canvas.SetLogy()
    if plot_info["logx"]:
        canvas.SetLogx()
    #draw the lumi text on the canvas
    hist.Draw(hist_opts)
    setTDRStyle(canvas, 1, 13, plot_info["printCMS"]) 
    hist.GetXaxis().SetTitle(plot_info["xlabel"])
    if plot_info["ylabel"] == "":
        plot_info["ylabel"] = "Events / %s GeV" % int(hist.GetBinWidth(1))
    #hist.GetYaxis().SetTitle(plot_info["ylabel"])
    #hist.SetTitleOffset(1.3, "y")
    #hist.SetTitleOffset(1.1, "x")
    canvas.cd()
    canvas.Update()
    canvas.RedrawAxis()
    #frame = canvas.GetFrame()
    #frame.Draw()
    #legend.SetFillColor(ROOT.kWhite)
    #legend.AddEntry(hist, legendName)

    #legend.Draw("same")
    canvas.Print(plot_info["output_file"]) 
def makeStackPlots (stacked, unstacked, hist_opts, plot_info):
    #legend = ROOT.TLegend(.5 ,.65 ,.885 ,.875)
    canvas = getCanvas()
    if plot_info["logy"]:
        canvas.SetLogy()
    if plot_info["logx"]:
        canvas.SetLogx()
    #draw the lumi text on the canvas
    hist1.Draw(hist_opts)
    hist1.GetXaxis().SetTitle(plot_info["xlabel"])
    if plot_info["ylabel"] == "":
        plot_info["ylabel"] = "Events / %s GeV" % int(hist.GetBinWidth(1))
    hist1.GetYaxis().SetTitle(plot_info["ylabel"])
    hist1.SetTitleOffset(1.3, "y")
    hist.SetTitleOffset(1.1, "x")
    setTDRStyle(canvas, 1, 13, plot_info["printCMS"]) 
    canvas.cd()
    canvas.Update()
    canvas.RedrawAxis()
    #frame = canvas.GetFrame()
    #frame.Draw()
    #legend.SetFillColor(ROOT.kWhite)
    #legend.AddEntry(hist, legendName)

    #legend.Draw("same")
    canvas.Print(plot_info["output_file"]) 

def setTDRStyle(canvas, luminosity, energy, printCMS):
    tdrstyle.setTDRStyle() 
    if printCMS == "right" or printCMS == "left":
        if energy == 13:
            CMS_lumi.lumi_13TeV = "%s fb^{-1}" % luminosity
            if printCMS == "left":
                iPos = 11
            else:
                iPos = 13
            CMS_lumi.writeExtraText = 1
            CMS_lumi.extraText = "Preliminary"
            CMS_lumi.CMS_lumi(canvas, 4, iPos)
def getCanvas():
    H_ref = 600; 
    W_ref = 800; 
    W = W_ref
    H  = H_ref

    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.12*W_ref
    R = 0.04*W_ref

    canvas = ROOT.TCanvas("c2","c2",50,50,W,H)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin( L/W )
    canvas.SetRightMargin( R/W )
    canvas.SetTopMargin( T/H )
    canvas.SetBottomMargin( B/H )
    canvas.SetTickx(0)
    canvas.SetTicky(0) 
    return canvas
def getBasicParser():
    parser = argparse.ArgumentParser()
    #parser.add_argument('-n', '--file_name', type=str, required=True, 
    #                    help="Name of root file in which histogram is stored.")
    parser.add_argument('-o', '--output_file', type=str, required=True,
                        help="Name of produced plot file (type pdf/png/jpg etc.).")
    parser.add_argument('-t', '--tree_name', type=str, required=False, default="Ntuple",
                        help="Name of root tree")  
    parser.add_argument('-f', '--tree_folder', type=str, required=False, default="",
                        help="Folder where tree is stored")  
    parser.add_argument('-v', '--tree_var', type=str, required=False,
                        help="Variable name in root tree")  
    parser.add_argument('--xlabel', type=str, required=False, default="", 
                        help="x axis label")
    parser.add_argument('--ylabel', type=str, required=False, default="", 
                        help="y axis label")
    parser.add_argument('--xmin', type=float, required=False, default=0, 
                        help="minimum x value")
    parser.add_argument('--xmax', type=float, required=False, default=0, 
                        help="maximum x value")   
    parser.add_argument('--ymin', type=float, required=False, default=0, 
                        help="minimum y value")
    parser.add_argument('--ymax', type=float, required=False, default=0, 
                        help="maximum y value")
    parser.add_argument('--rebin', type=int, required=False, default=0, 
                        help="Number of bins to group together (1D only)")
    parser.add_argument('--logy', action='store_true',
                        help="Set y axis to logarithmic scale")
    parser.add_argument('--logx', action='store_true', 
                        help="Set x axis to logarithmic scale")
    parser.add_argument('--printCMS', type=str, default="left",required=False,
                        choices=["left","right"], help="""print 'CMS preliminary' 
                        in left (or right) upper corner""")
    return parser
