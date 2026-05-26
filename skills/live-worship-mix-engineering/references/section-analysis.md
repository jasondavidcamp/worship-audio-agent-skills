# Section Analysis

Whole-song metrics hide the exact places a worship mix succeeds or fails.

## Required Sections

When possible, analyze:

- Sparse intro or verse.
- First full chorus.
- Biggest chorus or bridge.
- Outro or repeated refrain.
- Any user-identified problem timestamp.

If the song structure is unknown, pick the loudest 30-second windows plus one quieter vocal-led window.

## What To Compare Per Section

For each section, capture:

- Time range.
- Integrated/short-term loudness if available.
- RMS, peak, crest.
- Broad band levels.
- Vocal audibility notes.
- Band density notes.
- Musical function: verse, chorus, bridge, outro, speaking, prayer, etc.

## Section-Specific Questions

Sparse section:

- Is the vocal exposed in a good way?
- Does reverb/delay become distracting?
- Is piano/acoustic body too large?

Full chorus:

- Does the vocal stay intelligible?
- Does the band feel supportive rather than crowded?
- Is cymbal/sibilance fatigue acceptable?

Bridge/build:

- Does the mix build emotionally?
- Are drums and bass driving or merely louder?
- Do BGVs help the congregation sing?

Outro/refrain:

- Does repetition feel worshipful or tiring?
- Does bus compression flatten the lift?

## Output Format

Use compact section rows:

```yaml
section: biggest_chorus
range: 140-170s
metrics:
  lufs_or_rms: -18.9 dB RMS
  peak: -3.1 dBFS
  crest: 15.8 dB
diagnosis:
  vocal: "clear but slightly behind piano body"
  band: "supportive, low-mid full"
  fatigue: "safe"
next_move: "try 1-2 dB dynamic pocket in band bus around vocal presence"
```
