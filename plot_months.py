#!/usr/bin/env python3
# Disable warnings from pylint
# pylint: disable=invalid-name
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

from set_nan_values import set_land_vals
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

# http://code.google.com/p/netcdf4-python/
from netCDF4 import Dataset
from tnl_netcdf import ncdump
from graph_uv import generate_plot


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
    print(yg)

    shift = 75
    x_t = shift_longitude(x, shift)
    x_plot = np.where(x_t < 30., x_t + 360., x_t)
    y_plotg = shift_longitude(yg, shift)
    y_ploth = shift_longitude(yh, shift)
    print("x=")
    print(x)
    print("x_t=")
    print(x_t)

    print("x_plot=")
    print(x_plot)
    print(yg)
    y_ocng = set_land_vals(x_plot, y_plotg)
    y_ocnh = set_land_vals(x_plot, y_ploth)
    print("y_ocng: ")
    print(y_ocng)

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

def main():

    month_s = 7      # July 2009/ from 1 to 24
    month_e = 16      # April 2010

    DATA_IN = "./DATA_IN/"
    DATA_OUT= "./DATA_OUT/"

    obs_mon  = ["Jan2009", "Feb2009", "Mar2009", "Apr2009", "May2009", "Jun2009", 
                "Jul2009", "Aug2009", "Sep2009", "Oct2009", "Nov2009", "Dec2009",
                "Jan2010", "Feb2010", "Mar2010", "Apr2010", "May2010", "Jun2010", 
                "Jul2010", "Aug2010", "Sep2010", "Oct2010", "Nov2010", "Dec2010" ]

    fmm = open("f_min_max", "w")  # file max and min wind speed

    for month in range( month_s, month_e + 1  ):

      file_out_pdf = DATA_OUT + 'E2.1 Wind U V ' + obs_mon[month-1] + ".pdf"

      file_g = DATA_IN + "2009-2010_cal.usurf_g_2x2.nc"
      file_h = DATA_IN + "2009-2010_cal.usurf_h_2x2.nc"
      latsg, lonsg, timeg, wg = read_section_equator(file_g, "USURF")
      latsh, lonsh, timeh, wh = read_section_equator(file_h, "USURF")
      legend_dstg = "E2.1-G"
      legend_dsth = "E2.1-H"

      # Generate data for plots
      x_plot, y_ocng, y_ocnh, wmean_g, wmean_h, y_zero = \
          generate_data_plot(lonsh,  month, wg, wh)
      print(" Mean wind over ocean g {:5.2f} ".format(wmean_g))
      print(" Mean wind over ocean h {:5.2f} ".format(wmean_h))
      line_g = "<U 10m> = {:4.1f} m/s ".format(wmean_g)
      line_h = "<U 10m> = {:4.1f} m/s ".format(wmean_h)

      # Get an empty figure
  #   fig1, (ax0, ax) = plt.subplots(nrows=2)
  #   ax0.axis("off")
  #   fig1.set_size_inches(7.0, 11.0)

      fig = plt.figure(figsize=(8.0, 11.0))
      ax2 = fig.add_axes([0.05, 0.15,  0.9, 0.25])
      ax1 = fig.add_axes([0.05, 0.6,  0.9, 0.25])
  #   title = ax1.set_title("My plot", fontsize='large')


    # Set title for the plot
      ax1.set_title( 'E2.1 U Wind 10m Height Along Equator 2°x2 Monthly-Mean ' + obs_mon[month-1],
                            pad=25, fontweight="bold" )
      ax1.set_ylim(-8.,  6.0)
      y_ticks = np.arange(-8, 8, 2)
      ax1.set_yticks(y_ticks)
      ax1.set_yticklabels([-8, -6, -4, -2, 0, 2, 4, 6, 8 ])

      generate_plot(ax1, plt, x_plot, y_ocng, y_ocnh, y_zero, line_g, line_h,
                    legend_dstg, legend_dsth,y_ticks)

      wmin_g = np.nanmin((y_ocng))
      wmin_h = np.nanmin((y_ocnh))
      str = "\nMonth= " + obs_mon[month-1]
      fmm.write(str)
      fmm.write(" Min U wind over ocean g {:5.2f} ".format(wmin_g))
      fmm.write(" Min U wind over ocean h {:5.2f} ".format(wmin_h))

      wmax_g = np.nanmax((y_ocng))
      wmax_h = np.nanmax((y_ocnh))
      str = "\nMonth= " + obs_mon[month-1]
      fmm.write(str)
      fmm.write(" Max U wind over ocean g {:5.2f} ".format(wmax_g))
      fmm.write(" Max U wind over ocean h {:5.2f} ".format(wmax_h))

      fmm.write(" \n ")

  ############################# V component #######################################################

      file_g = DATA_IN + "2009-2010_cal.vsurf_g_2x2.nc"
      file_h = DATA_IN + "2009-2010_cal.vsurf_h_2x2.nc"
      latsg, lonsg, timeg, wg = read_section_equator(file_g, "VSURF")
      latsh, lonsh, timeh, wh = read_section_equator(file_h, "VSURF")
      x_plot, y_ocng, y_ocnh, wmean_g, wmean_h, y_zero = \
          generate_data_plot(lonsh, month, wg, wh)
      print(" Mean wind over ocean g {:5.2f} ".format(wmean_g))
      print(" Mean wind over ocean h {:5.2f} ".format(wmean_h))
      line_g = "<V 10m> = {:4.1f} m/s ".format(wmean_g)
      line_h = "<V 10m> = {:4.1f} m/s ".format(wmean_h)

    # Set title for the plot
      ax2.set_title( 'E2.1 V Wind 10m Height Along Equator 2°x2° Mohly-Mean ' + obs_mon[month-1],
                            pad=25, fontweight="bold" )
      ax2.set_ylim(-6., 8.)
      y_ticks = np.arange(-6,  10, 2)
      ax2.set_yticks(y_ticks)
      ax2.set_yticklabels([-6, -4, -2, 0, 2, 4, 6, 8, 10])

      generate_plot(ax2, plt, x_plot, y_ocng, y_ocnh, y_zero, line_g, line_h,
                    legend_dstg, legend_dsth,y_ticks)

      wmin_g = np.nanmin((y_ocng))
      wmin_h = np.nanmin((y_ocnh))
      str = "\nMonth= " + obs_mon[month-1]
      fmm.write(str)
      fmm.write(" Min V wind over ocean g {:5.2f} ".format(wmin_g))
      fmm.write(" Min V wind over ocean h {:5.2f} ".format(wmin_h))

      wmax_g = np.nanmax((y_ocng))
      wmax_h = np.nanmax((y_ocnh))
      str = "\nMonth= " + obs_mon[month-1]
      fmm.write(str)
      fmm.write(" Max V wind over ocean g {:5.2f} ".format(wmax_g))
      fmm.write(" Max V wind over ocean h {:5.2f} ".format(wmax_h))

      fmm.write(" \n ")
      plt.savefig(file_out_pdf)

    # Display the figure
    plt.show()
    plt.close()
    fmm.close()


if __name__ == "__main__":  # ky-ky
    # execute only if run as a script
    main()
    print(" \n*** End script *** \n")

# Last line of script
