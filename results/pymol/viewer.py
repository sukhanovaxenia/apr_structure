"""Standalone PyMOL script: only the standard library and pymol are required."""

import json
import os
import hashlib
from pathlib import Path
from pymol import cmd

COLORS = ["tv_orange", "magenta", "cyan", "yellow", "salmon", "lime", "violet", "wheat"]


def selection(obj, rows):
    terms = [f"(chain {r['display_chain']} and resi {r['display_resi']})" for r in rows]
    return f"({obj} and (" + " or ".join(terms) + "))" if terms else "none"


def show_structure(config_path, render=False):
    render = str(render).lower() in ("true", "1", "yes")
    path = Path(config_path).resolve()
    cfg = json.loads(path.read_text())
    base = path.parent
    sid = cfg["structure"]
    rows = cfg["residues"]
    reference_chain = cfg.get("chain", rows[0]["chain"])
    cmd.reinitialize()
    cmd.load(str((base / cfg["coordinate_file"]).resolve()), "structure")
    cmd.hide("everything")
    cmd.show("cartoon", "structure and polymer.protein")
    cmd.color("gray75", "structure")
    cmd.bg_color("white")
    cmd.set("orthoscopic", 1)
    cmd.set("antialias", 2)
    cmd.set("ray_opaque_background", 1)
    cmd.set("cartoon_fancy_helices", 1)
    for ligand in cfg["ligand_names"]:
        cmd.show("sticks", f"resn {ligand}")
        cmd.color("gray35", f"resn {ligand}")
    for i, call in enumerate(cfg["aprs"], 1):
        mapped = [r for r in rows if call["start"] <= r["position"] <= call["end"]]
        name = f"APR_{i:02d}"
        cmd.select(name, selection("structure", mapped))
        cmd.color(call.get("color", COLORS[(i - 1) % len(COLORS)]), name)
        cmd.show("sticks", name)
        print(f"{name}: {call['apr_id']} {call['sequence']} [{call['confidence']}]")
    cmd.orient("structure")
    cmd.zoom("structure", 4)
    cmd.deselect()
    cmd.scene("assembly", "store")
    figures = base / "figures"
    figures.mkdir(exist_ok=True)

    def save(view):
        if render:
            cmd.png(
                str(figures / f"{sid}_{view}.png"),
                cfg.get("width", 1600),
                cfg.get("height", 1100),
                dpi=200,
                ray=1,
            )

    save("APRs_assembly")
    chain_rows = [r for r in rows if r["chain"] == reference_chain]
    cmd.create("monomer_display", selection("structure", chain_rows))
    cmd.disable("structure")
    cmd.orient("monomer_display")
    cmd.zoom("monomer_display", 5)
    cmd.scene("monomer", "store")
    save("APRs_monomer")
    cmd.create("rsa_display", "monomer_display")
    cmd.disable("monomer_display")
    cmd.hide("sticks", "rsa_display")
    cmd.show("surface", "rsa_display")
    cmd.set("transparency", 0.1, "rsa_display")
    for row in chain_rows:
        if row["rsa"] is not None:
            cmd.alter(selection("rsa_display", [row]), f"q={row['rsa']}")
    cmd.spectrum("q", "blue_white_red", "rsa_display", minimum=0, maximum=1)
    for row in chain_rows:
        if not row["eligible"]:
            cmd.color("gray50", selection("rsa_display", [row]))
    cmd.scene("RSA", "store")
    save("RSA")
    if cfg.get("has_assembly_context", cfg["expected_chains"] > 1):
        cmd.create("interface_display", "monomer_display")
        cmd.disable("rsa_display")
        cmd.show("surface", "interface_display")
        cmd.color("gray85", "interface_display")
        cmd.color(
            "firebrick",
            selection("interface_display", [r for r in chain_rows if r["interface"]]),
        )
        for i, call in enumerate(cfg["aprs"], 1):
            mapped = [
                r for r in chain_rows if call["start"] <= r["position"] <= call["end"]
            ]
            cmd.show("sticks", selection("interface_display", mapped))
            # Surface retains interface colours; APR identity is visible in stored APR scenes.
        cmd.scene("interface", "store")
        save("interface")
        cmd.disable("interface_display")
    cmd.disable("rsa_display")
    cmd.disable("monomer_display")
    cmd.enable("structure")
    cmd.scene("assembly", "recall")
    cmd.save(str(base / f"{sid}.pse"))
    (base / f"{sid}_render.json").write_text(
        json.dumps(
            dict(
                pymol_version=cmd.get_version()[0],
                coordinates="observed atoms only; mapping verified before view generation",
                apr_calls=len(cfg["aprs"]),
                source=cfg["source"],
                rendered=bool(render),
                configuration_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                render_token=os.environ.get("APR_STRUCTURE_RENDER_TOKEN"),
                RSA_display="q modified only in rsa_display; original structure occupancy/B retained",
                interface_display="red for delta SASA >= 5 A^2; not an APR prediction",
            ),
            indent=2,
        )
    )


cmd.extend("apr_view", show_structure)
