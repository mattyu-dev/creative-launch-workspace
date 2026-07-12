# Editorial Operations design system

Status: implemented v2

Product: Creative Launch Workspace for Meta Ads

Reference lineage: Airtable-inspired editorial workflow grammar, independently adapted

## Product character

The workspace should feel like a meticulous creative-operations desk: calm enough for long review sessions, warm enough that assets remain the material of the work, and precise enough that owners and blockers never become decoration.

Its personality comes from composition, typography, proof marks, and a few full surfaces. It does not come from effects.

## Tokens

```css
--canvas: #fbfbf7;
--surface: #ffffff;
--surface-soft: #f3f4ef;
--ink: #1c211e;
--body: #414641;
--muted: #6b716b;
--line: #d9ddd6;
--line-strong: #aeb5ad;

--action: #1c211e;
--action-pressed: #090c0a;
--focus: #275fb8;

--oxide: #9e4029;
--forest: #113e31;
--paper: #f2e7d2;
--peach: #efa67b;
--mint: #acd2bb;

--ready: #166347;
--ready-soft: #e6f1eb;
--review: #805800;
--review-soft: #fbefd2;
--blocked: #a1362d;
--blocked-soft: #f7e7e4;
```

Signature colors create atmosphere. Semantic colors communicate state. They never exchange jobs.

## Typography

- Stack: Inter when locally available, then the system UI stack. No external font request.
- Page title: 16px / 500 inside the utility bar.
- Task focus: 24-36px / 400 desktop, 25px mobile.
- Panel title: 18px / 500.
- Body: 14px / 400.
- Operational cells: 12px / 400-550.
- Micro-labels: 10-11px / 600, uppercase only at this size.
- IDs, row lineage, URLs, hashes: monospace 10-11px.
- No product heading uses weight 700.

## Geometry and depth

- Base spacing unit: 4px.
- Inputs and controls: 6px radius.
- Workspace shell: 10px radius.
- One editorial summary surface: 12px radius.
- Status pills are allowed; panels are not pills.
- No gradient, glass, glow, or card shadow.
- Hairlines and surface changes create depth.
- A real overlay may use one shadow; the current workspace has no overlay.

## Shell

Desktop at 1300px and above:

```text
56px utility bar
task-first review focus
collapsed batch context
workspace shell
├── fluid four-column review queue
└── 340-400px decision inspector
```

Below 1024px, the queue becomes structured row cards and the inspector opens as a focused decision sheet. DOM and visual priority are:

1. one explicit human-review task;
2. filters with `To review` selected by default;
3. creative queue rendered as structured row-cards;
4. selected-row issue, reviewer and decision controls;
5. creative preview, technical mapping, export and batch context on demand.

There is no horizontally compressed desktop table on mobile.

## Components

### Task-first review focus

One forest surface answers the operator's first question: what needs me now? It opens on the ten ambiguous rows and explains that clean rows need no action while blocked rows are already routed for fixes. Two explicit actions switch to the human-review or blocker queues. Counts support the instruction instead of competing with it.

### Creative row

The queue exposes only four decision-oriented columns:

- synthetic proof thumbnail and creative ID;
- offline status;
- issue, owner and proposed fix;
- review state.

Campaign, ad set, delivery, UTM, post, source, idempotency, and destination details belong in the inspector.

### Synthetic proof thumbnail

Thumbnails are deterministic CSS proof tiles, not fake customer creative. Peach, mint, paper, and forest rotate by source row. Crop marks communicate creative review and remain functional: they label the tile as a proof surface.

### Decision inspector

The inspector starts with the issue, assigned reviewer, note and three decisions. The reviewer role defaults to the issue owner. Creative preview, technical mapping and local export are collapsed disclosures below the decision. This preserves depth without placing every control on the critical path.

### Progressive disclosure

- owner queue, issue mix, guardrails and AI evidence live under `Batch details`;
- bulk changes and state import live under `Batch actions`;
- preview, mapping and export live under separate inspector disclosures;
- persisted review receipts and exports never become authorization inputs.

### Status

- Ready: green semantic pair.
- Needs review: amber semantic pair.
- Blocked / needs fix: red semantic pair.
- Oxide is a brand/editorial accent, never a blocker substitute.

## Accessibility contract

- 44px touch targets on mobile.
- Visible focus ring in `#275fb8`.
- Keyboard row selection with Enter or Space.
- `aria-selected` on the active row.
- `aria-pressed` on filters.
- Captions and labels remain present when table headers are visually hidden on mobile.
- Task focus precedes the queue in DOM reading order.
- Reduced-motion mode removes press translation and smooth scrolling.
- Status never relies on color alone: every status includes text and a marker.

## Copy rules

- Short, direct, operational English.
- Sentence case except micro-labels.
- No "AI-powered", "revolutionary", "seamless", or invented performance claims.
- State the synthetic/local boundary wherever the surface could be mistaken for a live Meta tool.

## Acceptance checks

- one signature color moment per viewport;
- no external network dependency;
- no hidden live-mutation path;
- no horizontal table scroll on mobile;
- default view contains only the ten rows needing a decision;
- the first selected creative and its issue are understandable without opening technical details;
- all existing persistence, import, export, filter, bulk decision, and keyboard contracts pass.
