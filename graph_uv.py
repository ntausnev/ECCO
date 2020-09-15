def generate_plot(ax, plt, x_plot, y_ocng, y_ocnh, y_zero, \
        line_g, line_h, \
        legend_dstg, legend_dsth,y_ticks):
  import numpy as np

  # Generate the plot
  ax.plot(x_plot, y_ocng, lw=1, label=legend_dstg, color="red")
  ax.plot(x_plot, y_ocng, color="red", marker='o', ms=3.)
  ax.plot(x_plot, y_zero, lw=0.5, color="black", linestyle="--")

  ax.plot(x_plot, y_ocnh, lw=1, label=legend_dsth, color="green")
  ax.plot(x_plot, y_ocnh, color="green", marker='o', ms=2.)

  ax.text(0.25, -0.22, line_g, color='red', transform=ax.transAxes)
  ax.text(0.5, -0.22, line_h, color='green', transform=ax.transAxes)

  ax.set_ylabel('m / s')
  # Make a plot with major ticks that are multiples of 20 and minor ticks that
  # are multiples of 5.  Label major ticks with '%d' formatting but don't label
  # minor ticks.
  #ax.xaxis.set_major_locator(MultipleLocator(20))

  # Set title for the plot
  #   ax.set_title(
  #       'E2.1 U Wind 10m Height Along Equator 2°x2° Monthly-Mean Jul2009',
  #       pad=25, fontweight="bold")

  # Set up grid, legend, and limits
  # Set up grid, legend, and limits
  #ax.grid(True)
  ax.grid(False)
  ax.legend(frameon=False)

  # For the major/minor ticks, use no labels; default NullFormatter.

  ax.xaxis.set_major_locator(plt.MultipleLocator(30.))
  ax.xaxis.set_minor_locator(plt.MultipleLocator(10.))
  ax.yaxis.set_major_locator(plt.MultipleLocator(2.))
  ax.yaxis.set_minor_locator(plt.MultipleLocator(1.))

  x_ticks = np.arange(30., 420., 30.)
  #   y_ticks = np.arange(-8, 8, 2)

  ax.set_xticklabels([
      '$30^o$E', '$60^o$E', '$90^o$E', '$120^o$E', '$150^o$E', '$180^o$',
      '$150^o$W', '$120^o$W', '$90^o$W', '$60^o$W', '$30^o$W', '$0^o$',
      '$30^o$E'
  ])
  #   ax.set_yticklabels([-8, -6, -4, -2, 0, 2, 4, 6, 8])

  ax.tick_params(which="minor",
                 axis="x",
                 direction="in",
                 bottom=True,
                 top=True,
                 left=False,
                 right=False)
  ax.tick_params(which="minor",
                 axis="y",
                 direction="in",
                 bottom=False,
                 top=False,
                 left=True,
                 right=True)
  ax.tick_params(which="major", axis="x", direction="in", bottom=True, top=True)
  ax.tick_params(which="major", axis="y", direction="in", left=True, right=True)
  ax.tick_params(axis="x", direction="in")
  ax.tick_params(axis="y", direction="in")

  ax.tick_params(labelbottom=True,
                 labeltop=True,
                 labelleft=True,
                 labelright=True)

  ax.tick_params(axis='x', which='major', pad=7)

  ax.set_xticks(x_ticks)
  ax.set_yticks(y_ticks)

  ax.set_xlim(30., 390.)


#   ax.set_ylim(-8., 6.0)
