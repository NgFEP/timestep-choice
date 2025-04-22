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

This Bash script automates the setup and submission of molecular dynamics simulations under NPT and NVE ensembles across different time steps and lambda windows using AMBER on an HPC cluster.

### 📂 Directory Structure

- `run/`: Output directory for simulation results
- `inputs/`: Auto-generated input files for NPT and NVE simulations

### 🔧 Script Configuration

- **Environment:** `aq`
- **Lambdas:** `0.00000000`, `0.25000000`, `0.50000000`, `0.75000000`, `1.00000000`
- **Time Steps & Simulation Lengths:**
  - **NPT (1 ns):**
    - 0.0005 ps → 2,000,000 steps
    - 0.001 ps → 1,000,000 steps
    - 0.002 ps → 500,000 steps
    - 0.0025 ps → 400,000 steps
    - 0.00333333 ps → 300,000 steps
    - 0.004 ps → 250,000 steps
  - **NVE (100 ns):**
    - 0.0005 ps → 200,000,000 steps
    - 0.001 ps → 100,000,000 steps
    - 0.002 ps → 50,000,000 steps
    - 0.0025 ps → 40,000,000 steps
    - 0.00333333 ps → 30,000,000 steps
    - 0.004 ps → 25,000,000 steps

### 🛠 Input Files

For each combination of lambda and timestep, the script generates:

- `inputs/{lambda}_npt_{dt}.mdin`: NPT input file
- `inputs/{lambda}_nve_{dt}.mdin`: NVE input file

Each input includes relevant control parameters such as pressure coupling (for NPT), temperature regulation, and softcore region definition (`timask` and `scmask`).

### 🚀 SLURM Job Script

For each lambda and timestep, the script generates and submits a SLURM batch job:

- **Job Script:** `job_{lambda}_{dt}.sh`
- **Job Configuration:**
  - GPU partition, 1 GPU
  - 1 node, 1 CPU, 32GB memory
  - Runtime: up to 3 days
  - Output/Error logs: `job_{lambda}_{dt}.out` and `.err`
- **Execution:**
  - Loads necessary modules (GCC, OpenMPI, CUDA)
  - Sources AMBER environment
  - Runs NVE simulation (NPT lines are included but commented out)

> **Note:** The NVE simulation starts from the `0.0005 ps` timestep NPT output file, regardless of the NVE timestep being tested.

### 📝 Customization

- You can uncomment the NPT execution block if you want to run NPT simulations.
- Modify SLURM directives (e.g., `--mail-user`, `--nodelist`) as per your cluster setup.

### 📌 Example Output

After running the script, you will find:




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
