#!/bin/bash
source /home/sp2546/softwares/amber24/amber.sh

#lams=(0.00000000 0.25000000 0.50000000 0.75000000 1.00000000)
lams=(0.00000000)
#dt=(0.001 0.002)
#dt=(0.002 0.0025 0.00333333 0.004)
#dt=(0.0005 0.001)
dt=(0.0005)

# Array of NPT 1 ns time steps and corresponding total steps
declare -A npt_steps
npt_steps=( ["0.0005"]=2000000 )
#npt_steps=( ["0.002"]=500000 ["0.0025"]=400000 ["0.00333333"]=300000 ["0.004"]=250000 )
#npt_steps=( ["0.0005"]=2000000 ["0.001"]=1000000 )
#npt_steps=(["0.001"]=1000000 ["0.002"]=500000)
# Array of NVE 10 ns time steps and corresponding total steps
declare -A nve_steps
#nve_steps=( ["0.002"]=5000000 ["0.0025"]=4000000 ["0.00333333"]=3000000 ["0.004"]=2500000 )
#nve_steps=( ["0.0005"]=20000000 ["0.001"]=10000000 )
#nve_steps=(["0.001"]=10000000 ["0.002"]=5000000)
# Array for frequencies based on the time step
declare -A freq_steps
freq_steps=( ["0.0005"]=2000 )
#freq_steps=( ["0.002"]=500 ["0.0025"]=400 ["0.00333333"]=300 ["0.004"]=250 )
#freq_steps=( ["0.0005"]=2000 ["0.001"]=1000 )
#freq_steps=( ["0.001"]=1000 ["0.002"]=500 )

gpu_ids=(0)  # List of available GPUs
#gpu_ids=(1)
gpu_count=${#gpu_ids[@]}
job_index=0  # Initialize job index for GPU assignment

topology="ti_L00.parm7"
initial_cord="inicord"
input_paths="inputs"
amber="pmemd.cuda"
run_folder="run"

## Create necessary directories
mkdir -p "$run_folder"
mkdir -p "$input_paths"  # Create inputs directory

max_jobs=1  # Maximum number of concurrent jobs
declare -a pids=()  # Array to hold job PIDs

for lambda in "${lams[@]}"; do
    for dt in "${dt[@]}"; do
        # Assign GPU in round-robin fashion
        cuda=${gpu_ids[$((job_index % gpu_count))]}
        job_index=$((job_index + 1))
        npt_step=${npt_steps[$dt]}     # Get the npt_step based on dt
        nve_step=${nve_steps[$dt]}     # Get the nve_step based on dt
        freq=${freq_steps[$dt]}        # Get the frequency based on dt
        npt=${lambda}_npt
        nve=${lambda}_nve

        # Create input files with consistent naming
        cat << EOF > "$input_paths/${npt}_${dt}.mdin"

morph rpcamp into camp charges and O -> S
 &cntrl
   ntr=0,
   nstlim =${npt_step}, 
   ntx=1, irest=0, ntb=2, ntpr=${freq}, ig=-1,
   ntp=1, taup=1.0, pres0 = 1.0,
   barostat = 2, mcbarint = 100,
   dt=${dt}, nrespa=1,
   ntt=3, gamma_ln = 2,
   temp0 = 300.0, tempi = 300.0, tautp=2.0, 
   ntc=2, ntf=1, tol=0.000001,
   ntwr = ${freq}, ntwx=0,
   cut                 = 8.5,
   iwrap=1, 
 /
EOF

#        cat << EOF > "$input_paths/${nve}_${dt}.mdin"
#
#morph rpcamp into camp charges and O -> S
# &cntrl
#   ntr=0,
#   nstlim =${nve_step}, 
#   ntx=5, irest=1, ntpr=${freq}, ig=-1,
#   ntp=0, ntb=1, ntt=0,  
#!  taup=1.0, tempi=300.0,
#!  barostat = 2, mcbarint = 100,
#   dt=${dt}, nrespa=1,
#!  gamma_ln = 2, temp0 = 300., tautp=2.0,
#   ntc=2, ntf=1, tol=0.000001,
#   ntwr = ${freq}, ntwx=0,
#   icfe=1,  ifsc=1, clambda=${lambda},
#   timask1             = ':1',
#   timask2             = ':2',
#   scmask1             = ':1',              ! softcore region 1
#   scmask2             = ':2',              ! softcore region 2
#   cut                 = 8.5,
#   tishake             = 0,
#   iwrap=1, nscm=0,
# /
#EOF

        # Generate job script for this lambda and dt
        job_script="job_${lambda}_${dt}.sh"

        cat << EOF > "$job_script"
#!/bin/bash
source /home/sp2546/softwares/amber24/amber.sh

topology="${topology}"
initial_cord="${initial_cord}"
input_paths="${input_paths}"
amber="${amber}"
run_folder="${run_folder}"
lambda="${lambda}"
npt="${npt}"
nve="${nve}"
dt="${dt}"

export CUDA_VISIBLE_DEVICES=${cuda}

# Run the NPT simulation
\${amber} -O \\
    -p \${topology} \\
    -c \${initial_cord}/out_L00.rst7 \\
    -i \${input_paths}/\${npt}_\${dt}.mdin \\
    -o \${run_folder}/\${npt}_\${dt}.mdout \\
    -r \${run_folder}/\${npt}_\${dt}.rst7 \\
    -x \${run_folder}/\${npt}_\${dt}.nc \\
    -inf \${run_folder}/\${npt}_\${dt}.mdinfo

## Run the NVE simulation starting from the NPT output
#\${amber} -O \\
#    -p \${topology} \\
#    -c \${run_folder}/\${npt}_\${dt}.rst7 \\
#    -i \${input_paths}/\${nve}_\${dt}.mdin \\
#    -o \${run_folder}/\${nve}_\${dt}.mdout \\
#    -r \${run_folder}/\${nve}_\${dt}.rst7 \\
#    -x \${run_folder}/\${nve}_\${dt}.nc  \\
#    -inf \${run_folder}/\${nve}_\${dt}.mdinfo \\
#    -AllowSmallBox
#echo "Completed simulations for lambda=\${lambda}, dt=\${dt}"
EOF

        # Make the job script executable
        chmod +x "$job_script"

        # Run the job script in the background
        nohup ./"$job_script" > "nohup_${lambda}_${dt}.out" 2>&1 &
        pid=$!
        pids+=("$pid")
        echo "Started job $job_script with PID $pid on GPU $cuda"

        # If max_jobs reached, wait until any job finishes
        while [ ${#pids[@]} -ge $max_jobs ]; do
            sleep 1  # Wait a second before checking
            # Check for finished jobs
            new_pids=()
            for pid in "${pids[@]}"; do
                if kill -0 "$pid" 2>/dev/null; then
                    new_pids+=("$pid")
                else
                    echo "Job with PID $pid has finished"
                fi
            done
            pids=("${new_pids[@]}")
        done

        echo "Generated $job_script and submitted for lambda=${lambda}, dt=${dt}"
    done
done

# Wait for all remaining jobs to finish
wait

echo "All jobs have completed."
