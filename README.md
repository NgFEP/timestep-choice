This repository contains the files of simulations for the timestep choice manuscript (current version available at https://doi.org/10.26434/chemrxiv-2025-jwkz1)

# Input files: #
## Directory: c-md ##

### Camp System
**Path:** [`DATA/c-md/camp`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp)

- **hmr_off_shake_off**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_off_shake_off)

  - **Topology:** `ti_L00.parm7`  
    *(Located at `DATA/c-md/camp/hmr_off_shake_on`)*
  - **Initial coordinate:** `0.00000000_npt_0.0005.rst7`  
    *(Located at `DATA/c-md/camp/hmr_off_shake_on/inicord`)*

- **hmr_off_shake_on**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_off_shake_on)

  - **Topology:** `ti_L00.parm7`  
    *(Located at `DATA/c-md/camp/hmr_off_shake_on`)*
  - **Initial coordinate:** `0.00000000_npt_0.0005.rst7`  
    *(Located at `DATA/c-md/camp/hmr_off_shake_on/inicord`)*

- **hmr_on_shake_off**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_off)

  - **Topology:** `ti_hmr_L00.parm7`  
    *(Located at `DATA/c-md/camp/hmr_on_shake_off`)*
  - **Initial coordinate:** `out_L00.rst7`  
    *(Located at `DATA/c-md/camp/hmr_on_shake_off/inicord`)*

- **hmr_on_shake_on**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_on)

  - **Topology:** `ti_hmr_L00.parm7`  
    *(Located at `DATA/c-md/camp/hmr_on_shake_on`)*
  - **Initial coordinate:** `out_L00.rst7`  
    *(Located at `DATA/c-md/camp/hmr_on_shake_on/inicord`)*

**Example**

Download the topology [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_on/ti_hmr_L00.parm7), initial coordinate [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_on/inicord/0.00000000_npt_0.0005.rst7), and all input files [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_on/inputs) from the mentioned location.

## Batch Script for NPT and NVE Simulations using AMBER

This Bash script `sample_hmr_on_shake_on_step_3_nve.sh` [Link](https://github.com/NgFEP/timestep-choice/blob/main/DATA/c-md/ethane/hmr_on_shake_on/sample_hmr_on_shake_on_step_3_nve.sh) automates the setup and submission of molecular dynamics simulations under NPT and NVE ensembles across different time steps and lambda windows using AMBER on an HPC cluster. 

## 🔁 Automated NVE Simulation Submission Script (Single Lambda)

This script is designed to automate the setup and submission of **100 ns NVE simulations** for a single lambda value using **AMBER** with CUDA acceleration on a SLURM-based HPC cluster.

---

### 🧪 System Setup

- **Lambda value:** `0.00000000`
- **Topology file:** `out_hmr_L00.parm7`
- **Initial coordinate directory:** `inicord`
- **Starting restart file for all NVE simulations:** `0.00000000_npt_0.0005.rst7`

---

### 🧩 Time Step Configurations

| Time Step (ps) | NVE Total Steps | Output Frequency |
|----------------|------------------|------------------|
| 0.0005         | 200,000,000      | 2000             |
| 0.001          | 100,000,000      | 1000             |
| 0.002          | 50,000,000       | 500              |
| 0.0025         | 40,000,000       | 400              |
| 0.00333333     | 30,000,000       | 300              |
| 0.004          | 25,000,000       | 250              |

---

### 📄 Files and Structure

- **Input folder:** `inputs/` — auto-generated NVE `.mdin` files
- **Run folder:** `run/` — simulation outputs
- **Job scripts:** `job_{lambda}_{dt}.sh` — one per timestep

Each `.mdin` file is uniquely created per timestep, with key MD parameters for NVE runs.

---

### 🧠 Script Highlights

- Uses associative arrays (`declare -A`) to define timestep-dependent simulation length and frequencies.
- Generates `.mdin` files with appropriate AMBER parameters:
  - No thermostat/barostat (NVE ensemble)
  - Constant energy
  - 9 Å cutoff
  - iwrap = 1 to wrap coordinates
- SLURM job scripts include:
  - Resource requests (1 GPU, 32 GB RAM, 3 days wall time)
  - Module and environment setup
  - Execution via `pmemd.cuda` from AMBER 24

---

### 🧬 SLURM Job Script Sample (Auto-Generated)

```bash
#!/bin/bash
#SBATCH --job-name=aq_0.00000000_0.001
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=3-00:00:00
#SBATCH --error=job_0.00000000_0.001.err
#SBATCH --output=job_0.00000000_0.001.out
#SBATCH --mail-user=saikat.pal@rutgers.edu
#SBATCH --nodelist=gpu[019-020,022-026]

# Load necessary modules
module purge
module use /projects/community/modulefiles
module load gcc/10.2.0/openmpi/4.0.5-bz186
module load cmake/3.19.5-bz186
module load cuda/11.7.1

# Load AMBER
source /home/sp2546/softwares/AMBER/amber24/amber.sh

# Run NVE simulation
pmemd.cuda -O \
  -p out_hmr_L00.parm7 \
  -c inicord/0.00000000_npt_0.0005.rst7 \
  -i inputs/0.00000000_nve_0.001.mdin \
  -o run/0.00000000_nve_0.001.mdout \
  -r run/0.00000000_nve_0.001.rst7 \
  -x run/0.00000000_nve_0.001.nc \
  -inf run/0.00000000_nve_0.001.mdinfo \
  -AllowSmallBox




---

### Ethane System
**Path:** [`DATA/c-md/ethane`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/ethane)

## Directory: analysis_code ##

## Directory: conv_md ##

## Directory: ti ##

## Directory ti_t_test ## 
The input files for all TI simulations: 10ns each and repeated 8 times for t-test purposes.

# Output files: #
  Due to the file sizes, all input and output files are available through anonymous [ftp to 165.230.21.2.](ftp://165.230.21.2/)  
