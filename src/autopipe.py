#!/usr/bin/env python3

import numpy as np
import pandas as pd
import os, sys
from pathlib import Path
import regex as re
import subprocess


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
        line = re.sub(pattern, "", line).strip()

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
    
    return inputs[0], outputs[0], wires[0], assigns, m_name

def gen_module(inputs, outputs, m_name):
    
    mod = "module " + m_name + " ( clock,\n\t  "

    for inp in inputs:
        mod = mod + inp + ", "

    mod = mod + "\n\t  "
    for out in outputs:
        mod = mod + out + ", "

    mod = mod[:-2] + ");\n"

    return mod

def gen_inputs(inputs):
    in_str = "\tinput clock; \n\tinput "
    for inp in inputs:
        in_str = in_str + inp + ", "

    return in_str[:-2] + ";\n"

def gen_outputs(outputs):
    out_str = "\toutput "
    for out in outputs:
        out_str = out_str + out + ", "

    return out_str[:-2] + ";\n"

def gen_reg(registers):
    reg_str = "\treg "
    for reg in registers:
        reg_str = reg_str + reg + ", "

    return reg_str[:-2] + ";\n"

def gen_wires(wires, new_wires):
    wire1 = "\twire "
    for wire in wires:
        wire1 = wire1 + wire + ", "

    wire1 = wire1[:-2] + ";\n"

    wire2 = "\twire "
    for wire in new_wires:
        wire2 = wire2 + wire + ", "

    wire2 = wire2[:-2] + ";\n"

    return wire1 + wire2

def gen_assigns(ports, wires, assigns, regs, stage):
    ret = "\t "
    for j in range(len(assigns)):
        # assign new_n8_ = a0 & b0;
        # assign new_n13_ = ~new_n11_ & ~new_n12_;
        # 
        counter = 0
        for i in range(len(ports)):
            if counter == stage:
                break
            counter = counter + 1
            idx = assigns[j].find(ports[i]) # idx is left most index
            if idx != -1:
                num = len(ports[i])
                assigns[j] = assigns[j][:idx] + regs[i] + assigns[j][idx+num:]

        assigns[j] = "\t" + assigns[j] + ";\n"


def generate_forward(inputs, outputs, wires, assigns, m_name, stage):
    mod_str = gen_module(inputs, outputs, m_name)
    inp_str = gen_inputs(inputs)
    out_str = gen_outputs(outputs)

    registers = []
    counter = 0
    for inp in inputs:
        if counter == stage:
            break
        counter = counter + 1
        registers.append("__" + m_name + "_s_" + inp.replace("\\", "_"))
    # registers = ["__" + m_name + "_s_" + inp for inp in inputs]

    reg_str = gen_reg(registers)

    # create always block string
    always_str = "\talways @ (posedge clock) begin\n"
    

    # assign these to inputs, and assign registers to these wires
    reg_i_wires = []
    for i in range(len(registers)):
        reg_i_wires.append("new_w" + str(i))

    wire_str = gen_wires(wires, reg_i_wires)

    gen_assigns(inputs, wires, assigns, registers, stage)

    assign_str = "".join(assigns)

    # make new assigns for the new wires and inputs
    new_assign_str = ""
    for i in range(len(reg_i_wires)):
        new_assign_str = new_assign_str + "\tassign " + reg_i_wires[i] + " = " + inputs[i] + ";\n"
    

    for i, reg in enumerate(registers):
        always_str = always_str + "\t\t" + reg + " <= " + reg_i_wires[i] + ";\n"
    always_str = always_str + "\tend\nendmodule\n"


    return mod_str + inp_str + out_str + reg_str + wire_str + assign_str + new_assign_str + always_str

def generate_backward(inputs, outputs, wires, assigns, m_name, stage):
    mod_str = gen_module(inputs, outputs, m_name)
    inp_str = gen_inputs(inputs)
    out_str = gen_outputs(outputs)

    registers = outputs[:stage]
    for i in range(len(registers)):
        registers[i].replace("\\", "__")
    reg_str = gen_reg(registers)

    # create always block string
    always_str = "\talways @ (posedge clock) begin\n"
    

    # assign these to inputs, and assign registers to these wires
    reg_i_wires = []
    for i in range(len(registers)):
        reg_i_wires.append("new_w" + str(i))

    wire_str = gen_wires(wires, reg_i_wires)

    gen_assigns(registers, wires, assigns, reg_i_wires, stage)

    assign_str = "".join(assigns)

    # make new assigns for the new wires and inputs
    # new_assign_str = ""
    # for i in range(len(reg_i_wires)):
    #     new_assign_str = new_assign_str + "\tassign " + reg_i_wires[i] + " = " + inputs[i] + ";\n"
    

    for i, reg in enumerate(registers):
        always_str = always_str + "\t\t" + reg + " <= " + reg_i_wires[i] + ";\n"
    always_str = always_str + "\tend\nendmodule\n"


    return mod_str + inp_str + out_str + reg_str + wire_str + assign_str + always_str

args = sys.argv
# set defaults
vfile = 'c17.v'
stage = 4
direction = 'f'

for a in range(len(args)):
    if args[a] == '-v':
        vfile = args[a+1]
    elif args[a] == '-s':
        stage = int(args[a+1])
    elif args[a] == '-backward':
        direction = 'b'
    elif args[a] == '-forward':
        direction = 'f'
    


path = str(load_file(vfile))

inputs, outputs, wires, assigns, m_name = parse_verlg(path)

if direction == 'f':
    seq_v = generate_forward(inputs, outputs, wires, assigns, m_name, stage)


    seq_file = open(vfile[:-2] + "-seq-input.v", "w")
    seq_file.write(seq_v)
    seq_file.close()

elif direction == 'b':
    seq_v = generate_backward(inputs, outputs, wires, assigns, m_name, stage)


    seq_file = open(vfile[:-2] + "-seq-out.v", "w")
    seq_file.write(seq_v)
    seq_file.close()


vname = seq_file.name

print("\n\nRunning ABC on combinational input design:\n\n")
# combinational
subprocess.run("./abc -c \"read " + path + " ;aig.genlib;map;print_stats;\"",
                shell=True)

print("\n\nRunning ABC on sequential output design:\n\n")
# sequential
subprocess.run("./abc -c \"read " + vname + " ;strash;retime;read aig.genlib;map;print_stats\"",
                shell=True)

