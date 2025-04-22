#!/bin/bash

# Arrays and variables from your original script
env="aq"
lams=("0.00000000" "0.25000000" "0.50000000" "0.75000000" "1.00000000")

# Array of NVE 100 ns time steps and corresponding total steps
declare -A nve_steps
nve_steps=( ["0.0005"]=200000000 ["0.001"]=100000000 ["0.002"]=50000000 ["0.0025"]=40000000 ["0.00333333"]=30000000 ["0.004"]=25000000 )

run_folder="run"

for lambda in "${lams[@]}"; do
    for dt in "${!nve_steps[@]}"; do
        nve="${lambda}_nve"
        output="${nve}_${dt}"

        mdout="${run_folder}/${output}.mdout"

        if [ ! -f "${mdout}" ] || ! grep -q "Setup CPU time:" "${mdout}"; then
            echo "Resubmitting job for lambda=${lambda}, dt=${dt}"
            sbatch "job_${lambda}_${dt}.sh"
        else
            echo "Job for lambda=${lambda}, dt=${dt} completed successfully."
        fi
    done
done

