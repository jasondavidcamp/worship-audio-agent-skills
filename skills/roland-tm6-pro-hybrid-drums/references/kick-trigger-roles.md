# Kick Trigger Roles

Use this file when choosing a TM-6 PRO kick sound or shaping a kick trigger layer.

## Diagnose The Need

Choose one main job first:

- Low-end weight: the acoustic kick is felt weakly in the stream or room.
- Beater definition: the groove is hard to follow against bass, guitars, keys, or tracks.
- Consistency: soft and hard hits vary too much for the mix target.
- Modern punch: the aimpoint expects a more produced kick than the acoustic drum provides.
- Effect moment: a special intro, breakdown, or transition needs an electronic or processed kick.

## Sound Families

Warm acoustic support:

- Use for natural congregational and acoustic-led worship.
- Choose a round kick with low-mid body and short sustain.
- Keep click low; trim boxiness before adding sub.

Tight modern acoustic:

- Use for modern arena and track-heavy worship.
- Choose controlled low end, short-to-medium decay, and enough beater to mark time.
- Avoid long sub tails when bass guitar is active.

Sub reinforcement:

- Use only when the acoustic kick already has good attack but lacks weight.
- Keep the sample quiet and short.
- High-pass or decay-shorten if the master bus ducks on every kick.

Click/attack layer:

- Use when the kick disappears on smaller speakers or dense sections.
- Add the least attack that makes the groove readable.
- Avoid metal-like click unless the aimpoint explicitly wants aggressive drums.

Electronic/fat synth kick:

- Use for special moments, track-heavy arrangements, or intentionally hybrid songs.
- Prefer kit-specific use instead of a default Sunday layer.
- Check that it does not confuse bass guitar pitch or worship style.

## Initial TM-6 Moves

- Tune the sample to the acoustic kick if it sounds like two drums.
- Shorten decay before lowering sub if the kick feels late or bloated.
- Add transient attack only until the groove reads.
- Use compression for consistency, not to make the layer dominate.
- Put stream-specific kick reinforcement on a separate output when routing allows.

## Starting Blend

- Natural support: very low, felt more than heard.
- Modern reinforcement: low to moderate under the close mic.
- Sample-forward: clear and intentional, but verify the acoustic mics do not make it flammy.

In practical terms, start around -18 to -12 dB under the close kick mic for natural reinforcement, then raise cautiously. For modern worship, -15 to -9 dB under the close mic is a reasonable audition window if the sample is short and controlled.

## Failure Signs

- The bass guitar loses note clarity.
- The kick sounds like two separate hits.
- The mix ducks on every downbeat.
- The room feels exciting but the stream feels bloated.
- Soft ghosted footwork triggers the same giant kick as hard downbeats.

## Quick Recommendation Templates

Natural worship:

```yaml
trigger_job: add warm consistency
sound_family: warm acoustic kick with short tail
blend_start: very low under acoustic kick
tm6_moves: short decay, low click, gentle transient
```

Modern worship:

```yaml
trigger_job: add polished punch and low-end control
sound_family: tight modern acoustic kick
blend_start: low-to-moderate under close mic
tm6_moves: tune to drum, shorten tail, add moderate attack
```

Track-heavy:

```yaml
trigger_job: lock acoustic kick to programmed energy
sound_family: tight short kick with defined attack
blend_start: moderate in stream path
tm6_moves: short decay, clear transient, avoid wide/roomy samples
```
