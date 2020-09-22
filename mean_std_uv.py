#!/usr/bin/env python3
# Disable warnings from pylint
# pylint: disable=invalid-name
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable="indentation-is-not-a-multiple-of-four-[pycodestyle]"
# pylint: disable=E111

import numpy as np

#import matplotlib.ticker as ticker

from set_nan_values import set_land_vals
#from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
#                              AutoMinorLocator)

# http://code.google.com/p/netcdf4-python/
from netCDF4 import Dataset
from tnl_netcdf import ncdump

from matrix_print import matrix_print


def read_section_equator(fileIn, name_var):

  print("+++ Try Read file ={} +++ ".format(fileIn))
  nc_fid = Dataset(fileIn, 'r')  # Dataset to open the file
  # and create an instance of the ncCDF4 class

  nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)

  # Extract data from NetCDF file
  lats = nc_fid.variables['YSAT'][:]  # extract/copy the data
  lons = nc_fid.variables['XSAT'][:]
  time = nc_fid.variables['TIME'][:]
  u = nc_fid.variables[name_var][:]  # shape is lat, lon and time
  return lats, lons, time, u


# Generate data for plots
def generate_data_plot(lonsh, month, wg, wh):  # month 1-24

  x = np.linspace(-180, 178, 180)
  y_zero = np.zeros(180)
  x = lonsh
  time_rec = month - 1
  yg = wg[time_rec, 45, :]
  yh = wh[time_rec, 45, :]
  #   print(yg)

  shift = 75
  x_t = shift_longitude(x, shift)
  x_plot = np.where(x_t < 30., x_t + 360., x_t)
  y_plotg = shift_longitude(yg, shift)
  y_ploth = shift_longitude(yh, shift)
  #   print("x=")
  #   print(x)
  #   print("x_t=")
  #   print(x_t)

  #   print("x_plot=")
  #   print(x_plot)
  #   print(yg)
  y_ocng = set_land_vals(x_plot, y_plotg)
  y_ocnh = set_land_vals(x_plot, y_ploth)
  #   print("y_ocng: ")
  #   print(y_ocng)

  wmean_g = np.nanmean((y_ocng))
  wmean_h = np.nanmean((y_ocnh))
  print(" Mean wind over ocean g {:5.2f} ".format(wmean_g))
  print(" Mean wind over ocean h {:5.2f} ".format(wmean_h))

  wmin_g = np.nanmin((y_ocng))
  wmin_h = np.nanmin((y_ocnh))
  print(" Min wind over ocean g {:5.2f} ".format(wmin_g))
  print(" Min wind over ocean h {:5.2f} ".format(wmin_h))

  wmax_g = np.nanmax((y_ocng))
  wmax_h = np.nanmax((y_ocnh))
  print(" Max wind over ocean g {:5.2f} ".format(wmax_g))
  print(" Max wind over ocean h {:5.2f} ".format(wmax_h))

  return x_plot, y_ocng, y_ocnh, wmean_g, wmean_h, y_zero


def shift_longitude(arr_src, step):
  arr_out = np.roll(arr_src, step)
  return arr_out


def mean_std_uv(month_s, month_e):

  DATA_IN = "./DATA_IN/"

  month_total = 0
  for month in range(month_s, month_e + 1):

    month_total = month_total + 1

    file_g = DATA_IN + "2009-2010_cal.usurf_g_2x2.nc"
    file_h = DATA_IN + "2009-2010_cal.usurf_h_2x2.nc"
    latsg, lonsg, timeg, wg = read_section_equator(file_g, "USURF")
    latsh, lonsh, timeh, wh = read_section_equator(file_h, "USURF")


    # Generate data for plots
    x_plot, y_ocng, y_ocnh, wmean_g, wmean_h, y_zero = \
        generate_data_plot(lonsh,  month, wg, wh)
    print(" Mean wind over ocean g {:5.2f} ".format(wmean_g))
    print(" Mean wind over ocean h {:5.2f} ".format(wmean_h))

    if month_total == 1:
      # creating an empty 2d array of float32 type
      ug10 =  np.empty((0,y_ocng.size),np.float32)
      uh10 =  np.empty((0,y_ocnh.size),np.float32)
#### TEST:
    if month == 15:
      print("\nMonth={} U wind over ocean g ".format(month))
      print(y_ocng)
      print("\nMonth={} U wind over ocean h ".format(month))
      print(y_ocnh)

    ug10 = np.vstack( (ug10, y_ocng ))
    uh10 = np.vstack( (uh10, y_ocnh ))

    file_g = DATA_IN + "2009-2010_cal.vsurf_g_2x2.nc"
    file_h = DATA_IN + "2009-2010_cal.vsurf_h_2x2.nc"
    latsg, lonsg, timeg, wg = read_section_equator(file_g, "VSURF")
    latsh, lonsh, timeh, wh = read_section_equator(file_h, "VSURF")
    x_plot, y_ocng, y_ocnh, wmean_g, wmean_h, y_zero = \
        generate_data_plot(lonsh, month, wg, wh)

#   print(" Mean wind over ocean g {:5.2f} ".format(wmean_g))
#   print(" Mean wind over ocean h {:5.2f} ".format(wmean_h))

    if month_total == 1:
      # creating an empty 2d array of float32 type
      vg10 =  np.empty((0,y_ocng.size),np.float32)
      vh10 =  np.empty((0,y_ocnh.size),np.float32)
#### TEST:
    if month == 15:
      print("\nMonth={} V wind over ocean g ".format(month))
      print(y_ocng)
      print("\nMonth={} V wind over ocean h ".format(month))
      print(y_ocnh)


    vg10 = np.vstack( (vg10, y_ocng ))
    vh10 = np.vstack( (vh10, y_ocnh ))


  ug10_t = ug10.T   # Transpose matrix
  vg10_t = vg10.T   # Transpose matrix

  uh10_t = uh10.T   # Transpose matrix
  vh10_t = vh10.T   # Transpose matrix

  matrix_print(mat=ug10_t,fmt=".2E",title="ug10_t")
  matrix_print(mat=vg10_t,fmt=".2E",title="vg10_t")

  matrix_print(mat=uh10_t,fmt=".2E",title="uh10_t")
  matrix_print(mat=vh10_t,fmt=".2E",title="vh10_t")

  ug_mean = np.mean(ug10_t,axis=1)
  vg_mean = np.mean(vg10_t,axis=1)

  uh_mean = np.mean(uh10_t,axis=1)
  vh_mean = np.mean(vh10_t,axis=1)

  np.set_printoptions(precision=2)
  print("\nug_mean =")
  print(ug_mean)
  print("\nvg_mean =")
  print(vg_mean)

  print("\nuh_mean =")
  print(uh_mean)
  print("\nvh_mean =")
  print(vh_mean)

  ug_std = np.std(ug10_t,axis=1)
  vg_std = np.std(vg10_t,axis=1)

  uh_std = np.std(uh10_t,axis=1)
  vh_std = np.std(vh10_t,axis=1)

  print("\nug_std =")
  print(ug_std)
  print("\nvg_std =")
  print(vg_std)
  print("\nuh_std =")
  print(uh_std)
  print("\nvh_std =")
  print(vh_std)

  return ug_mean, vg_mean, ug_std, vg_std, uh_mean, vh_mean, uh_std, vh_std

def main():
  # execute only if run as a script
  month_s = 7  # July 2009/ from 1 to 24
  #   month_s = 15     # Test
  month_e = 16  # April 2010

  ug_mean, vg_mean, ug_std, vg_std, uh_mean, vh_mean, uh_std, vh_std = mean_std_uv(month_s, month_e)

if __name__ == "__main__":  # ky-ky
  main()

  print(" \n+++++ End script +++++ \n")

#Last line of script

#EOF - Last line in the file
