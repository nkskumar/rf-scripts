"""
This is a script to convert 2-port S-parameter data to ABCD-parameter data and vice versa.
To run script, type python param_conv.py filename parameter_type on the command line like so:

>python param_conv.py sample_file.s2p S dest_file_name 

Author: Nithin Kumar Santha Kumar
Email: nithinkumar.santhakumar@utdallas.edu
Date: 08/25/2022
License: MIT
"""

from math import cos,sin
import sys

def main():
    #filename only if in src folder else include entire filepath
    filepath = sys.argv[1]

    #type of parameter to convert to. <S/ABCD>
    param_type = sys.argv[2]

    #filename only if in dest folder else include entire filepath.
    dest_filepath = sys.argv[3] 

    #default values for option line
    freq_unit = "GHz"
    p_type = "S"
    p_format = "RI"
    z0 = 50.0
    data = []
    version = 2.0

    if filepath.endswith(".s2p") or filepath.endswith(".S2P"):
        if param_type == "S":
            try:
                with open(filepath,'r') as fp:
                    pass
            
            except FileNotFoundError:
                raise ValueError("File Path is incorrect or File does not exist!")
            
            with open(dest_filepath,"w") as f:
                f.write("! Converted ABCD-parameter data to S-parameter data\n")
                f.write(f"[Version] {version}\n")
                f.write(f"# {freq_unit} ABCD {p_format} {z0}\n")
                for lst in data:
                    for element in lst:
                        f.write(str(element))
                        f.write(" ")
                    f.write("\n")
        elif param_type == "ABCD":
            try:
                with open(filepath,'r') as fp:
                    for line in fp:
                        if line.startswith("!"):
                            continue
                        elif line.startswith("#"):
                            opt_line = line.strip().split()
                            #print(opt_line)
                            z0 = float(opt_line[5])
                            freq_unit = opt_line[1]
                            p_type = opt_line[2]
                            p_format = opt_line[3]
                            print(f"# {freq_unit} {p_type} {p_format} {z0}")
                        elif line.startswith("[Version]"):
                            ver_line = line.strip().split()
                            version = ver_line[1]
                            print(f"{version}")
                        elif line.startswith("[Number of Ports]"):
                            continue
                        elif (line.startswith("[Noise Data]") or line.startswith("! NOISE")):
                            break #Not implementing Noise parameters for now.
                        else:
                            data_line = line.strip().split()
                            data.append(to_abcd(data_line,z0,p_format))
            except FileNotFoundError:
                raise ValueError("File Path is incorrect or File does not exist!")
            
            with open(dest_filepath,"w") as f:
                f.write("! Converted S-parameter data to ABCD-parameter data\n")
                f.write(f"[Version] {version}\n")
                f.write(f"# {freq_unit} ABCD {p_format} R {z0}\n")
                for lst in data:
                    for element in lst:
                        f.write(str(element))
                        f.write(" ")
                    f.write("\n")
        else:
            raise ValueError("Invalid parameter type!")
    else:
        raise ValueError("File type must be .s2p!")
    

def to_sparam(data,z0,format):
    freq = data[0]
    a = data[1]
    b = data[2]
    c = data[3]
    d = data[4]
    s11 = (a + (b/z0) - (c*z0) - d) / (a + (b/z0) + (c*z0) + d)
    s12 = 2 * ((a*d) - (b*c)) / (a + (b/z0) + (c*z0) + d)
    s21 = 2 / (a + (b/z0) + (c*z0) + d)
    s22 = (-a + (b/z0) - (c*z0) + d) / (a + (b/z0) + (c*z0) + d)
    
    return [freq, s11, s21, s12, s22]

def to_abcd(data,z0,format):
    freq = float(data[0])
    
    s11_r = float(data[1])
    s11_i = float(data[2])
    s21_r = float(data[3])
    s21_i = float(data[4])
    s12_r = float(data[5])
    s12_i = float(data[6])
    s22_r = float(data[7])
    s22_i = float(data[8])

    if format == "RI":
        s11 = complex(s11_r,s11_i)
        s21 = complex(s21_r,s21_i)
        s12 = complex(s12_r,s12_i)
        s22 = complex(s22_r,s22_i)
        #print(f"s11 = {s11}, s21 = {s21}, s12 = {s12}, s22 = {s22}")
    elif format == "MA":
        s11 = complex(s11_r*cos(s11_i),s11_r*sin(s11_i))
        s21 = complex(s21_r*cos(s21_i),s21_r*sin(s21_i))
        s12 = complex(s12_r*cos(s12_i),s12_r*sin(s12_i))
        s22 = complex(s22_r*cos(s22_i),s22_r*sin(s22_i))
    elif format == "DB":
        #magnitude in dB = 20 * log10(sqrt(Re**2 + Im**2)) to magnitude = 10**(mag_dB / 20)
        s11_mag = 10**(s11_r / 20)
        s21_mag = 10**(s21_r / 20)
        s12_mag = 10**(s12_r / 20)
        s22_mag = 10**(s22_r / 20)
        s11 = complex(s11_mag*cos(s11_i),s11_mag*sin(s11_i))
        s21 = complex(s21_mag*cos(s21_i),s21_mag*sin(s21_i))
        s12 = complex(s12_mag*cos(s12_i),s12_mag*sin(s12_i))
        s22 = complex(s22_mag*cos(s22_i),s22_mag*sin(s22_i))
    else:
        raise ValueError("Invalid format! Format must be RI, MA, or DB only!")

    a = ((1 + s11) * (1 - s22) + (s12 * s21)) / (2 * s21)
    b = z0 * ((1 + s11) * (1 + s22) - (s12 * s21)) / (2 * s21)
    c = ((1 - s11) * (1 - s22) - (s12 * s21)) / (z0 * 2 * s21)
    d = ((1 - s11) * (1 + s22) + (s12 * s21)) / (2 * s21)

    print(f"freq = {freq}, A = {a}, B = {b}, C = {c}, D = {d}")

    return [freq, a, b, c, d]

if __name__ == "__main__":
    main()
