## Auto-pipeline

### Examples (2-bit adder)

```bash
# combinational design
adder2-comb.v

# inserting latches at the input size
adder2-seq-input.v

# inserting latches at the output size
adder2-seq-output.v

# use retiming to auto-pipeline the circuits and evaluate the delay/area/#latch after technology mapping
# load commands into abc, e.g., 
./abc -c "read adder2-seq-input.v; strash; retime; read aig.genlib; map; print_stats" 

# you should develop tool to automatically generate xxx-input.v and xxx-output.v; benchmarks are included in benchmarks/
# then, compare the quality of results (QoR) of these two designs using the above listed flow
# discuss your results
```
