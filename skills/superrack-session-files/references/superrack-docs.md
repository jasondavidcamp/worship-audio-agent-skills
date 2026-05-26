# SuperRack Documentation Anchors

Use these notes as documentation-backed interpretation rules. Validate everything against the actual `.sprk` rows because database names and IDs vary by session.

## Official Concepts

From Waves SuperRack Performer and SuperRack documentation:

- Racks must be routed to input and output I/O. Sources may be ASIO/Core Audio channels, console expansion cards, or other hardware devices.
- Each plugin rack has eight slots. Signal flow is top to bottom, so slot order is processing order.
- A plugin's rack position determines where it sits in the signal flow. Moving plugins changes processing order and can affect downstream channel format.
- Plugin sidechain status is shown on the plugin tile. Sidechain sources are selected from the plugin pane for plugins that support sidechain.
- Bypassing a plugin keeps it in the processing chain.
- Disabling a plugin removes it from processing without deleting it; settings and assignments are kept for re-enable. Disabling may reduce CPU/DSP load and rack latency.
- Removing a plugin deletes it from the rack slot and loses its settings/control assignments.
- Adding, removing, disabling, or moving plugins can briefly interrupt audio. Parameter changes and bypass are safer live actions.
- Rack presets describe an entire rack, including I/O patching, plugin chain, and plugin settings.
- Pasting a copied plugin copies only the current state; it does not copy data from other snapshots.
- Recall Safe prevents snapshot recall from changing selected racks/functions or plugin instances regardless of snapshot scope.
- Plugin recall safe can be set for a plugin position across active racks, or for a specific plugin instance from the plugin menu.
- The rack latency box displays total rack latency. Plugin latency indicators show individual plugin latency.
- A plugin can be removed from latency compensation calculations through the latency-related plugin menu item.

## Practical Consequences for `.sprk` Analysis

- Treat `plug.slot` as the primary chain order.
- Treat `snapshot_plugin.bypass` as the plugin IN/bypass state for a snapshot or Active state.
- Treat `plug.disabled` separately from bypass. A disabled plugin is more like "not processing" than "bypassed."
- Treat `plug.recall_safe` as operationally significant. Snapshot rows can exist but not be recalled into a safe plugin/rack state.
- Treat `plug.ignore_latency` as operationally significant. It can make the UI/plugin latency look different from compensation behavior.
- Do not assume copied/inserted plugin states apply to stored snapshots. Compare `snapshot_plugin` rows by `snapshot_id`.
- Do not move, disable, remove, or insert plugins directly in the database unless the user explicitly asks and a SuperRack-generated template makes the edit safe.
- Plugin recommendations belong in `waves-live-plugin-chains`; file edits here should preserve the session's existing plugin choices unless the user explicitly asks for a change and a safe SuperRack-generated template exists.

## Snapshot And Support Caveats

Waves support notes include live-session cautions that matter when diagnosing `.sprk` files:

- Snapshot changes with different rack input or output levels may create audible clicks.
- Snapshot change time depends partly on disk speed; SSDs are preferred for fast changes.
- Loading sessions across major SuperRack versions can have compatibility caveats. In particular, surround-rack routing from V14 sessions loaded in V15 may need manual reestablishment.
- In SuperRack Performer, yellow/red AUDIO or CPU indicators suggest increasing the buffer or lightening plugin load.
- Non-Waves VST3 plugins may be loaded in SuperRack Performer only when the supported mono/stereo component is installed and scanned. Apple Silicon requires ARM-compatible VST3 plugins.

## Documentation Sources

- Waves SuperRack Performer User Guide: `https://assets.wavescdn.com/pdf/live/superrack-performer.pdf`
- Waves SuperRack Performer v2 User Guide: `https://assets.wavescdn.com/pdf/live/superrack-performer-v2.pdf`
- Waves SuperRack v5 User Guide: `https://www.waves.com/1lib/pdf/live/superrack-v5.pdf`
- Waves SuperRack Support Notes: `https://img.wavescdn.com/support/superrack-support-notes`
