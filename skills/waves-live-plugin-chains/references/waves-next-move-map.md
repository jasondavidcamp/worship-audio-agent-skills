# Diagnosis To Next Move Map

Use targeted moves. Avoid changing the entire chain when one relationship is weak.

## Vocal Problems

Vocal clear but sharp:

- Try de-esser/Sibilance threshold refinement.
- Try F6 dynamic range around 3-7 kHz.
- If Silk Vocal is available, test gentle resonance smoothing before broad EQ cuts.
- Avoid broad top cuts until dynamic control fails.

Vocal warm but buried:

- Pocket band/piano/guitars before boosting vocal top.
- Try dynamic band-bus F6 sidechain keyed by vocal.
- Reduce piano/acoustic low-mid density.
- If the vocal chain lacks expansion before compression, test PSE or lower compressor input to prevent raised bleed.
- Confirm gain staging first; an over-driven vocal or band bus can make the vocal feel cloudy even after EQ.

Vocal loud but not intelligible:

- Check 1.5-4 kHz masking.
- Reduce reverb/delay wetness.
- Check compressor attack/release and RVox output.
- If using CLA-76/C6, verify the fast compressor is not flattening consonants and the multiband stage is not over-controlling presence.

Vocal processed or detached:

- Back off compression or tuning.
- Reduce serial effects on the vocal bus.
- Reassess whether the lead is too constant dynamically.
- If Tune Real-Time is first, check key/scale/speed before changing downstream EQ.

## Band Problems

Band full but cloudy:

- Reduce low-mid buildup on piano/guitars/band bus.
- Use dynamic EQ before adding brightness.
- Check whether bus saturation/color is thickening the low-mid range.
- Use separation EQ on less-important harmonic sources before applying broad mixbus cuts.

Band small:

- Check drum bus and overhead relationship.
- Bring up support instruments in chorus only if possible.
- Add bus glue carefully; do not solve size by master limiting.

Chorus does not lift:

- Compare verse/chorus vocal, drums, bass, BGV, and keys separately.
- Add arrangement-density support rather than only loudness.
- Check bus compression release and gain reduction; a glue compressor can hold down the section that should open up.
- Consider section automation/fader balance before master limiting.

## Drum Problems

Drums pokey but not driving:

- Reduce isolated snare peak or add bus glue.
- Check kick/bass relationship.
- Try drum bus compression for movement before increasing close-mic levels.

Drums buried:

- Bring overheads/snare/kick up in context.
- Avoid making cymbals harsh just to find drum energy.
- Check whether master/bus compression is clamping drum lift in choruses.

## Master/Loudness Problems

Mix too quiet but headroom exists:

- Use conservative master fader gain first.
- Verify loudest sections for clipping.

Mix clipped or crunchy:

- Remove/bypass limiter guesswork.
- Pull master or buses down.
- Re-render loudest sections before full render.
- Revisit source and bus gain staging before changing tone plugins.

Do not trust normalized limiter parameters until real rendered behavior has been verified.

## Effects Problems

Vocal feels distant:

- Reduce vocal reverb/delay return or decay before adding vocal level.
- Add or increase pre-delay when available so consonants remain forward.
- Filter the effect return so lows/low-mids do not blur the lyric.

Mix dry but lyric-forward:

- Add ambience/room conservatively and re-grade intelligibility.
- Favor tucked, filtered effects over obvious lushness for mono-first church playback.

## Gate/Expander Problems

Gate chatters or chops:

- Lower reduction amount or adjust threshold/hold/release before abandoning the gate.
- Use detector filtering where available so the gate listens to the intended source.
- Prefer natural decay over perfect silence on live multitracks.
