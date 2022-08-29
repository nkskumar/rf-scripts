"""
Author: Nithin Kumar Santha Kumar

Python script that returns the characteristic impedance and 
effective relative dielectric constant

Example:
>python microstrip.py w h e_r
Effective Relative Dielectric Constant = X
Characteristic Impedance = Y Ohms
"""
import sys
from math import pi,log,sqrt

def main()->None:
    """
    MAIN function
    """
    width = float(sys.argv[1])
    height = float(sys.argv[2])
    epsilon_r = float(sys.argv[3])

    #modified Wheeler's equation for effective relative dielectric constant
    e_eff = ((epsilon_r+1)/2) + (((epsilon_r-1)/2) * (1/sqrt(1 + 12*(height/width)) + (0.04 * (1 - (width/height)) ** 2)))

    if (width/height) < 1:
        #modified Wheeler's equation for characteristic impedance for narrow line case
        z_0 = (377.0 / (2*pi*sqrt(e_eff))) * log((8 * height / width) + (width / (4 * height)))  
    elif (width / height) >= 1:
        #modified Wheeler's equation for characteristic impedance for wide line case
        z_0 = 377.0 / (sqrt(e_eff) * ((width/height) + 1.393 + 0.667*log((width/height)+1.444)))  
    print(f"Effective Relative Dielectric Constant = {e_eff}")
    print(f"Characteristic Impedance = {z_0} Ohms")

if __name__ == "__main__":
    main()
