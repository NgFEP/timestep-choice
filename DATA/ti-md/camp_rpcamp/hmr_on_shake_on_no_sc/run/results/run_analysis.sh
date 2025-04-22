#!/bin/bash
#python step_1_extract_1.py drift NS Etot_1
#python step_8_extract.py start end 5 image Etot_1

for energy in Etot_1 EKtot_1 EPtot_1
do
  python step_1_extract_1.py drift NS "$energy"
  python step_8_extract.py start end 5 image "$energy"
done
