This repository contains the files of simulations for the timestep choice manuscript (current version available at https://doi.org/10.26434/chemrxiv-2025-jwkz1)

## Test run Example

To run the simulation using the provided script, download the necessary files from the links below:

- **Topology file:** [`ti_hmr_L00.parm7`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_on/ti_hmr_L00.parm7)
- **Initial coordinate file:** [`0.00000000_npt_0.0005.rst7`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_on/inicord/0.00000000_npt_0.0005.rst7)
- **Input files:** [`inputs/`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_on/inputs)

## Batch Script for NVE Simulations using AMBER

This Bash script `sample_hmr_on_shake_on_step_3_nve.sh` [Link](https://github.com/NgFEP/timestep-choice/blob/main/DATA/c-md/ethane/hmr_on_shake_on/sample_hmr_on_shake_on_step_3_nve.sh) automates the setup and submission of molecular dynamics simulations under NVE ensembles across different time steps and lambda windows using AMBER on an HPC cluster. 

## Automated NVE Simulation Submission Script (Single Lambda)

This script is designed to automate the setup and submission of **100 ns NVE simulations** for a single lambda value using **AMBER** with CUDA acceleration on a SLURM-based HPC cluster.

---

### System Setup

- **Lambda value:** `0.00000000`
- **Topology file:** `ti_hmr_L00.parm7`
- **Starting restart file for all NVE simulations:** `0.00000000_npt_0.0005.rst7`

---

### Time Step Configurations

| Time Step (ps) | NVE Total Steps | Output Frequency |
|----------------|------------------|------------------|
| 0.0005         | 200,000,000      | 2000             |
| 0.001          | 100,000,000      | 1000             |
| 0.002          | 50,000,000       | 500              |
| 0.0025         | 40,000,000       | 400              |
| 0.00333333     | 30,000,000       | 300              |
| 0.004          | 25,000,000       | 250              |

---

### Files and Structure

- **Input folder:** `inputs/` — auto-generated NVE `.mdin` files
- **Run folder:** `run/` — simulation outputs
- **Job scripts:** `job_{lambda}_{dt}.sh` — one per timestep

Each `.mdin` file is uniquely created per timestep, with key MD parameters for NVE runs.

---

### SLURM Job Script Sample

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
  -p ti_hmr_L00.parm7 \
  -c inicord/0.00000000_npt_0.0005.rst7 \
  -i inputs/0.00000000_nve_0.001.mdin \
  -o run/0.00000000_nve_0.001.mdout \
  -r run/0.00000000_nve_0.001.rst7 \
  -x run/0.00000000_nve_0.001.nc \
  -inf run/0.00000000_nve_0.001.mdinfo \
  -AllowSmallBox
```
After executing the `sample_hmr_on_shake_on_step_3_nve.sh` script, the following output files will be generated by the AMBER package for each simulation:

- `.mdout` — standard output log of the simulation
- `.nc` — trajectory file in NetCDF format
- `.rst7` — final restart coordinate file
- `.mdinfo` — performance and energy statistics
These files will be saved in the specified `run/` directory.
---
### Analysis

To analyze the simulation results, follow these steps:
1. Create a folder named `results`
   ```
   mkdir results
   ```

3. Download the analysis scripts:
   - [`step_1_extract_1.py`](https://github.com/NgFEP/timestep-choice/blob/main/DATA/c-md/camp/hmr_on_shake_on/run/results/step_1_extract_1.py)
   - [`step_8_extract.py`](https://github.com/NgFEP/timestep-choice/blob/main/DATA/c-md/camp/hmr_on_shake_on/run/results/step_8_extract.py)

4. Download and execute the analysis runner script:
   - [`run_analysis.sh`](https://github.com/NgFEP/timestep-choice/blob/main/DATA/c-md/camp/hmr_on_shake_on/run/results/run_analysis.sh)

The script will automate post-processing and data extraction using the provided Python tools. Make sure Python and any required libraries are installed in your environment before running the analysis.



## Directory: DATA ##
## subdirectory: c-md ##

### Camp System
**Path:** [`DATA/c-md/camp`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp)

- **hmr_off_shake_off**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_off_shake_off)

  - **Topology:** `ti_L00.parm7`  
    *(Located at `DATA/c-md/camp/hmr_off_shake_on`)*
  - **Initial coordinate:** `0.00000000_npt_0.0005.rst7`  
    *(Located at `DATA/c-md/camp/hmr_off_shake_on/inicord`)*
  - **mdin:**
    *(Located at `DATA/c-md/camp/hmr_off_shake_off/inputs`)*
    
- **hmr_off_shake_on**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_off_shake_on)

  - **Topology:** `ti_L00.parm7`  
    *(Located at `DATA/c-md/camp/hmr_off_shake_on`)*
  - **Initial coordinate:** `0.00000000_npt_0.0005.rst7`  
    *(Located at `DATA/c-md/camp/hmr_off_shake_on/inicord`)*
  - **mdin:**
    *(Located at `DATA/c-md/camp/hmr_off_shake_on/inputs`)*
    
- **hmr_on_shake_off**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_off)

  - **Topology:** `ti_hmr_L00.parm7`  
    *(Located at `DATA/c-md/camp/hmr_on_shake_off`)*
  - **Initial coordinate:** `out_L00.rst7`  
    *(Located at `DATA/c-md/camp/hmr_on_shake_off/inicord`)*
  - **mdin:**
    *(Located at `DATA/c-md/camp/hmr_on_shake_off/inputs`)*

- **hmr_on_shake_on**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_on)

  - **Topology:** `ti_hmr_L00.parm7`  
    *(Located at `DATA/c-md/camp/hmr_on_shake_on`)*
  - **Initial coordinate:** `out_L00.rst7`  
    *(Located at `DATA/c-md/camp/hmr_on_shake_on/inicord`)*
  - **mdin:**
    *(Located at `DATA/c-md/camp/hmr_on_shake_on/inputs`)*

### Ethane System
**Path:** [`DATA/c-md/ethane`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/ethane)
- **hmr_off_shake_off**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/ethane/hmr_off_shake_off)

  - **Topology:** `out_L00.parm7`  
    *(Located at `DATA/c-md/ethane/hmr_off_shake_on`)*
  - **Initial coordinate:** `0.00000000_npt_0.0005.rst7`  
    *(Located at `DATA/c-md/ethane/hmr_off_shake_on/inicord`)*
  - **mdin:**
    *(Located at `DATA/c-md/ethane/hmr_off_shake_off/inputs`)*
    
- **hmr_off_shake_on**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/ethane/hmr_off_shake_on)

  - **Topology:** `out_L00.parm7`  
    *(Located at `DATA/c-md/ethane/hmr_off_shake_on`)*
  - **Initial coordinate:** `0.00000000_npt_0.0005.rst7`  
    *(Located at `DATA/c-md/ethane/hmr_off_shake_on/inicord`)*
  - **mdin:**
    *(Located at `DATA/c-md/ethane/hmr_off_shake_on/inputs`)*
    
- **hmr_on_shake_off**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/ethane/hmr_on_shake_off)

  - **Topology:** `out_hmr_L00.parm7`  
    *(Located at `DATA/c-md/camp/hmr_on_shake_off`)*
  - **Initial coordinate:** `out_L00.rst7`  
    *(Located at `DATA/c-md/ethane/hmr_on_shake_off/inicord`)*
  - **mdin:**
    *(Located at `DATA/c-md/ethane/hmr_on_shake_off/inputs`)*

- **hmr_on_shake_on**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/ethane/hmr_on_shake_on)

  - **Topology:** `out_hmr_L00.parm7`  
    *(Located at `DATA/c-md//hmr_on_shake_on`)*
  - **Initial coordinate:** `out_L00.rst7`  
    *(Located at `DATA/c-md/ethane/hmr_on_shake_on/inicord`)*
  - **mdin:**
    *(Located at `DATA/c-md/ethane/hmr_on_shake_on/inputs`)*

## subdirectory ti-md ## 
### camp to rp-camp transformation
**Path:** [`DATA/ti-md/camp_rpcamp`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti-md/camp_rpcamp)

- **hmr_on_shake_on_all_sc**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti-md/camp_rpcamp/hmr_on_shake_on_all_sc)

  - **Topology:** `ti_hmr.parm7`  
    *(Located at `DATA/ti-md/camp_rpcamp/hmr_on_shake_on_all_sc`)*
  - **Initial coordinate:** `0.00000000_npt_0.0005.rst7`  
    *(Located at `DATA/ti-md/camp_rpcamp/hmr_on_shake_on_all_sc/inicord`)*
  - **mdin:**
    *(Located at `DATA/ti-md/camp_rpcamp/hmr_on_shake_on_all_sc/inputs`)*

- **hmr_on_shake_on_no_sc**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti-md/camp_rpcamp/hmr_on_shake_on_no_sc)

  - **Topology:** `ti_hmr.parm7`  
    *(Located at `DATA/ti-md/camp_rpcamp/hmr_on_shake_on_no_sc`)*
  - **Initial coordinate:** `0.00000000_npt_0.0005.rst7`  
    *(Located at `DATA/ti-md/camp_rpcamp/hmr_on_shake_on_no_sc/inicord`)*
  - **mdin:**
    *(Located at `DATA/ti-md/camp_rpcamp/hmr_on_shake_on_no_sc/inputs`)*

- **hmr_on_shake_on_one_sc**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti-md/camp_rpcamp/hmr_on_shake_on_one_sc)

  - **Topology:** `ti_hmr.parm7`  
    *(Located at `DATA/ti-md/camp_rpcamp/hmr_on_shake_on_one_sc`)*
  - **Initial coordinate:** `0.00000000_npt_0.0005.rst7`  
    *(Located at `DATA/ti-md/camp_rpcamp/hmr_on_shake_on_one_sc/inicord`)*
  - **mdin:**
    *(Located at `DATA/ti-md/camp_rpcamp/hmr_on_shake_on_one_sc/inputs`)*

### ethane to ethanol transformation
**Path:** [`DATA/ti-md/ethane_ethanol/`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti-md/ethane_ethanol/)
- **hmr_on_shake_on_3_atom_sc**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti-md/ethane_ethanol/hmr_on_shake_on_3_atom_sc)

  - **Topology:** `out_hmr.parm7`  
    *(Located at `DATA/ti-md/ti-md/ethane_ethanol/hmr_on_shake_on_3_atom_sc`)*
  - **Initial coordinate:** `0.00000000_npt_0.0005.rst7`  
    *(Located at `DATA/ti-md/ti-md/ethane_ethanol/hmr_on_shake_on_3_atom_sc/inicord`)*
  - **mdin:**
    *(Located at `DATA/ti-md/ti-md/ethane_ethanol/hmr_on_shake_on_3_atom_sc/inputs`)*

- **hmr_on_shake_on_all_sc**  
  [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti-md/ethane_ethanol/hmr_on_shake_on_all_sc)

  - **Topology:** `out_hmr.parm7`  
    *(Located at `DATA/ti-md/ti-md/ethane_ethanol/hmr_on_shake_on_all_sc`)*
  - **Initial coordinate:** `0.00000000_npt_0.0005.rst7`  
    *(Located at `DATA/ti-md/ti-md/ethane_ethanol/hmr_on_shake_on_all_sc/inicord`)*
  - **mdin:**
    *(Located at `DATA/ti-md/ti-md/ethane_ethanol/hmr_on_shake_on_all_sc/inputs`)*
    
 ## Subdirectory: `ti_t_test`

This directory contains input files for **Thermodynamic Integration (TI)** simulations to evaluate statistical consistency using a **t-test**. Each simulation runs for **10 ns** and is repeated **8 times** for robust statistical analysis.

**Path:** [`DATA/ti_t_test/`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti_t_test)

### ejm 42 to ejm 55 transformation

- **Repository Link:** [`git_hub_ejm_42~ejm_55`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti_t_test/git_hub_ejm_42~ejm_55)

---

#### Environment: `aq`
- **Path:** [`aq`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti_t_test/git_hub_ejm_42~ejm_55/aq)
- **Topology File:** `unisc.parm7`  
  *(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/aq`)*

lambda=0
*(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/aq/lambda0`)*

lambda=0.25
*(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/aq/lambda025`)*

lambda=0.5
*(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/aq/lambda05`)*

lambda=0.75
*(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/aq/lambda075`)*

lambda=1.00
*(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/aq/lambda1`)*

---

#### Environment: `com`
- **Path:** [`com`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti_t_test/git_hub_ejm_42~ejm_55/com)
- **Topology File:** `unisc.parm7`  
  *(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/com`)*

lambda=0
*(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/com/lambda0`)*

lambda=0.25
*(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/com/lambda025`)*

lambda=0.5
*(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/aq/lambda05`)*

lambda=0.75
*(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/com/lambda075`)*

lambda=1.00
*(Located at `DATA/ti_t_test/git_hub_ejm_42~ejm_55/com/lambda1`)*

---

### ethane to ethanol transformation
- **Repository Link:** [`git_hub_ethane_ethanol`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti_t_test/git_hub_ethane_ethanol)

---
- **all SC**
  
lambda=0
*(Located at `DATA/ti_t_test/git_hub_ethane_ethanol/SCAll_lambda0`)*

lambda=0.25
*(Located at `DATA/ti_t_test/git_hub_ethane_ethanol/SCAll_lambda025`)*

lambda=0.5
*(Located at `DATA/ti_t_test/git_hub_ethane_ethanol/SCAll_lambda05`)*

lambda=0.75
*(Located at `DATA/ti_t_test/git_hub_ethane_ethanol/SCAll_lambda075`)*

lambda=1.00
*(Located at `DATA/ti_t_test/git_hub_ethane_ethanol/SCAll_lambda1`)*

- **4/5-atom SC**

lambda=0
*(Located at `DATA/ti_t_test/git_hub_ethane_ethanol/lambda0`)*

lambda=0.25
*(Located at `DATA/ti_t_test/git_hub_ethane_ethanol/lambda025`)*

lambda=0.5
*(Located at `DATA/ti_t_test/git_hub_ethane_ethanol/lambda05`)*

lambda=0.75
*(Located at `DATA/ti_t_test/git_hub_ethane_ethanol/lambda075`)*

lambda=1.00
*(Located at `DATA/ti_t_test/git_hub_ethane_ethanol/lambda1`)*

---
### camp to rp-camp transformation
- **Repository Link:** [`git_hub_CampTI`](https://github.com/NgFEP/timestep-choice/tree/main/DATA/ti_t_test/git_hub_CampTI)
---
- **no SC**

lambda=0
*(Located at `DATA/ti_t_test/git_hub_CampTI/NoSC_lambda_0`)*

lambda=0.25
*(Located at `DATA/ti_t_test/git_hub_CampTI/NoSC_lambda_25`)*

lambda=0.5
*(Located at `DATA/ti_t_test/git_hub_CampTI/NoSC_lambda_05`)*

lambda=0.75
*(Located at `DATA/ti_t_test/git_hub_CampTI/NoSC_lambda_75`)*

lambda=1.00
*(Located at `DATA/ti_t_test/git_hub_CampTI/NoSC_lambda_1`)*

- **1 atom**

lambda=0
*(Located at `DATA/ti_t_test/git_hub_CampTI/SC_lambda_0`)*

lambda=0.25
*(Located at `DATA/ti_t_test/git_hub_CampTI/SC_lambda_25`)*

lambda=0.50
*(Located at `DATA/ti_t_test/git_hub_CampTI/SC_lambda_05`)*

lambda=0.75
*(Located at `DATA/ti_t_test/git_hub_CampTI/SC_lambda_75`)*

lambda=1.00
*(Located at `DATA/ti_t_test/git_hub_CampTI/SC_lambda_1`)*

- **all SC**

lambda=0
*(Located at `DATA/ti_t_test/git_hub_CampTI/SCAll_lambda_0`)*

lambda=0.25
*(Located at `DATA/ti_t_test/git_hub_CampTI/SCAll_lambda_25`)*

lambda=0.50
*(Located at `DATA/ti_t_test/git_hub_CampTI/SCAll_lambda_05`)*

lambda=0.75
*(Located at `DATA/ti_t_test/git_hub_CampTI/SCAll_lambda_75`)*

lambda=1.00
*(Located at `DATA/ti_t_test/git_hub_CampTI/SCAll_lambda_1`)*


# Output files: #
  Due to the file sizes, all input and output files are available through anonymous [ftp to 165.230.21.2.](ftp://165.230.21.2/)  
