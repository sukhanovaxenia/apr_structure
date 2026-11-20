# GAPDH APR findings — 20 November 2026

All 20 supplied APR peptides match the original prediction sequences and canonical references. Their confidence labels and full predictor provenance are retained. Nine homologous measurement groups were obtained from the frozen four-protein MSA; a projected window is not a new prediction in that protein.

19 of the 20 native windows have complete eligible coverage in the configured structure. TDH3 1–6 has 5/6 eligible positions in the all-chain profile. Human and TDH3 refer to experimental tetramers; TDH1/TDH2 refer to predicted monomers.

## Descriptive interface burial

The following supplied windows lose solvent-accessible area on assembling the frozen-coordinate experimental tetramer. Numbers are averages per residue over eligible positions after chain averaging. They do not measure dissociation energy or prove aggregation after dissociation.

| Protein / supplied window | Monomer mean RSA | Tetramer mean RSA | Mean assembly burial (Å²/residue) |
|---|---:|---:|---:|
| human_GAPDH_37_49 | 0.2830 | 0.1603 | 30.744 |
| human_GAPDH_305_315 | 0.1332 | 0.0518 | 19.381 |
| yeast_TDH3_238_245 | 0.0661 | 0.0015 | 11.589 |
| yeast_TDH3_306_313 | 0.0700 | 0.0034 | 15.496 |

Other windows can have low native RSA without appreciable oligomer-interface burial: being buried in a folded chain is different from being shielded by another subunit. The complete per-window measurements are in `results/apr_summary.tsv`; these four examples are not a new statistical selection of APRs.

## Statistical result and missing tests

These structural burial tests are separate from the NAD-binding-module enrichment hypothesis in the original amyloscope run. Domain-enrichment p-values are not reused as structural evidence.

The pre-existing structural protocol's amino-acid-standardized RSA remains the primary metric. None of the 15 evaluable native-window tests passes BH q<0.05 in its experimental/predicted family. Five native-window tests are unavailable, and all four global union tests are unavailable.

W313 in human and W311 in yeast occur in APR windows, but their amino-acid type does not satisfy the minimum count needed for the reference normalization. This is a normalization limitation, not missing coordinates. TDH3 position 1 has a separate structural-coverage limitation. `structural_missing_positions` and `normalization_unavailable_positions` distinguish these reasons. The minimum count was not lowered after seeing the predictions.

Raw-RSA exact-shift results and composition-preserving Monte Carlo diagnostics are retained separately. They should not be substituted as the primary test merely because their p-values are smaller. No inference of non-amyloid behaviour follows from the current nonsignificant or unavailable primary tests.

## Structural follow-up already available

- APR-related heavy-atom contacts, backbone H-bond proxy records and ligand proximity are supplied as explicit tables.
- DSSP strand overlap and topological beta-edge candidates remain separated by native-assembly and isolated-chain context.
- Homologous group tables retain exact projected positions, gaps and the fraction actually called in each protein.
- Four PyMOL sessions, protein-specific configs/commands/legends, 14 molecular images and four accessibility profiles visualize the imported calls.

The human prediction panel lacked TANGO while the yeast panels included it. A common-predictor sensitivity analysis remains appropriate before interpreting species differences. TDH1/TDH2 tetramer protection and chemical effects of oxidation were not inferred from monomer models or from this sequence-only APR run.
