"""
This is a script to convert 2-port S-parameter data to ABCD-parameter, T-parameter, Z-parameter, or Y-parameter data and vice versa.
To run script, type python param_conv.py filename parameter_type dest_filename on the command line like so:

>python param_conv.py sample_file.s2p ABCD dest_file_name 

Author: Nithin Kumar Santha Kumar
Email: nithinkumar.santhakumar@utdallas.edu
Date: 08/25/2022
License: MIT
"""

import sys
import os

try:
    import skrf as rf
except:
    os.system("pip install scikit-rf")

def main():
    """_summary_
    """
    #filename only if in src folder else include entire filepath
    filepath = sys.argv[1]

    #type of parameter to convert to. <S/ABCD/T/Z/Y>
    param_type = sys.argv[2]

    #filename only if in dest folder else include entire filepath.
    dest_filepath = sys.argv[3]

    if filepath.endswith(".s2p") or filepath.endswith(".S2P"):
        try:
            snp = rf.Network(filepath)
            if param_type == "S":
                pass
        except FileNotFoundError as no_file_found:
            raise ValueError("File Path is incorrect or File does not exist!") from no_file_found

    else:
        raise ValueError("File type must be .s2p!")  

if __name__ == "__main__":
    main()
