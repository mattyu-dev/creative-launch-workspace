---
register: brand
platform: web
---

# Creative Launch Workspace design system

## 1. Strategy

Creative Launch Workspace is a B2B product for teams controlling the handoff between approved creative and campaign build. The public page must behave like a credible SaaS launch surface, not an explanation of a side project.

The creative strategy is **Launch Control**. The signature visual is a routing track: inputs converge at a high-visibility checkpoint and leave with an explicit state. This motif can support the brand mark, product annotations, and workflow explanation, but it must remain semantic and sparse.

The first viewport is an asymmetric 44/56 split. The message, primary action, and at least half of a real product surface must be visible at 1440 by 900. No hidden hero content, decorative empty space, or metric template is allowed.

The page tells one sequence: identify the fragile handoff, show the control layer, demonstrate how exceptions move, explain bounded automation, expose inspectable evidence, and invite the visitor into the workspace.

## 2. Foundations

### Color

The committed palette is cold canvas, deep plum, action lemon, annotation fuchsia, and data lavender. Status green, amber, and red are reserved for real product states and never become brand decoration.

```css
:root {
  --canvas: oklch(97.5% 0.006 315);
  --surface: oklch(100% 0 0);
  --surface-tint: oklch(95.5% 0.014 315);
  --ink: oklch(19% 0.032 315);
  --plum: oklch(21% 0.055 315);
  --plum-raised: oklch(26% 0.062 315);
  --lemon: oklch(91% 0.17 100);
  --lemon-hover: oklch(86% 0.17 100);
  --lemon-pressed: oklch(80% 0.16 100);
  --fuchsia: oklch(57% 0.216 4);
  --fuchsia-text: oklch(44% 0.17 4);
  --lavender: oklch(82% 0.08 292);
  --muted: oklch(50% 0.02 315);
  --border: oklch(87% 0.016 315);
}
```

Lemon is the only primary-action color. Fuchsia occupies less than ten percent of the composition and marks annotations or routing only. Plum carries 35 to 45 percent of the first viewport. Lavender is reserved for data context.

### Typography

Mona Sans Variable is the single UI and display family. Its broad weight range supports a compact operational voice without introducing a second sans family. Geist Mono is reserved for identifiers, counts, and receipts.

- Display: 48 to 72px, 0.96 to 1.02 line height, letter spacing no tighter than -0.04em.
- Section title: 36 to 56px, 1.0 to 1.08 line height.
- Lead: 18 to 20px, maximum 70 characters.
- Body: 15 to 17px, 1.5 to 1.65 line height.
- Data: 11 to 14px Geist Mono.

### Spacing, geometry, and elevation

Use a four-pixel base grid with 8, 12, 16, 24, 32, 48, 72, 96, and 128px steps. Controls use 8 to 10px radii. Panels use 12 to 16px. Only the main product stage may reach 20px. Pills are reserved for status.

Elevation is minimal and directional. Product surfaces may use one soft shadow; content sections rely on borders, spacing, and color contrast. No glow or translucent glass.

### Motion

The page-load sequence uses one 240 to 360ms entrance with a small 30 to 50ms stagger. Interaction feedback remains under 200ms. Buttons press to 0.97 scale. Product tabs explain a state change; they do not animate for spectacle. Reduced-motion mode removes translation and nonessential transitions while keeping every element visible.

## 3. Components

### Header and brand mark

The header is one line and at most 72px high. The mark reduces the routing-track motif to three incoming lines, one lemon checkpoint, and two outgoing lines. Navigation labels are Product, Workflow, Controls, and Evidence. The persistent action is Open the workspace.

### Buttons

The primary button is plum text on lemon with an arrow that moves two pixels on hover. Secondary actions are text or a restrained outline. Labels state an action and destination. Every interactive target is at least 44px.

### Product stage

The hero product stage uses a real generated screenshot inside a deep-plum frame. The crop must keep the issue, owner, and next action legible. Tabs later in the page switch between Queue, Review, and Receipt views using real screenshots, WAI-ARIA tabs, and keyboard navigation.

### Routing flow

Four actual workflow steps may be numbered: Map brief, Check rows, Route exceptions, Record decision. They form a connected sequence, not four interchangeable feature cards.

### Evidence and boundaries

Fixture counts are labeled as interactive workspace data, never customer outcomes. Product boundaries appear once as compact trust copy. Engineering evidence links directly to source, tests, contracts, and generated evidence.

## 4. Patterns

### Hero

Use the single eyebrow “Pre-launch QA for Meta creative operations.” The headline is “The launch control layer before Ads Manager.” The subhead names the checks, routing, and human authority. The product remains visible without JavaScript and above the fold on desktop and mobile.

### Product narrative

Move from the launch handoff to the working control surface. Use alternating full-width compositions, connected rows, and an interactive product stage. Do not create a grid of three equal feature cards.

### Controls narrative

State the operating model once: AI proposes, deterministic rules bound the result, people decide ambiguous calls. Place synthetic-data and no-publish boundaries as supporting trust information, not as the hero message.

### Closing action

Return to the same promise and the same label: Open the workspace. The footer may state “Built by Mathieu Petroni” and link to inspectable profiles or source. It must not become a founder case-study section.

## 5. Content Guidance

Write as a real product selling an operational outcome. Prefer launch, check, route, owner, exception, decision, evidence, and workspace. Avoid AI-first language, vague transformation claims, theatrical manifestos, internal implementation jargon, and portfolio language.

Use sentence case. Headlines stay under eight words where practical. Paragraphs stay under 70 characters per line. Avoid long dashes in visible copy. Never use fabricated customers, ROI, guarantees, testimonials, pricing, trials, bookings, or enterprise-security claims.

Primary action: **Open the workspace**. Secondary action: **See the workflow**.

## 6. Do / Don't

Do show the real product in the first viewport. Do make issue, owner, and next action readable. Do use lemon only for high-value actions. Do preserve semantic status colors inside the product. Do support keyboard, reduced motion, reduced transparency, increased contrast, 320px widths, and 200% text zoom.

Do not reuse the previous coral brand. Do not clone a generic purple AI site. Do not use cream paper, gradients, grid patterns, glass, blobs, glow, gradient text, decorative dots, hero metric strips, or repeated card grids. Do not hide default content behind opacity. Do not add a case-study route or describe the product as a personal project.
