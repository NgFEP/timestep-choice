#!/bin/bash
for energy in Etot_1 
do
  python step_1_extract_1.py drift NS "$energy"
  python step_8_extract.py start end 5 image "$energy"
done
