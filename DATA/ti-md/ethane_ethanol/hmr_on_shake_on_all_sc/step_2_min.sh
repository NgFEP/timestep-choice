#!/bin/bash
source /home/saikat/softwares/AMBER/amber24/amber.sh
cat << EOF > "min.mdin"
Minimization of the entire molecular system
&cntrl
imin            = 1
maxcyc          = 5000
ntmin           = 2
ntx             = 1
ntxo            = 1
ntpr            = 5
cut             = 10

ifsc            = 1
icfe            = 1
clambda         = 0.00000000
timask1         = ':1'
timask2         = ':2'
scmask1         = ':1'
scmask2         = ':2'
/
EOF

pmemd -O -p out_hmr.parm7 -c out.rst7 -i min.mdin -o min.mdout -r min_hmr.rst7
