# autopipe
This project automates the pipelining of combinational verilog files using forward or backward propagation.

The automation tool is written in Python and does not require compiliation.

The tool uses abc, and in order to utilize that application the autopipe.py and and .v files must be moved to the /abc folder.

The tool has 3 command line arguments:
1) -v <combinational.v>
2) -s <# of stages>
3) -forward or -backward
Note: When running the tool, the <combinational.v> file being read must be in the /abc folder. 

The command should look similar to this:
python3 autopipe.py -v adder2-comb.v -s 4 -forward

The output (latches, delay, area, node #, edge #) from abc is printed to the terminal.