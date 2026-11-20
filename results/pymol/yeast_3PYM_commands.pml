# Run from this pymol directory: pymol yeast_3PYM.pml
# Available scenes: assembly, monomer, RSA; interface for oligomers.
# Selectors below use mapped observed residues; absent coordinates are not invented.
scene assembly, recall
# yeast_TDH3_1_6: MVRVAI; moderate; colour tv_orange
select current_APR, APR_01
show sticks, current_APR
zoom current_APR, 8
# yeast_TDH3_128_132: MFVMG; moderate; colour magenta
select current_APR, APR_02
show sticks, current_APR
zoom current_APR, 8
# yeast_TDH3_238_245: VSVVDLTV; moderate; colour cyan
select current_APR, APR_03
show sticks, current_APR
zoom current_APR, 8
# yeast_TDH3_306_313: VKLVSWYD; moderate; colour yellow
select current_APR, APR_04
show sticks, current_APR
zoom current_APR, 8
