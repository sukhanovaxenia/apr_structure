# GAPDH: supplied APRs integrated into structural analysis

Study snapshot: 20 November 2026. This folder contains the actual imported
amyloscope predictions, sequence-verified structural inputs, completed
measurements, null tests, homologous-window comparisons and PyMOL views.

Start with `FINDINGS.md`, then `results/REPORT.md` and `results/GALLERY.html`.
The reusable code is in the separate local `apr-structure` repository.

## Inputs and scope

- 20 native calls: human GAPDH 5; yeast TDH1 6; TDH2 5; TDH3 4.
- Confidence classes retained exactly: 19 moderate, 1 strong. No supplied call
  was discarded or promoted to experimentally established amyloid status.
- Human somatic GAPDH P04406: 1U8F biological tetramer, three retained NAD.
- Yeast TDH3 P00359: 3PYM biological tetramer, four retained NAD.
- TDH1 P00360 and TDH2 P00358: AlphaFold monomers; assembly and NAD protection
  remain unavailable.

`inputs/consensus_regions.tsv` is copied from the actual
`amyloscope_runlast/amyloscope_out/consensus_regions.tsv`. The original
amyloscope config is preserved and its full sequences match the reference.
The structural tables are frozen copies of the existing verified calculations.
`inputs/snapshot_manifest.json` records original project paths and hashes.

## Launch on this Mac

From the installed study directory:

```bash
cd /Users/kseniasuhanova/iCloud/Documents/Documents_icloud/Lab_amyloids/Projects/GAPDH/structural_apr/2026-11-20

# Read-only validation:
bash run.sh validate

# Rebuild APR measurements from the cached structural tables:
bash run.sh run --overwrite

# Rebuild all PyMOL images and sessions and refresh the report/gallery:
bash run.sh render
```

`run --overwrite` replaces this study's generated `results/` directory,
including any previous rendered sessions. It does not modify `inputs/` or the
older project baseline. Run `render` afterward if you want fresh PSE/PNG files.
For a new analysis design, copy the whole study to a separate dated folder.

The launcher uses the tested base Python 3.13 environment and locates the
sibling `Projects/apr-structure` repository. It does not install packages into
your existing environments. For another machine or location:

```bash
export APR_STRUCTURE_REPO=/path/to/apr-structure
export APR_STRUCTURE_PYTHON=/path/to/python
bash run.sh validate
```

After installing the reusable package, the equivalent commands are
`apr-structure run study.json`, `apr-structure render study.json`, etc.
PyMOL defaults to the installed Mac application or a `pymol` executable on PATH;
override it with `bash run.sh render --pymol /path/to/pymol`.

## PyMOL per protein

Open the saved PSE directly, or launch a protein-specific config:

```bash
cd results/pymol
/Applications/PyMOL.app/Contents/bin/pymol human_1U8F.pml
/Applications/PyMOL.app/Contents/bin/pymol yeast_3PYM.pml
/Applications/PyMOL.app/Contents/bin/pymol TDH1_AF.pml
/Applications/PyMOL.app/Contents/bin/pymol TDH2_AF.pml
```

These are alternative commands; open the protein you want. Each has a matching
JSON config, `*_commands.pml` with actual peptide/coordinate examples and
`*_legend.tsv` mapping APR selectors to colours and confidence classes.

Scenes are `assembly`, `monomer`, `RSA` and, for tetramers, `interface`.
`APR_01`, `APR_02`, etc. are local to the current protein. Cofactors are dark
grey, whereas APR colours identify windows. Interface red denotes SASA loss,
not a newly predicted APR. The original structure's occupancy/B values remain
intact; RSA is stored only in a display copy.

## Interpretation safeguards

The structure-average table has complete quality coverage for 19 calls. TDH3
1–6 is partial because canonical position 1 is not eligible in all four chains.
Separately, standardized-RSA tests involving W313 in human or W311 in yeast
cannot be evaluated with the retained minimum-five-per-amino-acid rule. These
are different reasons for missing statistics. Both are recorded explicitly.

No evaluable primary window reaches BH q<0.05 under the specified nulls and
families. The four global standardized tests are unavailable. This does not
establish absence of aggregation propensity. Raw RSA, composition diagnostics,
contacts, H-bonds, beta-strand overlap and interface burial remain reportable
with their stated limits.

The prediction panel lacked human TANGO data but included yeast TANGO data.
Keep this availability difference in mind when comparing species. The model
and experimental structures are also different evidence classes.

The previous baseline in the main GAPDH project is retained as a historical
no-APR calculation. This dated folder is the updated APR analysis; do not read
its results as if they were already present in the older baseline report.
