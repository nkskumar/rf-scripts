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
    """_summary_

    Raises
    ------
    ValueError
        _description_
    ValueError
        _description_
    ValueError
        _description_
    ValueError
        _description_
    """
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
    z_0 = 50.0
    data = []
    version = 2.0

    if filepath.endswith(".s2p") or filepath.endswith(".S2P"):
        if param_type == "S":
            try:
                with open(filepath,'r') as fp:
                    pass         
            except FileNotFoundError as no_file_found:
                raise ValueError("File Path is incorrect or File does not exist!") from no_file_found

            with open(dest_filepath,"w") as f:
                f.write("! Converted ABCD-parameter data to S-parameter data\n")
                f.write(f"[Version] {version}\n")
                f.write(f"# {freq_unit} ABCD {p_format} {z_0}\n")
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
                            z_0 = float(opt_line[5])
                            freq_unit = opt_line[1]
                            p_type = opt_line[2]
                            p_format = opt_line[3]
                            print(f"# {freq_unit} {p_type} {p_format} {z_0}")
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
                            data.append(to_abcd(data_line,z_0,p_format))
            except FileNotFoundError as no_file_found:
                raise ValueError("File Path is incorrect or File does not exist!") from no_file_found
          
            with open(dest_filepath,"w") as f:
                f.write("! Converted S-parameter data to ABCD-parameter data\n")
                f.write(f"[Version] {version}\n")
                f.write(f"# {freq_unit} ABCD {p_format} R {z_0}\n")
                for lst in data:
                    for element in lst:
                        f.write(str(element))
                        f.write(" ")
                    f.write("\n")
        else:
            raise ValueError("Invalid parameter type!")
    else:
        raise ValueError("File type must be .s2p!")  

def to_sparam(data,z0,frmt):
    """_summary_

    Parameters
    ----------
    data : _type_
        _description_
    z0 : _type_
        _description_
    format : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    freq = data[0]
    a_param = data[1]
    b_param = data[2]
    c_param = data[3]
    d_param = data[4]
    s11 = (a_param + (b_param/z0) - (c_param*z0) - d_param) / (a_param + (b_param/z0) + (c_param*z0) + d_param)
    s12 = 2 * ((a_param*d_param) - (b_param*c_param)) / (a_param + (b_param/z0) + (c_param*z0) + d_param)
    s21 = 2 / (a_param + (b_param/z0) + (c_param*z0) + d_param)
    s22 = (-a_param + (b_param/z0) - (c_param*z0) + d_param) / (a_param + (b_param/z0) + (c_param*z0) + d_param)

    return [freq, s11, s21, s12, s22]

def to_abcd(data,z_0,frmt):
    """_summary_

    Parameters
    ----------
    data : _type_
        _description_
    z0 : _type_
        _description_
    format : _type_
        _description_

    Returns
    -------
    _type_
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    freq = float(data[0])
    s11_r = float(data[1])
    s11_i = float(data[2])
    s21_r = float(data[3])
    s21_i = float(data[4])
    s12_r = float(data[5])
    s12_i = float(data[6])
    s22_r = float(data[7])
    s22_i = float(data[8])

    if frmt == "RI":
        s11 = complex(s11_r,s11_i)
        s21 = complex(s21_r,s21_i)
        s12 = complex(s12_r,s12_i)
        s22 = complex(s22_r,s22_i)
        #print(f"s11 = {s11}, s21 = {s21}, s12 = {s12}, s22 = {s22}")
    elif frmt == "MA":
        s11 = complex(s11_r*cos(s11_i),s11_r*sin(s11_i))
        s21 = complex(s21_r*cos(s21_i),s21_r*sin(s21_i))
        s12 = complex(s12_r*cos(s12_i),s12_r*sin(s12_i))
        s22 = complex(s22_r*cos(s22_i),s22_r*sin(s22_i))
    elif frmt == "DB":
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

    a_param = ((1 + s11) * (1 - s22) + (s12 * s21)) / (2 * s21)
    b_param = z_0 * ((1 + s11) * (1 + s22) - (s12 * s21)) / (2 * s21)
    c_param = ((1 - s11) * (1 - s22) - (s12 * s21)) / (z_0 * 2 * s21)
    d_param = ((1 - s11) * (1 + s22) + (s12 * s21)) / (2 * s21)

    print(f"freq = {freq}, A = {a_param}, B = {b_param}, C = {c_param}, D = {d_param}")

    return [freq, a_param, b_param, c_param, d_param]

if __name__ == "__main__":
    main()
