#!/usr/bin/env python3

import numpy as np
import pandas as pd
import os, sys
from pathlib import Path
import regex as re

def load_path(rel_path):
    """
    Gets the exact file path relative to this script executable location
    Used with a scripting environment (e.g. google colab or jupyter notebooks)

    Parameters
    ----------
    rel_path : str
        The path to the file

    Returns
    -------
    str
        A string containing the exact file path needed
    """
    current_folder = globals()['_dh'][0]
    p = os.path.join(current_folder, rel_path)
    return p

def load_file(f_name):
    p = Path(__file__).with_name(f_name)
    return p


args = sys.argv
# set defaults
vfile = 'adder2-comb.v'
stage = 3
direction = 'f'

for a in range(len(args)):
    if args[a] == '-v':
        vfile = args[a+1]
    elif args[a] == '-s':
        stage = int(args[a+1])
    elif args[a] == '-backward':
        direction = 'b'
    elif args[a] == '-forward': # not necessary
        direction = 'f'
    


path = str(load_file(vfile))

with open(vfile) as f:
    content = f.read().splitlines()

m_name = ""
inputs = []
curr = ""
for line in content:
    pattern = "[" + ";()," + "]"
    line = re.sub(pattern, "", line)

    if line.startswith("module"):
        m_name = line.split()[1]
        continue
    elif line.startswith("input"):
        sub_str = line.split()
        inputs.append(sub_str[1:])
        # search next lines

    elif line.startswith("output"):
        sub_str = line.split()
        inputs.append(sub_str[1:])
        # search next lines
    

# verilog File structure
#
# module name ( \vars, , ,  );
# input \var, , , ;
# output var, , , ;
# wire , , , , ;
# assign wire/output = (~/'+')in/out/wire &/| (~/'+')in/out/wire;
# endmodule
# note only variable name \1 has the slash, and it always carries it

# generate input/forward .v file with all inputs registered
# generate output/backward .v file with all outputs registered