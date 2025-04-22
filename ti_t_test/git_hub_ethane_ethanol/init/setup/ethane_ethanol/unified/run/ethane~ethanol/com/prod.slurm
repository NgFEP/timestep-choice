#!/bin/bash
#SBATCH --job-name="pr_ethane~ethanol.slurm"
#SBATCH --output="pr_ethane~ethanol.slurm.slurmout"
#SBATCH --error="pr_ethane~ethanol.slurm.slurmerr"
#SBATCH --partition=general-long-gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --gres=gpu:8
#SBATCH --time=3-00:00:00

lams=(0.00000000 0.25000000 0.50000000 0.75000000 1.00000000)
# check if AMBERHOME is set
if [ -z "${AMBERHOME}" ]; then echo "AMBERHOME is not set" && exit 0; fi

EXE=${AMBERHOME}/bin/pmemd.cuda.MPI
echo "running replica ti"
mpirun -np ${#lams[@]} ${EXE} -rem 3 -remlog remt${trial}.log -ng ${#lams[@]} -groupfile inputs/ti.groupfile
