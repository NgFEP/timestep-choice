#!/bin/bash
source /home/saikat/softwares/AMBER/amber24/amber.sh
cat<<EOF>strip_stateA.in
parm others/out_hmr.parm7
trajin others/out.rst7
strip :2
autoimage
trajout out_L00.rst7
EOF
cpptraj -i strip_stateA.in
rm strip_stateA.in

cat<<EOF>parmstrip_stateA.in
parm others/out_hmr.parm7
parmstrip :2
parmwrite out out_hmr_L00.parm7
EOF
cpptraj -i parmstrip_stateA.in
rm parmstrip_stateA.in
