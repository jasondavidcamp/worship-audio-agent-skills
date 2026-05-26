#!/usr/bin/env python3
"""Build a local Waves plugin catalog for live SuperRack mix decisions."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


DEFAULT_PLUGINS_DIRS = [
    Path("/mnt/c/Program Files (x86)/Waves/Plug-Ins V16"),
    Path("C:/Program Files (x86)/Waves/Plug-Ins V16"),
]


@dataclass(frozen=True)
class Rule:
    names: tuple[str, ...]
    category: str
    live_use: str
    stance: str
    notes: str


RULES = [
    Rule(("Primary Source Expander",), "gate/expander", "Bleed control on live vocals, close drums, and stage mics.", "core live", "Excellent first-stage cleanup when used gently."),
    Rule(("F6",), "dynamic EQ", "Dynamic/static EQ, vocal pocketing, harshness/low-mid control, bus shaping.", "core live", "One of the safest default problem-solvers for live SuperRack mixes."),
    Rule(("C6",), "multiband dynamics", "Vocal/bus multiband control, low-mid and presence management.", "core live", "Powerful but easy to overdo; use when F6 needs broader-band control."),
    Rule(("C4",), "multiband dynamics", "Broad multiband smoothing for vocals, bass, band, or drums.", "useful live", "Less surgical than C6/F6."),
    Rule(("RComp",), "compressor", "General compression on vocals, instruments, and buses.", "core live", "Simple, predictable, often better than fancy choices."),
    Rule(("RChannel",), "channel strip", "Basic EQ/compression/gate channel shaping.", "useful live", "A compact all-in-one Renaissance-style channel option."),
    Rule(("REQ", "Q10", "H-EQ", "GEQ", "SSLEQ", "EMO-Q4"), "EQ", "Static corrective and tonal EQ.", "core live", "Use after deciding whether the problem is static or dynamic."),
    Rule(("SSL E-Channel", "SSL G-Channel", "SSL EV2 Channel", "CLA MixHub", "Scheps Omni Channel", "MagmaChannelStrip"), "channel strip", "Console-style HPF/EQ/dynamics on channels or buses.", "core live", "Good when a source needs one coherent channel workflow."),
    Rule(("SSLComp", "API-2500"), "bus compressor", "Drum, band, vocal, and mix bus glue.", "core live", "Keep gain reduction light for worship; preserve section lift."),
    Rule(("CLA-76", "CLA-2A", "CLA-3A", "dbx-160", "H-Comp", "VComp", "PuigChild", "KramerPIE", "DPR-402", "Abbey Road RS124"), "compressor", "Color compression and dynamics control.", "useful live", "Pick for a specific envelope/color, not because a famous chain uses it."),
    Rule(("DeEsser", "RDeEsser", "Sibilance", "MannyM-TripleD"), "de-esser/resonance control", "Sibilance, snare wire, cymbal bite, and vocal edge control.", "core live", "Dynamic high-frequency control usually beats dull high-shelf cuts."),
    Rule(("Silk Vocal", "CLA Vocals", "Butch Vig Vocals", "JJP-Vocals", "Maserati VX1", "Greg Wells VoiceCentric"), "vocal processor", "Fast vocal polish or tonal shaping.", "useful with caution", "Can be great, but may hide what processing is happening. Validate by render/taste."),
    Rule(("Waves Tune Real-Time", "WavesTune", "WavesTune LT"), "pitch", "Live vocal tuning or offline pitch correction.", "useful live", "Tune Real-Time is the live choice; offline Tune variants are less relevant to SuperRack live use."),
    Rule(("Vocal Rider", "Bass Rider", "PlaylistRider"), "rider/leveler", "Automatic level riding before/after compression.", "useful with caution", "Can help consistency; verify it does not fight musical phrasing."),
    Rule(("H-Delay", "SuperTap", "MannyM-Delay", "CLA Epic", "CLA EchoSphere", "Space Rider"), "delay", "Vocal/instrument delay and live FX throws.", "useful live", "Prefer aux-style use when final topology allows; SuperRack serial chains need restraint."),
    Rule(("H-Reverb", "RVerb", "TrueVerb", "IRLive", "IR-1", "ARPlates", "Abbey Road Chambers", "MagmaSprings", "MannyM-Reverb", "CLA Epic", "Lofi Space"), "reverb", "Vocal and instrument space.", "useful with caution", "Latency/CPU/tail management matters; keep mono deployment in mind."),
    Rule(("Smack Attack", "TransX", "Torque", "InTrigger Drum Replacer", "InTrigger"), "drum shaping/trigger", "Transient shaping, drum tone correction, trigger/sample support.", "useful live", "Use InTrigger live/low-latency modes for SuperRack; avoid making drums feel over-processed."),
    Rule(("Sub Align", "InPhase", "InPhase LT"), "phase/time alignment", "Kick/sub/bass alignment and phase diagnosis.", "useful live", "Use deliberately; phase moves can break more than they fix."),
    Rule(("RBass", "MaxxBass", "LoAir", "Submarine", "MaxxVolume", "MV2"), "low-end/level enhancement", "Bass/kick extension or low-level density.", "useful with caution", "Useful on small systems; risky for headroom and mono PA if overused."),
    Rule(("NLS", "J37", "KramerTape", "Abbey Road Saturator", "BB Tubes", "Lil Tube", "REDD17", "REDD37-51", "Saphira", "Vitamin", "Aphex AX"), "saturation/exciter", "Warmth, harmonic density, and controlled excitement.", "useful with caution", "Check for static/grain and cymbal hash before learning taste from it."),
    Rule(("Abbey Road TG Mastering Chain", "CLA MixDown", "Greg Wells MixCentric", "IMPusher", "Maserati GRP"), "mix/bus processor", "Fast bus tone, compression, and finish.", "useful with caution", "Useful for broad tone shaping; do not let it hide balance problems."),
    Rule(("Abbey Road Vinyl", "Retro Fi", "Berzerk Distortion", "Magma StressBox", "MDMX Distortion", "MannyM-Distortion", "MultiMod Rack"), "creative distortion/lo-fi", "Special-effect grit, destruction, or lo-fi character.", "situational live", "Use only as an obvious effect; not a core worship mix tool."),
    Rule(("AudioTrack", "C1", "EMO-D5"), "channel dynamics", "Gate/expander/compressor basics and dynamics cleanup.", "useful live", "Good utility choices, though PSE/F6/RComp often fit many live worship workflows better."),
    Rule(("Clarix LB", "IDX Intelligent Dynamics", "Curves AQ", "Curves Equator"), "intelligent/dynamic processing", "Smart tone/dynamics correction.", "useful with caution", "May be powerful, but verify latency, stability, and audible side effects in renders."),
    Rule(("CLA Effects", "CLA Unplugged", "EddieKramer FX", "Maserati HMX", "Greg Wells PianoCentric", "Greg Wells ToneCentric"), "source-specific multi-processor", "Fast character processing for instruments or FX.", "situational live", "Can be useful for quick tone, but less transparent than discrete processors."),
    Rule(("API-550", "API-560", "Scheps 73", "PuigTec", "VEQ3", "VEQ4", "KramerHLS", "RS56", "TG12345"), "analog EQ/color", "Tone-shaping EQ with color.", "useful live", "Great for musical shaping after cleanup is stable."),
    Rule(("L1", "L2", "L3", "L3 Multi", "L3 Ultra", "L3-LL", "L3-16", "L4 Ultramaximizer", "UM", "WLM", "WLM Plus"), "limiter/loudness", "Peak protection, loudness measurement, or final-bus control.", "useful with caution", "Avoid loudness chasing during mix-shape work; LL variants are more live-minded."),
    Rule(("PAZ", "VU Meter", "Dorrough", "AR TG Meter Bridge", "SignalGenerator"), "metering/utility", "Metering, calibration, and troubleshooting.", "safe utility", "Useful for diagnostics; not tone processors."),
    Rule(("Clarix LB", "Clarity Vx", "Clarity Vx Pro", "Clarity Vx DeReverb", "Clarity Vx DeReverb Pro", "WNS", "NS1", "W43", "X-Click", "X-Crackle", "X-FDBK", "X-Hum", "X-Noise", "Z-Noise", "DeBreath"), "noise/restoration", "Noise, breath, feedback, and restoration control.", "verify-first/broadcast", "Clarix LB is broadcast-only for this skill; other restoration tools are latency/CPU/support-sensitive and must be verified in the actual SuperRack target."),
    Rule(("Feedback Hunter",), "feedback control", "Feedback detection/suppression.", "useful live", "Potentially valuable for monitors/FOH, but do not replace good gain structure."),
    Rule(("GTR", "GTRAmp", "GTRSolo", "GTRStomp", "GTRToolRack", "GTRTuner", "PRS Supermodels", "Voltage Amps Guitar", "Voltage Amps Bass", "Maserati GTi", "CLA Guitars", "JJP-Guitars"), "guitar/amp", "Guitar/bass amp and instrument processing.", "situational live", "Useful if SuperRack is hosting guitar processing; otherwise leave to source/amp modeler."),
    Rule(("CLA Drums", "JJP-Drums", "JJP-Cymb-Perc", "Maserati DRM", "EddieKramer DR"), "drum multi-processor", "Fast drum coloration.", "useful with caution", "Can sound impressive soloed; compare against the requested drum target before committing."),
    Rule(("CLA Bass", "JJP-Bass", "Maserati B72", "EddieKramer BA", "RenAxx"), "bass processor", "Bass tone and dynamics.", "useful live", "Good for bass pocketing, but protect vocal/kick relationship."),
    Rule(("Center", "S1", "PS22", "Doubler", "Reel ADT", "UltraPitch", "Waves Harmony", "OVox", "Vocal Bender", "Brauer Motion", "MondoMod", "MetaFlanger", "MetaFilter", "Kaleidoscopes", "Enigma", "Doppler", "Morphoder", "SoundShifter"), "width/modulation/pitch FX", "Creative width, doubling, movement, harmony, and special effects.", "situational live", "Use for deliberate effects, not core mix correction; mono church deployment reduces value."),
    Rule(("StudioVerse",), "chain browser", "StudioVerse chains/presets.", "avoid for SuperRack", "Do not rely on it for SuperRack/SoundGrid workflows unless explicitly verified."),
    Rule(("Abbey Road Studio 3", "NX", "Nx", "B360", "C360", "L360", "R360", "S360", "MV360", "IR-360", "Spherix", "Immersive Wrapper", "LFE360", "Dorrough Surround"), "surround/immersive/headphone", "Immersive/surround/headphone monitoring.", "avoid for church mono", "Usually irrelevant for mono-first church workflows."),
    Rule(("Bass Fingers", "Bass Slapper", "Clavinet", "CODEX", "CR8 Sampler", "Electric", "Element", "Flow Motion", "GrandRhapsody", "COSMOS", "Key Detector", "Sync Vx", "Waves Stream", "Waves Gemstones"), "instrument/app/support", "Instrument, app, analysis, or support plugin.", "not a mix insert default", "Installed but not normally part of live insert chains."),
]


def clean_name(path: Path) -> str:
    name = path.name
    if name.endswith(".bundle"):
        name = name[:-7]
    return name


def classify(name: str) -> dict[str, str]:
    lname = name.lower()
    for rule in RULES:
        if any(matches_token(lname, token.lower()) for token in rule.names):
            return {
                "category": rule.category,
                "live_use": rule.live_use,
                "stance": rule.stance,
                "notes": rule.notes,
            }
    return {
        "category": "uncategorized/needs review",
        "live_use": "Installed Waves bundle; purpose not yet classified.",
        "stance": "needs review",
        "notes": "Add manual notes after seeing it in SuperRack or using Waves docs.",
    }


def matches_token(lname: str, token: str) -> bool:
    if lname == token:
        return True
    if len(token) <= 3:
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", lname))
    return token in lname


def find_plugins_dir() -> Path:
    for candidate in DEFAULT_PLUGINS_DIRS:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Could not find Waves Plug-Ins V16 directory.")


def build_inventory(plugins_dir: Path) -> list[dict[str, str]]:
    rows = []
    for path in sorted(plugins_dir.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_dir() or not path.name.endswith(".bundle"):
            continue
        name = clean_name(path)
        row = {
            "name": name,
            "bundle": path.name,
            "path": str(path),
        }
        row.update(classify(name))
        rows.append(row)
    return rows


def markdown(rows: list[dict[str, str]]) -> str:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["stance"]] = counts.get(row["stance"], 0) + 1

    lines = [
        "# Local Waves Plugin Catalog",
        "",
        "Generated from the installed Waves V16 bundles on the current machine.",
        "",
        "This is an installed-plugin catalog, not a guarantee that every plugin is appropriate for every SuperRack target. Prefer the `core live` and `useful live` plugins for live SuperRack work, and verify any `useful with caution`, `verify-first/broadcast`, `situational live`, or `avoid` plugin inside the actual SuperRack target before committing a session.",
        "",
        "## Summary",
        "",
    ]
    for stance, count in sorted(counts.items()):
        lines.append(f"- {stance}: {count}")
    lines.extend(
        [
            f"- total installed Waves V16 bundles cataloged: {len(rows)}",
            "",
            "## How To Use This Catalog",
            "",
            "- Cleanup first: PSE, F6, channel-strip HPF/EQ/gate, de-esser.",
            "- Control second: RComp, CLA compressors, C6/C4, SSL/API bus compression.",
            "- Polish third: saturation, exciter, delay/reverb, specialty processors.",
            "- For mono-first church workflows, do not reward stereo width processors unless they improve the mono render too.",
            "- For live drums, prefer PSE/F6/SSL/API/Smack Attack/InTrigger-style utility over one-knob hype processors.",
            "",
            "## Installed Bundle Catalog",
            "",
            "| Plugin | Category | Stance | Live worship use | Notes |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            "| {name} | {category} | {stance} | {live_use} | {notes} |".format(
                **{k: row[k].replace("|", "/") for k in ("name", "category", "stance", "live_use", "notes")}
            )
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugins-dir", type=Path)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--md-output", type=Path)
    args = parser.parse_args()

    plugins_dir = args.plugins_dir or find_plugins_dir()
    rows = build_inventory(plugins_dir)

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    if args.md_output:
        args.md_output.parent.mkdir(parents=True, exist_ok=True)
        args.md_output.write_text(markdown(rows), encoding="utf-8")

    print(json.dumps({"plugins_dir": str(plugins_dir), "count": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
