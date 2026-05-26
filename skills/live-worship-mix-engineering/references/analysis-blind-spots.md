# Analysis Blind Spots

Use this before giving a grade or deciding the next render.

## Metrics Can Miss These

- A vocal can measure bright and still be unintelligible if the band owns the same presence range.
- A vocal can be loud enough and still feel emotionally small if compression pins every phrase.
- A chorus can be louder without feeling bigger if drums, BGVs, and harmonic density do not change musically.
- Low peak level does not mean the mix is safe if bus processing is audibly crunchy.
- Clean LUFS/peak/spectrum/mono metrics do not prove a render is usable; static, crackle, plugin hash, or corrupted-sounding artifacts can pass numeric checks.
- High mono correlation is useful for mono-first church contexts, but it does not guarantee good balance.
- A smoother vocal is not always better if it loses consonants, urgency, or congregational leadership.

## Common False Positives

Do not over-score a render because:

- Master loudness increased.
- The high end sounds more exciting for ten seconds.
- The lead vocal is isolated but no longer feels connected to the band.
- The plugin chain resembles a respected preset package.
- The loudest 30-second window improved while sparse sections got worse.

## Common False Negatives

Do not under-score a render because:

- It is more mono than a commercial reference.
- Vocal processing is obvious when soloed but natural in the full band.
- The mix is quieter than a released track while being appropriate for church/rehearsal evaluation.
- The band bus ducks subtly under the lead vocal.

## Required Sanity Checks

Before a final grade:

- Verify no clipping or render-bound error occurred.
- Verify no static/crackle/artifact report exists for the render path; if the user reports one, invalidate the batch before scoring.
- Loudness-match candidates before judging tone.
- Check at least one sparse vocal section and one dense chorus/bridge.
- Decide whether the issue is source, bus, master, arrangement, or aimpoint mismatch.
- Compare against the active aimpoint or preference rule from `band-sound-aimpoint`.

## When To Hand Off To Band Sound Aimpoint

Use `band-sound-aimpoint` for a short taste call when:

- Two candidates trade clarity against warmth.
- Tuning or compression audibility is the main risk.
- Reverb/delay depth changes emotional feel.
- The candidate is technically better but may conflict with the church's active aimpoint.

Avoid asking when the render has an objective failure; fix that first.
