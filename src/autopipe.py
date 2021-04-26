#!/usr/bin/env python3

import numpy as np
import pandas as pd
import os, sys
from pathlib import Path
import hdlparse.verilog_parser as vlog

def load_path(rel_path):
    """
    Gets the exact file path relative to this script executable location

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


args = sys.argv
# set defaults
vfile = 'c880.v'
stage = 4
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
    
path = load_path(vfile)

# verilog File structure
#
# module name ( \vars, , ,  );
# input \var, , , ;
# output var, , , ;
# wire , , , , ;
# assign wire/output = (~/'+')in/out/wire &/| (~/'+')in/out/wire;
# endmodule
# note only variable name \1 has the slash, and it always carries it

