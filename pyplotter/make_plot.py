#!/usr/bin/env python
import ROOT
import CMS_lumi, tdrstyle
import argparse
import plot_functions as plotter

def main():
    plot_info = getPlotArgs()
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
    hist = plotter.getHistFromFile(plot_info)
    if type(hist) == "<class '__main__.TH2F'>":
        hist_opts = "colz"
    elif plot_info["is_data"]:
        hist_opts = "e1"
        line_color = ROOT.kBlack
        fill_color = ROOT.kBlack
    else:
        hist_opts = "hist"
        line_color = ROOT.kRed+4
        fill_color = ROOT.kOrange-8
    plotter.setHistAttributes(hist, plot_info, line_color, fill_color)
    plotter.makePlot(hist, hist_opts, plot_info)
def getPlotArgs():
    parser = plotter.getBasicParser()
    parser.add_argument("-n", "--file_name", type=str, required=True,
                        help="Name of root file where plots are stored")
    parser.add_argument("--is_data", action='store_true',
                        help="Plot histogram with data points")
    return vars(parser.parse_args())
    
if __name__ == "__main__":
    main()
