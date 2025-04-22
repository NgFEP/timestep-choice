#rm CDK2/setup/molname-ligname.mapping
#rm -rf CDK2

#### To run amber MD simulation
#source /home/saikat/softwares/amber22/amber.sh

#### To generate TI input files
#source /home/saikat/softwares/AMBER/FE-Workflow-master/FE-Workflow.bashrc
source /home/saikat/softwares/AMBER/FE-Workflow/FE-Workflow.bashrc
#conda activate amber-conda
#echo "Activating conda environment"
#eval "$($(which conda) 'shell.bash' 'hook')"
#conda activate /home/saikat/softwares/anaconda3/envs/AmberTools23
#conda activate /home/saikat/softwares/amber22_src/build/CMakeFiles/miniconda/install

setup_fe input 
