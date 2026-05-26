# Section Manifest

Use a section manifest when the same song or service mix will be analyzed more than once. It keeps verse/chorus/bridge/problem timestamps repeatable without retyping `--section "name:start:end"` arguments.

## Minimal YAML Shape

```yaml
song: Example Service Mix
sections:
  - name: sparse_verse
    start: 42.0
    end: 72.0
    purpose: vocal_intelligibility
  - name: first_chorus
    start: 96.0
    end: 126.0
    purpose: balance_lift
  - name: big_bridge
    start: 182.0
    end: 212.0
    purpose: density_punch
```

## Minimal JSON Shape

```json
{
  "song": "Example Service Mix",
  "sections": [
    {"name": "sparse_verse", "start": 42.0, "end": 72.0, "purpose": "vocal_intelligibility"},
    {"name": "first_chorus", "start": 96.0, "end": 126.0, "purpose": "balance_lift"}
  ]
}
```

## Section Purposes

Use short purpose labels so reports stay scannable:

- `vocal_intelligibility`
- `balance_lift`
- `density_punch`
- `low_end_translation`
- `mono_translation`
- `tail_buildup`
- `codec_delivery`
- `reported_problem`

## Usage

```powershell
& "<python>" scripts/render_diagnostic_report.py --candidate "C:\path\candidate.wav" --baseline "C:\path\baseline.wav" --section-manifest "C:\path\sections.yaml" --md-output "C:\path\report.md"
```

Explicit `--section "name:start:end"` arguments can be used with a manifest. They are appended after the manifest sections, which is useful for one-off problem timestamps.

Keep manifests outside the public repo when section names, service dates, song names, or file paths reveal private production context.
