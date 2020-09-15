#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Disable warnings from pylint
# pylint: disable=invalid-name
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import numpy as np


def set_land_vals(x, y):
  #    9°E-45°E, 93°E-135°E, and 91°W-89°W   81°W  370-390
  #    9  -45  , 93  -135  ,    269 -271    279  -  315

  yocn = np.copy(y)
  index = 0
  while index < x.size:
    if x[index] >= 9. and x[index] <= 45.:
      yocn[index] = np.nan

    if x[index] >= 93. and x[index] <= 135.:
      yocn[index] = np.nan

    if x[index] >= 269. and x[index] <= 271.:
      yocn[index] = np.nan

    if x[index] >= 279. and x[index] <= 315.:
      yocn[index] = np.nan

    if x[index] >= 370. and x[index] <= 390.:
      yocn[index] = np.nan

    index += 1
  return yocn


def main():
  x = np.arange(30.0, 390.0, 2.0)
  y = np.zeros(x.size, dtype=float)
  yocn = set_land_vals(x, y)
  print(x)
  print(yocn)


# execute only if run as a script
if __name__ == "__main__":
  main()
  print(" *** End script *** ")
# Last line of script
