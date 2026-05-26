# Source Capture And Intelligibility

Use this when a worship mix problem may be caused before the console: microphone choice, placement, user technique, stage volume, room spill, feedback risk, or inconsistent tone.

Mined from public sources:

- Shure, House of Worship Audio Systems Guide: https://www.shure.com/en-US/docs/guide/Houses-of-Worship
- Shure, How to Choose the Best Mic for the Pastor: https://www.shure.com/en-ASIA/insights/how-to-choose-the-best-mic-for-the-pastor
- Shure, Choosing Between Lavalier and Headset Mics: https://www.shure.com/en-MEA/insights/fundamentals-choosing-between-lavalier-and-headset-mics
- DPA, How to Mic Vocals With Handheld Mics on Stage: https://www.dpamicrophones.com/mic-university/how-to-mic/how-to-mic-vocals-with-handheld-mics-on-stage/

## First Principle

Do not solve a capture problem with downstream processing until the capture path has been checked. EQ and compression can improve tone, but they cannot fully restore direct sound that was never captured clearly.

## Triage Questions

For speech or pastor mics:

- Is the mic type matched to the speaker's movement and comfort: headworn, handheld, lavalier, or lectern?
- Is the capsule close enough to the mouth to favor direct sound over room sound?
- Does the mic position stay consistent as the person turns, walks, reads, or gestures?
- Are two speech mics open at once, such as lav/headset plus lectern, causing hollow tone or feedback risk?
- Are clothing, hair, jewelry, or cable rub creating noise before the mix path?

For lead and BGV handhelds:

- Is the singer using a consistent distance and angle?
- Is the mic aimed at the mouth, not the chest, forehead, or ceiling?
- Does the singer move away on loud notes, and if so, does that improve tone or make the vocal disappear?
- Is proximity effect adding useful warmth or muddy low-mid buildup?
- Is cymbal, guitar, or wedge spill stronger than the direct vocal between phrases?

For stage and room:

- Are loud sources forcing FOH to under-reinforce instruments that will then disappear in the stream?
- Are monitors, PA spill, or reflective surfaces limiting gain before feedback?
- Does the problem improve when fewer microphones are open?
- Would a better microphone position or source discipline be lower risk than more gating, compression, or EQ?

## Diagnosis To Move

Speech lacks intelligibility:

- First check mic distance, placement, and whether the chosen mic type fits the speaker.
- Prefer headworn or stable close-position capture for mobile speakers when feedback or room pickup is a recurring issue.
- If using a lavalier, keep placement consistent and close enough to reduce tonal swings.
- If using a lectern mic, coach the speaker's position or switch mic type for mobile speakers.

Vocal is inconsistent:

- Check handheld technique before adding heavy compression.
- If the singer works the mic intentionally, preserve musical dynamics while smoothing only the disruptive swings.
- If the singer is untrained, prefer gentle dynamics and coaching over extreme processing.

Vocal is muddy:

- Check proximity effect and low-mid spill before cutting broad warmth.
- Use HPF and targeted low-mid control only after confirming the source is close and direct enough.

Vocal is bright but cymbal-heavy:

- Check off-axis cymbal pickup before de-essing the entire vocal.
- If the vocal mic is capturing more cymbal than singer between phrases, expansion or stage/source changes may matter more than EQ.

Speech or vocal is hollow:

- Look for multiple open mics capturing the same source at different arrival times.
- Mute unused mics, especially lectern plus worn mic combinations.

Feedback risk:

- Do not assume a different EQ curve is the first fix.
- Check mic-to-mouth distance, open mic count, mic polar pattern, monitor/PA geometry, room reflections, and source loudness.

## Skill Behavior

When capture is suspect, write the recommendation in this order:

1. Source/capture evidence.
2. Lowest-risk capture or routing correction.
3. Console/processing move only if capture cannot be changed.
4. How to verify the change by listening or recording.

Example:

```text
The pastor mic sounds thin and unstable because the capture distance changes when he turns away from the lav, not because the channel needs more compression. First test a headworn mic or more consistent lav placement. If that is not possible, use modest compression and avoid boosting presence so much that room spill and feedback come up with the voice.
```
