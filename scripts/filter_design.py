'''Python script for designing lumped element LP, HP, or BP filters.
This script returns the L and C values.
Required arguments are cutoff frequency in GHz, filter type, Tee/Pi configuration, and number of elements.

Example:
>py filter_design.py 3.0 LP T 3
L_1 = X, C_2 = Y, L_3 = Z
'''

import sys
import os

chebyshev = {1:"",2:"",3:"",4:"",5:"",6:"",7:"",8:"",9:"",10:""}
butterworth = {1:"",2:"",3:"",4:"",5:"",6:"",7:"",8:"",9:"",10:""}

def main():
    
    #Center frequency in GHz
    fc = float(sys.argv[1])
    
    #Filter type. <LP/HP/BP>
    f_type = sys.argv[2]

    #Configuration. Can be either Tee or Pi. <T/P> 
    config = sys.argv[3]

    #number of elements. Must be an integer from 1 to 10.
    num_elements = int(sys.argv[4])

    if(1 <= num_elements <= 10):
        pass
    else:
        raise ValueError("Number of elements must be between 1 and 10!")

def low_pass(num=1,fc=1,config="T",):
    pass

def high_pass():
    pass

def band_pass():
    pass

if __name__ == "__main__":
    main()