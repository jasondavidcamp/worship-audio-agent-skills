# Worship Audio Agent Skills

AI-agent skills and helper tools for live worship audio: mix aimpoints, REAPER render comparison, Behringer WING snapshots, Waves SuperRack sessions, and practical mix-engineering workflows.

## Skills

- `band-sound-aimpoint`: define reference targets, style vocabulary, and taste-call calibration for worship mixes.
- `live-worship-mix-engineering`: critique worship mix renders, diagnose weak points, and choose practical next moves.
- `reaper-render-reference`: use REAPER as a staging host for render comparisons and Waves/SuperRack transfer notes.
- `behringer-wing-snap`: inspect Behringer WING `.snap` files and compare routing against SuperRack sessions.
- `superrack-sprk`: inspect, validate, and carefully patch Waves SuperRack `.sprk` session databases.

## Layout

Each folder under `skills/` is a Codex-style skill:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
```

The workflows and reference docs are also readable by other AI agents or humans, even though the trigger metadata follows Codex skill conventions.

## Public Repo Notes

This repo intentionally excludes private rendered audio, `.snap` files, `.sprk` sessions, exported `.xps` presets, purchased training material, personal taste-call logs, and workstation-specific paths. Add those only in a private deployment repo or local skill folder.

## Script Dependencies

Most scripts use Python standard libraries. Audio analysis scripts may also use packages such as `numpy`, `soundfile`, `scipy`, `librosa`, `pyloudnorm`, and optionally `essentia`.
