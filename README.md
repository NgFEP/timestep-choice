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

Download the topology [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_on), initial coordinate [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_on/inicord/0.00000000_npt_0.0005.rst7), and all input files [Link](https://github.com/NgFEP/timestep-choice/tree/main/DATA/c-md/camp/hmr_on_shake_on/inputs) from the mentioned location.




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
