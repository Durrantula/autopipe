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


def after_key(line, lst, rm_first=1):
    sub_str = line.split()
    int_names = []
    for i, s in enumerate(sub_str):
        if s.isdigit():
            sub_str[i] = "_" + s
    if rm_first:
        lst.append(sub_str[1:])
    else:
        lst.append(sub_str)
    
def assign_key(line, res, op1, op2, gate):
    sub_str = line.split()[1:] # remove 'assign'
    res_  = sub_str[0]
    op1_ = sub_str[2]
    gate.append(sub_str[3])
    op2_ = sub_str[4]

    if op1_.startswith("~"):
        if op1_[1:].isdigit():
            op1_ = op1_[0] + "_" + op1_[1:]
    elif op1_.isdigit():
        op1_ = "_" + op1_

    if op2_.startswith("~"):
        if op2_[1:].isdigit():
            op2_ = op2_[0] + "_" + op2_[1:]
    elif op2_.isdigit():
        op2_ = "_" + op2_

    if res_.isdigit():
        res_ = "_" + res_

    res.append(res_)
    op1.append(op1_)
    op2.append(op2_)
        
def init_assigns(assigns, res, op1, op2, gate):
    for i in range(len(res)):
        assigns.append("assign " + res[i] + " = " + op1[i] + " " + gate[i] + " " + op2[i])

def parse_verlg(path):
    with open(path) as f:
        content = f.read().splitlines()

    key_names = ("module", "input", "output", "wire", "assign", "endmodule")
    m_name = ""
    inputs = []
    outputs = []
    wires = []
    assigns = []
    res = []
    op1 = []
    op2 = []
    gate = []
    curr = ""
    for i, line in enumerate(content):
        pattern = "[" + "\\\\;()," + "]"
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
            assign_key(line, res, op1, op2, gate)
            # assigns.append(line)    # maybe split
            curr = ""               # assign new_n8_ = a0 & b0

        elif line.startswith("endmodule"):
            curr = ""
            break
        else:
            if curr == "input":
                if i != len(content) and content[i+1].startswith(key_names):
                    curr = ""
                after_key(line, inputs, rm_first=0)

            elif curr == "output":
                if i != len(content) and content[i+1].startswith(key_names):
                    curr = ""
                after_key(line, outputs, rm_first=0)

            elif curr == "wire":
                if i != len(content) and content[i+1].startswith(key_names):
                    curr = ""
                after_key(line, wires, rm_first=0)
    
    init_assigns(assigns, res, op1, op2, gate)
    return inputs, outputs, wires, assigns, m_name

def gen_module(inputs, outputs, m_name):
    
    mod = "module " + m_name + " ( clock,\n\t  "

    for line in inputs:
        for inp in line:
            mod = mod + inp + ", "
        mod = mod + "\n\t  "

    for line in outputs:
        for out in line:
            mod = mod + out + ", "
        mod = mod + "\n\t  "
    mod = mod[:-6] + ");\n"

    return mod

def gen_inputs(inputs):
    in_str = "\tinput clock; \n\tinput "
    for line in inputs:
        for inp in line:
            in_str = in_str + inp + ", "
        in_str = in_str + "\n\t"

    return in_str[:-4] + ";\n"

def gen_outputs(outputs):
    out_str = "\toutput "
    for line in outputs:
        for out in line:
            out_str = out_str + out + ", "
        out_str = out_str + "\n\t"

    return out_str[:-4] + ";\n"

def gen_reg(registers):
    reg_str = "\treg "
    for line in registers:
        for reg in line:
            reg_str = reg_str + reg + ", "
        reg_str = reg_str + "\n\t"

    return reg_str[:-4] + ";\n"

def gen_wires(wires, new_wires):
    wire1 = "\twire "
    for line in wires:
        for wire in line:
            wire1 = wire1 + wire + ", "
        wire1 = wire1 + "\n\t"
    wire1 = wire1[:-4] + ";\n"

    wire2 = "\twire "
    for line in new_wires:
        for wire in line:
            wire2 = wire2 + wire + ", "
        wire2 = wire2 + "\n\t"

    wire2 = wire2[:-4] + ";\n"

    return wire1 + wire2

def gen_assigns(portnd, wires, assigns, regs, stage):
    ret = "\t "
    for j in range(len(assigns)):
        # assign new_n8_ = a0 & b0;
        # assign new_n13_ = ~new_n11_ & ~new_n12_;
        # 
        counter = 0
        for k, ports in enumerate(portnd):
            for i in range(len(ports)):
                if counter == stage:
                    break
                counter = counter + 1
                idx = -1
                sub_str = assigns[j].split()
                # temporarily remove negations
                sub_str = [s.replace("~", "") for s in sub_str]

                if ports[i] in sub_str:
                    idx = assigns[j].rfind(ports[i]) # idx is left most index

                if idx != -1:
                    num = len(ports[i])
                    assigns[j] = assigns[j][:idx] + regs[k][i] + assigns[j][idx+num:]

        assigns[j] = "\t" + assigns[j] + ";\n"


def generate_forward(inputs, outputs, wires, assigns, m_name, stage):
    mod_str = gen_module(inputs, outputs, m_name)
    inp_str = gen_inputs(inputs)
    out_str = gen_outputs(outputs)

    registers = []
    regline = []
    counter = 0
    for line in inputs:
        regline.clear()
        if counter == stage:
            break
        for inp in line:
            if counter == stage:
                break
            counter = counter + 1
            regline.append("__" + m_name + "_s_" + inp.replace("\\", "_"))
        registers.append(regline.copy())

    reg_str = gen_reg(registers)

    # create always block string
    always_str = "\talways @ (posedge clock) begin\n"
    

    # assign these to inputs, and assign registers to these wires
    reg_i_wires = []
    regline = []
    for j, regs in enumerate(registers):
        regline.clear()
        for i in range(len(regs)):
            regline.append("new_w" + str(j) + str(i))
        reg_i_wires.append(regline.copy())

    wire_str = gen_wires(wires, reg_i_wires)

    gen_assigns(inputs, wires, assigns, registers, stage)

    assign_str = "".join(assigns)

    # make new assigns for the new wires and inputs
    new_assign_str = ""
    for j, regs in enumerate(reg_i_wires):
        for i in range(len(regs)):
            new_assign_str = new_assign_str + "\tassign " + regs[i] + " = " + inputs[j][i] + ";\n"
    # for i in range(len(reg_i_wires)):
    #     new_assign_str = new_assign_str + "\tassign " + reg_i_wires[i] + " = " + inputs[0][i] + ";\n"
    

    for i, regs in enumerate(registers):
        for j, reg in enumerate(regs):
            always_str = always_str + "\t\t" + reg + " <= " + reg_i_wires[i][j] + ";\n"
    always_str = always_str + "\tend\nendmodule\n"


    return mod_str + inp_str + out_str + reg_str + wire_str + assign_str + new_assign_str + always_str

def generate_backward(inputs, outputs, wires, assigns, m_name, stage):
    mod_str = gen_module(inputs, outputs, m_name)
    inp_str = gen_inputs(inputs)
    out_str = gen_outputs(outputs)

    registers = []
    regline = []
    counter = 0
    for line in outputs:
        regline.clear()
        if counter == stage:
            break
        for out in line:
            if counter == stage:
                break
            counter = counter + 1
            regline.append(out)
        registers.append(regline.copy())

    reg_str = gen_reg(registers)

    # create always block string
    always_str = "\talways @ (posedge clock) begin\n"
    

    # assign these to inputs, and assign registers to these wires
    reg_i_wires = []
    regline = []
    for j, regs in enumerate(registers):
        regline.clear()
        for i in range(len(regs)):
            regline.append("new_w" + str(j) + str(i))
        reg_i_wires.append(regline.copy())

    wire_str = gen_wires(wires, reg_i_wires)

    gen_assigns(outputs, wires, assigns, reg_i_wires, stage)

    assign_str = "".join(assigns)

    # make new assigns for the new wires and inputs
    # new_assign_str = ""
    # for i in range(len(reg_i_wires)):
    #     new_assign_str = new_assign_str + "\tassign " + reg_i_wires[i] + " = " + inputs[i] + ";\n"
    

    for i, regs in enumerate(registers):
        for j, reg in enumerate(regs):
            always_str = always_str + "\t\t" + reg + " <= " + reg_i_wires[i][j] + ";\n"
    always_str = always_str + "\tend\nendmodule\n"


    return mod_str + inp_str + out_str + reg_str + wire_str + assign_str + always_str

args = sys.argv
# set defaults
vfile = 'c880.v'
stage = 15
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

