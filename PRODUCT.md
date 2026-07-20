---
register: product
platform: web
---

# Launch Control

Launch Control is pre-launch QA for Meta Ads. It validates approvals, placements, destinations, naming and UTMs across every creative row, routes exceptions to the right owner and keeps ambiguous decisions human.

## Audience

- Creative operations leads and media buyers managing launch handoffs.
- CMOs, Heads of Growth and agency leads who need exceptions to have owners.
- CTOs and technical recruiters evaluating product judgment, trust boundaries and engineering quality.

## Product promise

**Catch creative launch mistakes before Ads Manager.**

A visitor should understand the category, see the working product and reach the live workspace in one first-screen scan.

## Working demo

The public interaction uses the committed synthetic batch `78f20843aea8a367`:

- 100 creative rows;
- 30 ready;
- 10 held for human decision;
- 60 blocked;
- zero external writes.

Queue, Review and Receipt are interactive HTML states. Confirming `cr_007` records browser-local state, creates an inspectable receipt and enables a real JSON export. It does not call Meta.

## Authority boundary

Automation may propose structured source context. Deterministic rules verify allowlists, schema and launch constraints. Named people decide ambiguous intent. The browser demo cannot publish, upload assets, load credentials or change spend.

## Conversion

- Primary action: **Try the live workspace**.
- Desktop secondary action: **See how it works**.
- Proof links: contracts, deterministic replay, CI and architecture.
- Belief sequence: Detect, Route, Prove. Inside the workspace the human step is labelled Decide because routing has already happened; Decide is the human half of Route.

## Brand behavior

The product feels industrial, calm and exact. Neutral layers create depth, charcoal carries authority and orange identifies the next action. Product evidence is always more prominent than decoration.

Forbidden: portfolio framing, case studies, fake clients, logos, testimonials, ROI, pricing, purple AI styling, multiple accent colors and repeated screenshots.

## Quality contract

- One canonical public landing and no `case-study.html`.
- Native product proof above the fold.
- H1 no longer than two lines on desktop.
- Useful Queue state inside the 390 by 844 mobile fold.
- 12px minimum product text and 44px minimum controls.
- Keyboard navigation, `aria-live`, reduced motion and no horizontal overflow.
- Lighthouse performance at least 90 and accessibility 100.
