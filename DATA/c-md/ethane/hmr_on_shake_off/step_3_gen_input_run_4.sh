#!/bin/bash
#source /home/sp2546/softwares/amber22/amber.sh
env="aq"
lams=("0.00000000")

# Array of NPT 1 ns time steps and corresponding total steps
declare -A npt_steps
npt_steps=( ["0.0005"]=2000000 ["0.001"]=1000000 ["0.002"]=500000 ["0.0025"]=400000 ["0.00333333"]=300000 ["0.004"]=250000 )

# Array of NVE 100 ns time steps and corresponding total steps
declare -A nve_steps
nve_steps=( ["0.0005"]=200000000 ["0.001"]=100000000 ["0.002"]=50000000 ["0.0025"]=40000000 ["0.00333333"]=30000000 ["0.004"]=25000000 )

# Array for frequencies based on the time step
declare -A freq_steps
freq_steps=( ["0.0005"]=2000 ["0.001"]=1000 ["0.002"]=500 ["0.0025"]=400 ["0.00333333"]=300 ["0.004"]=250 )

## Array for frequencies based on the time step
#declare -A cudas
#cudas=( ["0.0005"]=0 ["0.001"]=1 ["0.002"]=2 ["0.004"]=3 )

topology="out_hmr_L00.parm7"
initial_cord="inicord"
input_paths="inputs"
amber="pmemd.cuda"
run_folder="run"

## Create necessary directories
mkdir -p "$run_folder"
mkdir -p "$input_paths"  # Create inputs directory

for lambda in "${lams[@]}"; do
    for dt in "${!nve_steps[@]}"; do
	#cuda=${cudas[$dt]}
	npt_step=${npt_steps[$dt]}     # Get the npt_step based on dt
        nve_step=${nve_steps[$dt]}  # Get the total_step based on dt
        freq=${freq_steps[$dt]}        # Get the frequency based on dt
	npt=${lambda}_npt
        nve=${lambda}_nve

#        # Create input files with consistent naming
#        cat << EOF > "$input_paths/${npt}_${dt}.mdin"
#morph rpcamp into camp charges and S -> O
# &cntrl
#   ntr=0,
#   nstlim =${npt_step}, 
#   ntx=1, irest=0, ntb=2, ntpr=${freq}, ig=-1,
#   ntp=1, taup=1.0, pres0 = 1.0,
#   barostat = 2, mcbarint = 100,
#   dt=${dt}, nrespa=1,
#   ntt=3, gamma_ln = 2,
#   temp0 = 300.0, tempi = 300.0, tautp=2.0, 
#   ntc=2, ntf=1, tol=0.000001,
#   ntwr = ${freq}, ntwx=0,
#   icfe=1, ifsc=1, clambda=${lambda},
#   timask1             = ':1',
#   timask2             = ':2',
#   scmask1             = ':1',              ! softcore region 1
#   scmask2             = ':2',              ! softcore region 2
#   cut                 = 8.5,
#   tishake             = 0,
#   iwrap=1, nscm=0,
# /
#EOF

        cat << EOF > "$input_paths/${nve}_${dt}.mdin"
morph rpcamp into camp charges and S -> O
 &cntrl
   ntr=0,
   nstlim =${nve_step}, 
   ntx=5, irest=1, ntpr=${freq}, ig=-1,
   ntp=0, ntb=1, ntt=0,  
!  taup=1.0, tempi=300.0,
!  barostat = 2, mcbarint = 100,
   dt=${dt}, nrespa=1,
!  gamma_ln = 2, temp0 = 300., tautp=2.0,
   ntc=1, ntf=1, tol=0.000001,
   ntwr = ${freq}, ntwx=0,
   cut                 = 9,
   iwrap=1, 
 /
EOF

        # Generate job script for this lambda and dt
        job_script="job_${lambda}_${dt}.sh"

        cat << EOF > "$job_script"
#!/bin/bash
#SBATCH --job-name=${env}_${lambda}_${dt}
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=3-00:00:00
#SBATCH --error=job_${lambda}_${dt}.err
#SBATCH --output=job_${lambda}_${dt}.out
#SBATCH --mail-user=saikat.pal@rutgers.edu
#SBATCH --nodelist=gpu[019-020,022-026]

module purge
module use /projects/community/modulefiles
module load gcc/10.2.0/openmpi/4.0.5-bz186
module load cmake/3.19.5-bz186
module load cuda/11.7.1

source /home/sp2546/softwares/AMBER/amber24/amber.sh

topology="${topology}"
initial_cord="${initial_cord}"
input_paths="${input_paths}"
amber="${amber}"
run_folder="${run_folder}"
lambda="${lambda}"
npt="${npt}"
nve="${nve}"
dt="${dt}"


## Run the NPT simulation
#\${amber} -O \\
#    -p \${topology} \\
#    -c \${initial_cord}/inpcrd \\
#    -i \${input_paths}/\${npt}_\${dt}.mdin \\
#    -o \${run_folder}/\${npt}_\${dt}.mdout \\
#    -r \${run_folder}/\${npt}_\${dt}.rst7 \\
#    -x \${run_folder}/\${npt}_\${dt}.nc \\
#    -inf \${run_folder}/\${npt}_\${dt}.mdinfo
#
# Run the NVE simulation starting from the NPT output
\${amber} -O \\
    -p \${topology} \\
    -c \${initial_cord}/0.00000000_npt_0.0005.rst7 \\
    -i \${input_paths}/\${nve}_\${dt}.mdin \\
    -o \${run_folder}/\${nve}_\${dt}.mdout \\
    -r \${run_folder}/\${nve}_\${dt}.rst7 \\
    -x \${run_folder}/\${nve}_\${dt}.nc  \\
    -inf \${run_folder}/\${nve}_\${dt}.mdinfo \\
    -AllowSmallBox
echo "Completed simulations for lambda=\${lambda}, dt=\${dt}"
EOF

        # Make the job script executable and run it
        chmod +x "$job_script"
        sbatch "$job_script" 
        echo "Generated ${job_script} and submitted for lambda=${lambda}, dt=${dt}"
    done
done

