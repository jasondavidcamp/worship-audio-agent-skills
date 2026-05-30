# Worship Audio Agent Skills

AI-agent skills and helper tools for live worship audio: mix aimpoints, worship mix diagnosis, render-file diagnostics, REAPER session automation, Behringer WING snapshots, Waves plugin-chain choices, SuperRack session files, and practical mix-engineering workflows.

## Skills

- `band-sound-aimpoint`: define reference targets, style vocabulary, and taste-call calibration for worship mixes.
- `live-worship-mix-engineering`: critique worship mix renders, diagnose weak points, and choose practical brand-neutral next moves.
- `reaper-session-automation`: safely operate REAPER projects, tracks, FX chains, render settings, short snippet renders, render-window recovery, and REAPER-to-SuperRack handoffs.
- `waves-live-plugin-chains`: choose source-specific live-safe Waves plugin chains for SuperRack SoundGrid/Performer, or for LV1/REAPER-staged chains that must transfer safely to SuperRack.
- `mix-render-diagnostics`: analyze existing render candidates, references, stems, sections, stereo/mono translation, codec delivery risk, artifacts, and candidate reports.
- `behringer-wing-snap`: inspect Behringer WING `.snap` files and compare routing against SuperRack sessions.
- `superrack-session-files`: inspect, validate, and carefully patch Waves SuperRack `.sprk` session databases and `.xps` rack presets.

Boundary note: `reaper-session-automation` owns DAW/session operations; `mix-render-diagnostics` starts after trustworthy audio files or stems exist.

## Workflows

- [REAPER to SuperRack Iteration](workflows/reaper-to-superrack-iteration.md): how the skills work together to design Waves chains in REAPER, transfer them into SuperRack, and validate deployment state.
- [Backlog](BACKLOG.md): future experiments and improvements that are not ready to become skill instructions yet.

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

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

Waves, SuperRack, REAPER, Behringer WING, and other product names are trademarks of their respective owners. This project is not affiliated with or endorsed by those companies.
