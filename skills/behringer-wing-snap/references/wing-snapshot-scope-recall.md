# WING Snapshot Scope And Recall

Use this when the question involves snapshot safety, scene recall, partial recall, snapshot scope mismatch, or why a recalled snapshot may not change the expected console area.

## Source Material Mined

- WING remote/OSC documentation: snapshot files are JSON trees and include scope groups for channel, aux, bus, main, matrix, FX, input routing, output routing, configuration, surface area, and data groups.
- WING snapshot behavior documentation: snapshot scope determines which parts of the console are saved/recalled.
- Existing `.snap` observations: some exported snapshots include `scopes`; some may omit scopes and still carry usable `ae_data`/`ce_data`.

## Core Principle

A snapshot can contain data and still not be intended to recall all of it. Analyze both the data and the scopes. Treat scopes as recall-safety metadata.

## Scope Groups To Check

- `ch`: input channels.
- `aux`: aux channels.
- `bus`: buses.
- `main`: mains.
- `mtx`: matrices.
- `fx`: FX slots.
- `routin`: input routing.
- `routout`: output routing.
- `cfg`: groups, audio, surface, custom.
- `area`: console surface areas.
- `data`: user/data sections.

Scopes may appear as dictionaries of booleans or compact strings depending on export/source. Do not fail when the representation changes; summarize what is enabled, disabled, or absent.

## Diagnostic Patterns

- User expects routing recall, but `routin`/`routout` scopes are absent or disabled: likely recall-scope mismatch.
- User expects bus/matrix changes, but `bus`/`mtx` scopes are disabled: snapshot may leave output mix state unchanged.
- FX/external inserts exist in `ae_data.fx`, but `fx` scope is disabled: data is visible, but recall may not affect FX slots.
- No `scopes` object: analyze structure, but avoid making recall guarantees.
- Surface/user-layer changes appear in `ce_data`, but `cfg.surface` or `area` scopes are not enabled: recall may not affect operator layout.

## Safety Workflow

1. Identify whether the task is analysis-only or recall/edit preparation.
2. Summarize scopes before recommending recall.
3. Separate "file contains this value" from "snapshot will recall this value."
4. If editing scopes, require explicit user confirmation and keep a backup.
5. For live-use snapshots, flag any routing, insert, sample-rate, or output patch scope that could change service audio unexpectedly.

## Recommended Output

For scope/recall findings, report:

- Scope summary: included, omitted, disabled, unknown.
- Expected effect: what recall likely changes.
- Non-effect: what recall may leave untouched.
- Risk: routing change, output change, FX insert change, surface/operator change, or no-scope uncertainty.
