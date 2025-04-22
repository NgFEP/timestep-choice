#!/bin/bash
source /home/saikat/softwares/AMBER/amber24/amber.sh
cat << EOF > "min_3_atom_sc.mdin"
Minimization of the entire molecular system
&cntrl
imin            = 1
maxcyc          = 5000
ntmin           = 2
ntx             = 1
ntxo            = 1
ntpr            = 5
cut             = 9

ifsc            = 1
icfe            = 1
clambda         = 0.00000000
timask1         = ':1'
timask2         = ':2'
scmask1         = ':1@C,H,H1,H2'
scmask2         = ':2@C1,O,H3,H4,H5'
/
EOF

pmemd -O -p out_hmr.parm7 -c out.rst7 -i min_3_atom_sc.mdin -o min_3_atom_sc.mdout -r min_hmr_3_atom_sc.rst7
