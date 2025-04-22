#!/bin/bash
source /home/saikat/softwares/AMBER/amber24/amber.sh

#cat<<EOF>strip_stateA.in
#parm unisc.parm7
#trajin stateA.rst7
#strip :Na+,Cl-
#autoimage
#trajout stateA_noion.rst7
#EOF
#cpptraj -i strip_stateA.in
#rm strip_stateA.in
#
#cat<<EOF>strip_stateB.in
#parm unisc.parm7
#trajin stateB.rst7
#strip :Na+,Cl-
#autoimage
#trajout stateB_noion.rst7
#EOF
#cpptraj -i strip_stateB.in
#rm strip_stateB.in
#
#cat<<EOF>parmstrip_stateA.in
#parm unisc.parm7
#parmstrip :Na+,Cl-
#parmwrite out unisc_noion.parm7
#EOF
#cpptraj -i parmstrip_stateA.in
#rm parmstrip_stateA.in

parmed="parmed"
$parmed out.parm7 << EOF
hmassrepartition
outparm out_hmr.parm7
quit
EOF

