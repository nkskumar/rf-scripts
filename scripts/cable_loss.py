"""Python Script for calculating loss (in dB/m) of a cable using
the diameters, relative permittivity, frequency, loss tangent,
and loss constants of the cable.

Formula is based on video by TheSignalPath.
URL: https://thesignalpath.com/blogs/videofeed/tsp-214-what-is-a-good-rf-cable-theory-experiments-with-junkosha-phase-amplitude-stable-cables/

Use:
>py cable_freq.py freq epsilon_r d_d c_d tand k1 k2 rho1 rho2 
where:
    d_d is Dielectric Diameter
    c_d is Conductor Diameter
    tand is loss tangent
    k1 is
    k2 is
    rho1 is
    rho2 is

Example:
>py cable_loss.py 3 4.6 10 5 0.0031 k1 k2 rho1 rho2
Loss of the Cable is: x dB

Author: Nithin Kumar Santha Kumar
Email: nithinkumar.santhakumar@utdallas.edu
Date: 09/25/2022
License: MIT
"""

import sys
import math

def main():
    freq = float(sys.argv[1])
    e_r = float(sys.argv[2])
    d_d = float(sys.argv[3])
    c_d = float(sys.argv[4])
    tan_d = float(sys.argv[5])
    k1 = float(sys.argv[6])
    k2 = float(sys.argv[7])
    rho1 = float(sys.argv[8])
    rho2 = float(sys.argv[9])

    log_term = math.log10(d_d / c_d)
    sqrt_term = math.sqrt(e_r * freq)
    k_terms = (k2 * math.sqrt(rho1) / c_d) + (k1 * math.sqrt(rho2) / d_d)
    loss = 8.686e2 * ((((2.287e-3 * sqrt_term) / log_term) * k_terms) + (1.047e-4 * math.sqrt(e_r) * tan_d * freq)) 

    print(f"The cable loss in dB/m is {loss}")

if __name__ == "__main__":
    main()