#!/bin/bash
#### estimate energy drift
for energy in Etot_1
do
  python step_1_extract_amber_data.py drift NS "$energy"
  python step_2_plot_drift.py start end 5 image "$energy"
done

#### estimate avg 

for energy in DV/DL_1 
do
  python step_1_extract_amber_data.py no_drift NS "$energy"
  python step_2_plot_avg.py start end 5 no_image "$energy"
done
