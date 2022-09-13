"""Python Script for calculating insertion loss (in dB) after measuring 
output power of a DUT.

Format choices are: dBm, dBW, mW, W

Example:
>py il.py mW 1.0 0.1
Format: mW, Reference Power: 1.0, Output Power: 0.1
Insertion Loss (dB): 10.0 dB

Author: Nithin Kumar Santha Kumar
Email: nithinkumar.santhakumar@utdallas.edu
Date: 09/13/2022
License: MIT
"""
import numpy as np
import sys
import os

try:
    import numpy as np
except:
    os.system("pip install numpy")

def main():
    unit = sys.argv[1]

    p_ref = float(sys.argv[2])

    p_out = float(sys.argv[3])
    
    if unit == "dBm" or unit == "dBW":
        insertion_loss = p_ref - p_out
    else: 
        insertion_loss = 10 * np.log10(p_ref / p_out)
    
    print(f"Reference Power: {p_ref} {unit}, Output Power: {p_out} {unit}")
    print(f"Insertion Loss (dB): {insertion_loss} dB")

if __name__ == "__main__":
    main()