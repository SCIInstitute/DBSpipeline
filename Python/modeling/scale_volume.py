import sys, argparse
#pip install pynrrd
import nrrd
import numpy as np
import os

#usage:
# python scale_volume [-flags inputs] [filename]



def scale_nrrd(filename, outfile, scalar = 1.0 , threshold = 0.015):
  readdata, header = nrrd.read(filename)
  
  scaled_data=scalar*readdata
  
  roidata = (scaled_data>threshold).astype(int)

#  print(header)
  
  nrrd.write(outfile, roidata, header)
  
  return
  
  
def make_outname(filename, scalar = -1.0, unit = "mA"):

  dirname, fname = os.path.split(filename)
  fileroot, f_ext = os.path.splitext(fname)
  
  stim_str = "_{:2.1f}".format(scalar)+unit
  outfname = os.path.join(dirname,fileroot+stim_str+f_ext)
  
  return outfname
  
def build_parser():
  parser = argparse.ArgumentParser(
                prog = "scale_volume",
                description = "scales a activation field to find the ROI regoins (pixels) to use in MRtrix.",
                epilog="output saves as the filename with the scale factor added"
                )

  # This will be implemented as rollout broadens
  parser.add_argument("filename", metavar="filename(s)", nargs="*",
                      help="target file(s) (.nrrd) to scale and threshold")
  parser.add_argument("-s", "--scale", type=float, required=False,
                      help="Scaling factor (amplitude of the stimulation)",
                      default = -1.0, dest="scalar")
  parser.add_argument("-u", "--units", required=False,
                      help="Units for Scaling factor (mA)",
                      default ="mA", dest="units")
  parser.add_argument("-t", "--threshold", type=float, required=False,
                      help="Activation Threshold",
                      default = 0.015, dest="threshold")
  return parser
  
def main():

  parser = build_parser()
  options = parser.parse_args()
  
  print(options.filename)
  print(options.scalar)
  print(options.threshold)
  print(options.units)
  
  filenames = options.filename
  scalar = options.scalar
  threshold = options.threshold
  units = options.units
  
  for filename in filenames:
    print("running :", filename)
    
    outname = make_outname(filename, scalar, units)
    scale_nrrd(filename, outname, scalar, threshold)
  
  return
      


if __name__ == "__main__":
   main()
  
  

  

