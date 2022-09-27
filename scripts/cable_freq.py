"""Python Script for calculating cutoff frequency (in GHz) of a cable using
the diameters and relative permittivity of the cable.

Use:
>py cable_freq.py epsilon_r dielectric_diameter conductor_diameter

Example:
>py cable_freq.py 4.6 10 5
Cutoff Frequency of the Cable is: 5.93 GHz


Author: Nithin Kumar Santha Kumar
Email: nithinkumar.santhakumar@utdallas.edu
Date: 09/24/2022
License: MIT
"""

import sys
import math

def main():
    e_r = float(sys.argv[1])
    dielectric_diameter = float(sys.argv[2])
    conductor_diameter = float(sys.argv[3])

    f_c = (190.8 / math.sqrt(e_r)) * (1 / (dielectric_diameter + conductor_diameter))

    print(f"Cutoff Frequency of the Cable is: {f_c:.2f} GHz")

if __name__ == "__main__":
    main()