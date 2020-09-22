#!/usr/bin/env python3
# Disable warnings from pylint
# pylint: disable=invalid-name
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable="indentation-is-not-a-multiple-of-four-[pycodestyle]"
# pylint: disable=E111

import numpy as np

def matrix_print(mat, fmt="g",title="title"):
  """
    matrix_print(mat=A, fmt="g", title="title")
    matrix_print(mat=A, fmt=".2e", title="title")
  """
  print("\n"+title)
  col_maxes = [
      max([len(("{:" + fmt + "}").format(x)) for x in col]) for col in mat.T
  ]
  for x in mat:
    for i, y in enumerate(x):
      print(("{:" + str(col_maxes[i]) + fmt + "}").format(y), end="  ")
    print("")

def main():
  inf = float(np.nan)
  A = np.array([[0, 1., 4., inf, 3, 7], [1, 0, 2, inf, 4, 8],
              [4, 2, 0, 1, 5.5, 0], [inf, inf, 1.01, 0, 3, 11],
              [3, 4, 5, 3, 0, 12]])

  A[2, 3] = -15.7777
  A[4, 2] = -19.7777

  print("\nFormat g:")
  matrix_print(mat=A, fmt="g",title="\nFormat g:")
  print("\nFormat .2E:")
  matrix_print(mat=A, fmt=".2E",title="\nFormat .2E:")

if __name__ == "__main__":
  # execute only if run as a script
  main()
  print(" \n+++++ End script +++++ \n")

#Last line of script
#EOF - Last line in the file
