# Run from this pymol directory: pymol TDH1_AF.pml
# Available scenes: assembly, monomer, RSA; interface for oligomers.
# Selectors below use mapped observed residues; absent coordinates are not invented.
scene assembly, recall
# yeast_TDH1_1_6: MIRIAI; moderate; colour tv_orange
select current_APR, APR_01
show sticks, current_APR
zoom current_APR, 8
# yeast_TDH1_65_70: IIIDGV; moderate; colour magenta
select current_APR, APR_02
show sticks, current_APR
zoom current_APR, 8
# yeast_TDH1_128_133: MFVVGV; moderate; colour cyan
select current_APR, APR_03
show sticks, current_APR
zoom current_APR, 8
# yeast_TDH1_238_245: VSVVDLTV; moderate; colour yellow
select current_APR, APR_04
show sticks, current_APR
zoom current_APR, 8
# yeast_TDH1_306_313: VKLISWYD; moderate; colour salmon
select current_APR, APR_05
show sticks, current_APR
zoom current_APR, 8
# yeast_TDH1_323_330: VDLIEYVA; strong; colour lime
select current_APR, APR_06
show sticks, current_APR
zoom current_APR, 8
