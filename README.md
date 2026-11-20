# apr-structure

A reusable command-line package for connecting **supplied APR predictions** to
protein structures. It imports amyloscope intervals with exact sequence checks,
measures accessibility and structural contacts, tests positional null models,
projects homologous measurement windows through a supplied MSA, and generates
protein-specific PyMOL configurations, commands, images and sessions.

Protein identities, sequences, ligands, target-chain counts, coordinate paths and
analysis settings live in the study configuration. The package does not predict
APRs or establish amyloid formation.

## Installation

For analysis of existing residue tables:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
apr-structure --help
```

For the optional mmCIF measurement backend:

```bash
python -m pip install -e '.[measure]'
```

FreeSASA needs a working native installation. A conda environment with numpy,
pandas, matplotlib, pyyaml, scipy, biopython and freesasa can also be used. DSSP
is a separate executable; PyMOL is a separate application. Neither is required
to analyze precomputed tables. The table workflow and the coordinate backend
were tested in different existing environments; see `docs/VALIDATION.md`.

Without installation, set `PYTHONPATH` to this repository's `src` directory and
run `python -m apr_structure`. The supplied GAPDH study has a launcher that does
this, so it does not modify the existing Python environments.

## Study workflow

```bash
apr-structure validate /path/to/study.json
apr-structure run /path/to/study.json
apr-structure render /path/to/study.json --pymol /path/to/pymol
```

`run` generates all numerical outputs, reports, plots and PyMOL input files.
`render` runs PyMOL and refreshes the report/gallery. To rebuild only the viewing
files or report, use `views` or `report` with the same config.

A nonempty analysis output is not silently mixed with a new run. Change
`output_dir` for a new analysis, or explicitly use `run --overwrite` to replace
an output directory marked as belonging to this tool. Keep input files outside
the output directory. `run_manifest.json` records input and code hashes, package
versions, completion state and unavailable-test counts.

## Starting a different protein project

1. Copy `examples/new_protein.json` to a new study directory.
2. Provide the exact canonical/reference FASTA and original prediction FASTA
   or amyloscope config. Set `protein` to the actual reference FASTA ID.
3. Supply a consolidated APR TSV with Protein/Start/End/Region columns, or
   explicitly map other names in `apr.columns`. Class, Tools, Locus and the
   complete original row are preserved. Coordinates must be declared.
4. Supply validated structural tables and coordinates, **or** measure a fresh
   homogeneous protein assembly with the optional backend.
5. Select the native context and statistical design before interpreting results.
6. Omit `alignment` for unrelated proteins. Supply a verified MSA only when
   homologous-window comparison is scientifically appropriate.

The minimal example uses a monomer. For a dimer or tetramer, change
`expected_chains` to the number of copies of the target sequence and set
`native_context` to `assembly`. Add other structures as additional entries;
multiple conformations of one protein are supported, but remain dependent
observations unless the design establishes otherwise.

To calculate tables from a new mmCIF:

```bash
apr-structure measure study.json --dssp /path/to/mkdssp
apr-structure validate study.json
apr-structure run study.json
apr-structure render study.json
```

Use a fresh `metrics_dir` for `measure`. It writes `residues.tsv`, contacts,
backbone H-bond proxies, DSSP strands, ligand contacts, interfaces, metadata,
and canonical-numbered `coordinates.pdb`. `--structure ID` can select a subset.
Without DSSP, SASA/contact calculations proceed, while DSSP annotations are
explicitly unavailable. The assembly must already be supplied as coordinates;
the backend does not guess a biological assembly from an asymmetric unit.

## Supported scope

**Table workflow:** arbitrary reference sequences and configurable column
names; monomer and assembly metrics; experimental or predicted structures;
multiple target chains; explicit author-to-reference display mapping.
A single target chain in a larger complex can use `expected_chains: 1` with
`native_context: assembly`. Supply externally computed context-aware metrics
for such complexes. Contacts to chains outside the target table are not
mislabelled as APRs of the target protein.

**Built-in coordinate backend:** standard L-amino-acid protein monomers and
homomers, one coordinate model, up to 25 protein chains for PDB export,
explicitly retained small molecules with supported C/N/O/P/S element radii.
It accepts a uniquely mappable canonical construct, including truncations;
tags, mutations and nonstandard residues require separate curation. It rejects
RNA/DNA polymer contexts and heterogeneous protein sequences rather than
silently measuring the wrong assembly. Use the table adapter for these cases.
It does not rebuild missing atoms, relax structures, protonate molecules,
generate AlphaFold multimers, or infer covalent chemistry.

## Outputs

| Output | Meaning |
|---|---|
| `validated_aprs.tsv` | Sequence-verified native calls, confidence, tools and original source rows |
| `apr_summary.tsv` | One structure per window; completeness, native RSA, assembly/ligand burial, contacts, H-bonds, secondary structure and within-chain Rg |
| `chain_metrics.tsv` | Dependent-chain diagnostics; not biological replicates |
| `null_tests.tsv`, `nulls/` | Actual null distributions, effects, p/q and reasons for unavailable tests |
| `apr_contact_pairs.tsv` | Heavy-atom contact records involving APRs, with unique residue-pair IDs |
| `apr_backbone_hbonds.tsv` | Backbone electrostatic proxy records involving APRs |
| `apr_ligand_contacts.tsv` | Ligand proximity records; not chemical H-bond assignments |
| `strand_overlap.tsv` | APR–DSSP-strand overlap and topological edge candidates by context |
| `homologous_groups.tsv` | Exact projected position lists; `called_here` distinguishes predictions from projections |
| `homologous_group_metrics.tsv` | Measurements of those exact projected lists, without inherited native-window p-values |
| `pymol/` | JSON/PML and command examples per structure; PSE/PNG after rendering |
| `REPORT.md`, `GALLERY.html` | Data-derived results and figures |

See `docs/INPUTS.md` for the table contract, `docs/METHODS.md` for scientific
definitions and `docs/PYMOL.md` for viewing commands.

## GAPDH example

The companion `GAPDH_APR_analysis_2026-11-20` study contains the real 20 supplied
amyloscope APRs and frozen structure inputs. `examples/gapdh.json` shows its
configuration; it expects the companion study's `inputs/` directory and is not
a replacement for those data files. No GAPDH identity or interval is built into
the package's analysis routines.

The new APR results are separate from the older no-APR baseline. Human GAPDH
and TDH3 use experimental tetramers; TDH1/TDH2 use predicted monomers. Do not
compare these as if all four were experimental tetramers.

## Development checks

```bash
python -m unittest discover -s tests -v
```

Coordinate tests are skipped if optional measurement dependencies are absent.
Tests cover bad sequence/numbering rejection, exact-shift resolution, missing
data, composition sampling, chain dependence, noncontiguous MSA projections,
analytic SASA geometries and a synthetic non-GAPDH dimer with a GOL ligand.
Synthetic test windows are not included in the biological GAPDH results.

