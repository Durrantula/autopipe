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


def after_key(line, lst):
    sub_str = line.split()
    lst.append(sub_str[1:])

def parse_verlg(path):
    with open(path) as f:
        content = f.read().splitlines()

    key_names = ("module", "input", "output", "wire", "assign", "endmodule")
    m_name = ""
    inputs = []
    outputs = []
    wires = []
    assigns = []
    curr = ""
    for i, line in enumerate(content):
        pattern = "[" + ";()," + "]"
        line = re.sub(pattern, "", line)

        if line.startswith("module"):
            m_name = line.split()[1]
            continue

        elif line.startswith("input"):
            after_key(line, inputs)
            curr = "input"
            
        elif line.startswith("output"):
            after_key(line, outputs)
            curr = "output"

        elif line.startswith("wire"):
            after_key(line, wires)
            curr = "wire"

        elif line.startswith("assign"):
            assigns.append(line)    # maybe split
            curr = ""               # assign new_n8_ = a0 & b0

        elif line.startswith("endmodule"):
            curr = ""
            break
        else:
            if curr == "input":
                if i != len(content) and content[i+1].startswith(key_names):
                    curr = ""
                inputs.append(line.split())

            elif curr == "output":
                if i != len(content) and content[i+1].startswith(key_names):
                    curr = ""
                outputs.append(line.split())

            elif curr == "wire":
                if i != len(content) and content[i+1].startswith(key_names):
                    curr = ""
                wires.append(line.split())
    
    return inputs, outputs, wires, assigns, m_name


def generate_forward(inputs, outputs, wires, assigns, m_name):
    registers = ["\\" + m_name + "|s_" + inp for inp in inputs]

    # create always block string
    always_str = "always @ (posedge clock) begin\n"
    
    reg_o_wires = []
    for i in range(len(inputs)):
        reg_o_wires.append("new_w" + i)

    # make new assigns for the new wires and inputs

    for i, reg in enumerate(registers):
        always_str = always_str + reg + "<=" + reg_o_wires[i] + ";\n"

    # Everywhere we see an input[i] in an assign statement, we replace
    # the input[i] with reg_o_wires[i]??



    always_str = always_str + "end\nendmodule\n"

    big_string_lol = "BEEF"
    return big_string_lol




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

inputs, outputs, wires, assigns, m_name = parse_verlg(path)

forward_v = generate_forward(inputs, outputs, wires, assigns, m_name)


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