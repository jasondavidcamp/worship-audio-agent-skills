# SuperRack .sprk Reference

## Database Shape

`.sprk` files observed so far are SQLite databases. Start with:

```sql
PRAGMA integrity_check;
PRAGMA foreign_key_check;
SELECT type, name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%';
```

Important tables:

- `snapshot`: snapshots such as `Active`, `starter`, `good`.
- `snapshot_chainer`: names and presets for rack/bus chainers in each snapshot.
- `object`: `id`, `obj_type`, `obj_index`, `name`; join to `cluster_type`.
- `chainer`: chainer details, keyed by `obj_id`.
- `plug`: plugin instance rows. `slot` is chain order within `chainer_id`.
- `snapshot_plugin`: plugin state per snapshot.
- `plugin_preset`: XML-like preset payload; F6 parameters live here.
- `plug_sidechain`: sidechain source for a plugin.
- `routes`: routing rows. Do not edit unless the encoding is understood.

## Validation Queries

Use these orphan checks after edits:

```sql
SELECT COUNT(*) FROM plug p LEFT JOIN chainer c ON c.obj_id=p.chainer_id WHERE c.obj_id IS NULL;
SELECT COUNT(*) FROM snapshot_plugin sp LEFT JOIN plug p ON p.id=sp.plug_id WHERE p.id IS NULL;
SELECT COUNT(*) FROM snapshot_plugin sp LEFT JOIN plugin_preset pp ON pp.id=sp.preset_id WHERE pp.id IS NULL;
SELECT COUNT(*) FROM snapshot_plugin sp LEFT JOIN snapshot s ON s.id=sp.snapshot_id WHERE s.id IS NULL;
SELECT COUNT(*) FROM plug_sidechain ps LEFT JOIN plug p ON p.id=ps.plug_id WHERE p.id IS NULL;
SELECT COUNT(*) FROM routes r LEFT JOIN src_routing_type t ON t.id=r.src_asgn_type WHERE t.id IS NULL;
SELECT COUNT(*) FROM routes r LEFT JOIN dst_routing_type t ON t.id=r.dst_asgn_type WHERE t.id IS NULL;
```

## F6-RTA Identity

SuperRack UI may show `F6-RTA`.

Database rows observed:

- `plug.plugin_name`: `F6-RTA`
- `plug.plugin_4cc`: `QDZM`
- `plugin_preset.preset` header:
  - `<PluginName>F6</PluginName>`
  - `<PluginSubComp>QDZM</PluginSubComp>`

## F6 Parameter Tokens

F6 preset payload uses:

```xml
<Parameters Type="RealWorld">
...
</Parameters>
```

Tokenize this block with:

```regex
[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|\*
```

Observed token count: `272`.

For six visible floating bands:

- Frequency tokens: `0-5`
- Q tokens: `8-13`
- Static gain tokens: `48-53`
- Threshold tokens: `56-61` confirmed for Bands 5 and 6, likely same order for Bands 1-4
- Dynamic range tokens: `64-69`
- Attack tokens: `80-85`
- Release tokens: `88-93`
- Visible band enabled flags: `168-173`
- Per-band external sidechain source flags: `144-149` confirmed for Bands 5 and 6, likely same order for Bands 1-4.

The visible band enable flags were confirmed by disabling Band 1 in SuperRack UI, which changed token `168` from `1` to `0`. Therefore:

- Band 1 enable: token `168`
- Band 2 enable: token `169`
- Band 3 enable: token `170`
- Band 4 enable: token `171`
- Band 5 enable: token `172`
- Band 6 enable: token `173`

## Vocal Pocketing Pattern

To use bands 5 and 6 for vocal pocketing while disabling bands 1-4:

- `4 = 2200`
- `5 = 4000`
- `12 = 1.5`
- `13 = 1`
- `52 = 0`
- `53 = 0`
- `60 = 0`
- `61 = 0`
- `68 = -2`
- `69 = -1.5`
- `84 = 20`
- `85 = 10`
- `92 = 180`
- `93 = 120`
- `168 = 0`
- `169 = 0`
- `170 = 0`
- `171 = 0`
- `172 = 1`
- `173 = 1`

This leaves the static EQ line flat and applies only dynamic ducking on the sidechain.

## Sidechain Pattern

Observed sidechain row for Band Bus F6 keyed by Vocal Bus:

- `plug_sidechain.plug_id = 225`
- `AsgnType = 1`
- `ControlType = 2`
- `TrackType = 0`
- `TrackHandle = 48`
- `SectionType = 7`
- `SectionIndex = -1`
- `ChannelIndex = -1`
- `controlID = 0`

In the observed session, `TrackHandle=48` matched `Vocal Bus` object index. Do not assume this value in other sessions.

## Learned Caution

Earlier attempts changed tokens `136-141`, which did not disable visible bands in the UI. Use `168-173` for visible F6 band enable state.

## F6 External Detector Mapping

A controlled UI save changed Band 6 `SC SOURCE` from `INT` to `EXT` on the Band Bus pocketing F6-RTA.

Observed database effects:

- Active preset changed from `plugin_preset.id=756` to `763`.
- `plug_sidechain` row did not change.
- Stored snapshots `starter` and `good` did not change.
- Active preset token `149` changed from `0` to `1`.
- A reverse save changed Band 6 `SC SOURCE` from `EXT` back to `INT`.
- That reverse save changed only Active preset token `149`, from `1` back to `0`.

Because token group `144-149` is six values wide, token `148` is confirmed for Band 5 and token `149` is confirmed for Band 6. The adjacent band mapping is likely:

- Band 1 source flag: token `144`
- Band 2 source flag: token `145`
- Band 3 source flag: token `146`
- Band 4 source flag: token `147`
- Band 5 source flag: token `148` confirmed
- Band 6 source flag: token `149` confirmed

Observed values:

- `0` = `INT`
- `1` = `EXT`

The first `INT` to `EXT` save also changed Active-only tokens `160`, `162`, `163`, `164`, and `198`; these did not revert when Band 6 returned to `INT`. Treat them as likely UI/editor state, one-time mode initialization, or unrelated state unless later tests prove otherwise.

A Band 5 `INT` to `EXT` save changed token `148` from `0` to `1`. It also changed token `198` from `5` to `4`, consistent with `198` being selected/current band UI state rather than sidechain source.

A reverse Band 5 `EXT` to `INT` save changed only token `148`, from `1` back to `0`.

## F6 SC Mode Mapping

An exploratory save set Bands 5 and 6 to `EXT` and appears to have changed an F6 `SC MODE` control. Compared with the prior saved state:

- token `148`: `0` to `1` = Band 5 `SC SOURCE` `INT` to `EXT`
- token `149`: `0` to `1` = Band 6 `SC SOURCE` `INT` to `EXT`
- token `198`: `4` to `5` = selected/current band UI state
- token `133`: `0` to `1` = candidate `SC MODE`-related state
- token `164`: `1` to `0` = candidate `SC MODE`-related state or related mode/UI state

This was not initially isolated enough to confirm SPLIT/WIDE mapping.

A later save changed Band 6 back to `SC MODE = Split` while leaving Bands 5 and 6 `SC SOURCE = EXT`. Compared with the previous exploratory state, only token `133` changed:

- token `133`: `1` to `0`
- tokens `148` and `149` stayed `1`, confirming this was not source selection.
- token `198` stayed `5`, confirming this was not just selected-band UI state.

Therefore token `133` is confirmed for Band 6 `SC MODE`, with observed values:

- `0` = `Split`
- `1` = the other mode observed before the reverse test, likely `Wide`

Band 5 was then changed while Bands 5 and 6 remained `SC SOURCE = EXT`. Compared with the prior Band 6 Split state:

- token `132`: `0` to `1`
- token `198`: `5` to `4`, selected/current band UI state
- source flags `148` and `149` stayed `1`

Therefore token `132` is confirmed for Band 5 `SC MODE`.

A reverse Band 5 change back to `Split` changed only token `132`, from `1` back to `0`.

Because `132-133` match Bands 5-6, the likely per-band SC MODE flags are:

- Band 1 mode flag: token `128`
- Band 2 mode flag: token `129`
- Band 3 mode flag: token `130`
- Band 4 mode flag: token `131`
- Band 5 mode flag: token `132` confirmed
- Band 6 mode flag: token `133` confirmed

Token `164` did not change in the isolated reverse test. Do not treat it as the primary SPLIT/WIDE flag.

## F6 Band Shape Mapping

A Band 6 shape change from `Bell` to `High Shelf` changed:

- token `141`: `1` to `2`
- token `198`: `4` to `5`, selected/current band UI state

A reverse Band 6 change from `High Shelf` back to `Bell` changed only:

- token `141`: `2` to `1`

The source flags `148-149` and mode flags `132-133` did not change. Therefore token `141` is confirmed for Band 6 shape/type.

Observed values:

- `0` = `Low Shelf`
- `1` = `Bell`
- `2` = `High Shelf`

A Band 6 shape change from `Bell` to `Low Shelf` changed only token `141`, from `1` to `0`.

Because `141` sits in a likely six-band group `136-141`, the likely shape/type flags are:

- Band 1 shape flag: token `136`
- Band 2 shape flag: token `137`
- Band 3 shape flag: token `138`
- Band 4 shape flag: token `139`
- Band 5 shape flag: token `140`
- Band 6 shape flag: token `141` confirmed

## Plugin Bypass Mapping

Bypassing the Band Bus pocketing F6-RTA did not change the `plug` row or F6 parameter tokens.

Observed bypass row change:

- table: `snapshot_plugin`
- row: `plug_id=225`, `snapshot_id=-1` (`Active`)
- `bypass`: `0` to `1`
- `preset_id` changed from `788` to `792`, but the RealWorld token stream did not change.
- Stored snapshots `starter` and `good` kept `bypass=0`.

Therefore:

- `snapshot_plugin.bypass = 0` means plugin is in/active.
- `snapshot_plugin.bypass = 1` means plugin is bypassed for that snapshot/Active state.

## Renaissance Vox Token Mapping

RVox / Renaissance Vox preset payloads use a compact `RealWorld` token stream with 9 tokens observed.

Example Blue Vocal RVox tokens after controlled UI changes:

```text
-20 -80 130 * * * * -11.5 *
```

Controlled saves confirmed:

- token `0` = `Threshold`
  - Changing the RVox threshold to `-20` changed only the first token from the earlier value (`-6.3`) to `-20`.
- token `1` = `Gate`
  - Changing the RVox gate to `-35` changed token `1` from `-80` to `-35`.
- token `7` = output `Gain`
  - Changing RVox gain/output to `-11.5` changed token `7` from `0` to `-11.5`.

Likely from observed defaults, but not yet isolated:

- token `2` may be a fixed/ceiling-style output or internal value; commonly observed `130`.

When editing RVox for one singer, clone shared `plugin_preset` rows first or verify SuperRack has already created a private preset for that plugin. In the Laura/Blue Vocal test, manual RVox changes created private preset rows for Blue Vocal, avoiding changes to Red Vocal.

## Silk Vocal Identity

SuperRack UI may show Silk Vocal or Silk Vocal Live depending on host/platform wording.

Database rows observed after adding Silk Vocal to Blue Vocal:

- `plug.plugin_name`: `SilkVocl`
- `plug.plugin_4cc`: `KPMM`
- `plugin_preset.preset` header:
  - `<PluginName>Silk Vocal</PluginName>`
  - `<PluginSubComp>KPMM</PluginSubComp>`
- `RealWorld` token count observed: `436`

Do not edit Silk Vocal parameter tokens until controlled UI changes establish the mapping. It is safe to preserve a SuperRack-generated Silk Vocal instance and tune known downstream processors around it.

## Silk Vocal Gender Mapping

A controlled UI save changed Silk Vocal Live voice type from `Male` to `Female` on the Blue Vocal rack.

Compared with the prior Male preset, the Active Silk Vocal `RealWorld` token stream remained 436 tokens. The likely primary gender selector changed:

- token `403`: `0` to `1`

Observed value hypothesis:

- `0` = `Male`
- `1` = `Female`

The same save also changed tokens `273-281`, `283-284`, `314-316`, `318-319`, `353-355`, and `366`. Treat these as likely internal model/curve coefficients loaded by the gender switch, not independent user controls, unless later isolated UI experiments prove otherwise. When patching Male/Female, prefer using a SuperRack-generated Female preset snapshot as a template or change token `403` only with caution and validation.

Important operational note: this UI save also demonstrated that if SuperRack has the session open, saving from the UI can overwrite external database patches made after the session was loaded. Close/reload the session after DB patching before making UI changes.

## Silk Vocal Focus Amount Mapping

A controlled UI save changed Silk Vocal Live `Low` amount from `45` to `55` while preserving the previously learned Female profile changes.

Observed database effect:

- token `371`: `45` to `55`

Therefore token `371` is confirmed as the visible `Low` amount control in the observed Silk Vocal Live `RealWorld` token stream.

Known visible values from screenshot / saves:

- `Low` amount: token `371`, observed `45` and `55`

A controlled UI save changed Silk Vocal Live `Mid` amount from `35` to `37` while preserving the previously learned Female profile and Low amount changes.

Observed database effect:

- token `372`: `35` to `37`

Known visible values from screenshot / saves:

- `Mid` amount: token `372`, observed `35` and `37`

A controlled UI save changed Silk Vocal Live `High` amount from `50` to `60` while preserving the previously learned Female profile, Low, and Mid amount changes.

Observed database effect:

- token `373`: `50` to `60`

Known visible values from screenshot / saves:

- `High` amount: token `373`, observed `50` and `60`

A controlled UI save changed Silk Vocal Live output trim from `0.0` to `-4.0`.

Observed database effects:

- token `12`: `0` to `-3.9599999999999999645`
- token `30`: `0` to `-3.9599999999999999645`

No `snapshot_chainer_params` row changed for this plugin output trim test. Therefore this is a Silk plugin output control, not the rack output gain.

Known visible values from screenshot / saves:

- Silk output trim: tokens `12` and `30`, observed `0` and about `-3.96` for UI `-4.0`

## Silk Vocal Factory Preset: Raw to Pro - Female (Gain Match)

Loading the Silk Vocal Live factory preset `Raw to Pro - Female (Gain Match)` on Blue Vocal created an Active Silk preset named:

- `<Preset Name="Raw to Pro - Female (Gain Match)">`
- `SetupName="Raw to Pro - Female (Gain Match)"`

Observed visible/known token values:

- Gender/profile token `403`: `1` (`Female`)
- Low amount token `371`: `45`
- Mid amount token `372`: `35`
- High amount token `373`: `50`
- Output trim tokens `12` and `30`: `-5.5`

Compared with the default Male Silk preset, this factory preset changed the known Female internal model tokens plus these additional tokens:

- token `405`: `0` to `-10`
- token `424`: `100` to `34.700000000000002842`
- token `434`: `0.4000000000000000222` to `0.5999999999999999778`

Treat tokens `405`, `424`, and `434` as preset-specific/vendor controls until isolated UI tests identify their visible controls. This preset is a good vendor-authored baseline for Laura-style female lead vocal tests because it is gain-matched and conservative on Low/Mid/High amounts.

## F6 Band Solo Mapping

Toggling Solo on Band 6 changed the Active F6 RealWorld token stream:

- token `21`: `0` to `1`

The same save also changed `snapshot_plugin.bypass` for the Active pocketing F6-RTA from `1` back to `0`, so the plugin was re-enabled during this experiment. The stored snapshots kept `bypass=0`.

Because token `21` sits in a likely six-band group `16-21`, the likely band solo flags are:

- Band 1 solo flag: token `16`
- Band 2 solo flag: token `17`
- Band 3 solo flag: token `18`
- Band 4 solo flag: token `19`
- Band 5 solo flag: token `20`
- Band 6 solo flag: token `21` confirmed

A reverse Band 6 Solo off save changed only token `21`, from `1` back to `0`.

Observed values:

- `0` = Solo off
- `1` = Solo on

## F6 Threshold Mapping

Changing Band 6 threshold from `0` to `-10` changed only:

- token `61`: `0` to `-10`

Previously suspected tokens `72-77` remained `0.5` and are not threshold for the observed F6-RTA RealWorld token stream.

Because token `61` sits in a six-band-looking group `56-61`, the likely threshold tokens are:

- Band 1 threshold: token `56`
- Band 2 threshold: token `57`
- Band 3 threshold: token `58`
- Band 4 threshold: token `59`
- Band 5 threshold: token `60` confirmed
- Band 6 threshold: token `61` confirmed

A reverse Band 6 threshold change from `-10` back to `0` changed only token `61`.

A Band 5 threshold change from `0` to `-10` changed token `60`; token `198` also moved from `5` to `4`, consistent with selected/current band UI state.

A reverse Band 5 threshold change from `-10` back to `0` changed only token `60`.

## UI Cross-Checks

Cross-check database conclusions against the SuperRack UI when screenshots are available:

- Top rack title identifies the selected chainer, e.g. `Band Bus`.
- Overview strips show bus/rack numbers and plugin ordering.
- The Rack view shows the selected plugin with a yellow outline.
- The sidechain dropdown above the plugin editor should display the expected source, e.g. `Vocal Bus`.
- On the plugin tile, an orange/red `SC` badge indicates sidechain is active for that plugin instance.
- F6-RTA may still show all six numbered band markers on the graph even when some bands are disabled; use the lower band buttons and plugin controls to confirm active/inactive state.
- The rack-level sidechain assignment and the F6 per-band `SC SOURCE` `INT`/`EXT` setting are distinct. If the F6 UI shows `INT` for an active band, do not claim confirmed external vocal-triggered ducking until the per-band detector source mapping is verified.
