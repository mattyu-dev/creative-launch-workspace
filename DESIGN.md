---
register: brand
platform: web
---

# Launch Control visual system

## Strategy

Launch Control is a B2B pre-launch QA product for Meta Ads. It must read as a real SaaS product in five seconds: what it catches, how exceptions move, who decides and what evidence remains.

The direction is Industrial AI Elegance, combining Apple-like hierarchy and material restraint with Linear-like product proof. The signature is the orange route from Detect to Route to Prove. The page never uses portfolio, personal-project or case-study framing.

The hero demonstrates a recorded decision trace from Detect to Route to Prove, looping automatically. Astryx provides the accessible product controls. The faceted orange decision token is a CSS clip-path hexagon that travels the rail and sits on the node of the current phase; the Three.js r128 requirement was lifted on 2026-07-16 and the WebGL renderer was removed. No generated raster or decorative product sculpture is allowed.

## Foundations

### Color

```css
:root {
  --canvas: #ECEDEE;
  --shell: #F4F5F5;
  --surface: #FFFFFF;
  --surface-soft: #F7F7F5;
  --ink: #232427;
  --charcoal: #171719;
  --body: #55575C;
  --muted: #6B6D72;
  --orange: #E34A32;
  --orange-hover: #F05A3C;
  --orange-soft: #FFF0EC;
}
```

Orange is the single brand and action color. Green, amber and red are reserved for real product state. Plum, lemon, fuchsia, lavender, gradient text and multicolor CTA systems are forbidden.

### Typography

- Inter Variable: body, display and product UI.
- Instrument Serif Italic: no more than two editorial accents on the full page.
- System monospace: identifiers and receipts only.
- Display: 56 to 64px desktop, 44px mobile, weight 600, line height .96 and tracking -.052em.
- Product UI: 12px minimum, with 14px body copy and 20 to 25px state titles. Exemption: uppercase micro-labels and step numerals may go down to 10px when letter-spacing is at least .04em and contrast is at least 4.5:1; never for product data such as IDs, statuses or values.

The hero implements a 600 to 900 variable-weight proximity interaction. Word groups remain intact so the effect never creates broken wrapping.

### Shape and depth

- Page wrapper: 1440px maximum, 40px desktop radius and 28px mobile radius.
- Product stage: 28px radius with an inner white highlight and diffuse charcoal shadow.
- Marketing cards: 24px radius.
- Product panels: 16px radius.
- Controls: 10 to 13px radius. Primary marketing actions may use pills.

Depth comes from warm neutral layers, inset highlights and restrained shadows. Glass is limited to the floating navigation and does not stack across the page.

## Product proof

The landing contains one native HTML/CSS product shell with three real states:

1. Queue shows the current synthetic run, routed exceptions and named owners.
2. Review shows the creative, exact launch facts, proposed fix and human actions.
3. Receipt shows the saved local decision, event trail and exportable JSON state.

Tabs use WAI-ARIA semantics, arrow-key navigation and a Transitions.dev sliding pill. The confirmation writes browser-local state, announces the result through `aria-live` and exports a real JSON file. No raster product screenshot is loaded by the landing.

## Motion

- Hero rise: 620ms with 60ms stagger.
- Recorded trace: 6600ms from Detect to Route to Prove, then a 3200ms reading pause; the walkthrough loops every 9800ms. Clicking a step holds the chosen phase for 5200ms before the loop resumes.
- Decision token: 18px CSS clip-path hexagon, orange gradient, left 13% / 50% / 87% per phase, 600ms cubic-bezier(.22,1,.36,1) travel along the rail.
- Tab pill: 250ms cubic-bezier(.22,1,.36,1).
- Inspector entrance: 280ms, 12px horizontal travel.
- Receipt timeline: 260ms with 60ms stagger.
- Button press: scale .98 for 100ms.

No `transition: all`, ease-in entrance, autoplay carousel, permanent drift or decorative parallax. Reduced-motion mode holds the walkthrough on the final Prove state with the CSS token resting on the last rail node, and runs no loop.

## Content and conversion

Eyebrow: **Pre-launch QA for Meta Ads**

Headline: **Catch creative launch mistakes before Ads Manager.**

Primary action everywhere: **Try the live workspace**

Synthetic counts must always be labeled as a current synthetic run. Never add fabricated clients, testimonials, ROI, pricing, trials, enterprise claims or platform-write capability.

## Accessibility and performance

- WCAG AA contrast for copy and controls.
- 44px minimum interactive targets.
- No horizontal overflow at 320px or 200% text zoom.
- Keyboard tabs and visible focus.
- Reduced motion, reduced transparency and increased contrast modes.
- No hero raster. The Astryx bundle is self-hosted, single-file and gzip-budgeted.
- Target Lighthouse: 90+ performance and 100 accessibility.

## No-go rules

- No old workspace, guided-review or evidence screenshots on the landing.
- No product UI text below 12px.
- No duplicate use of the sculpture.
- No fake browser chrome.
- No H1 longer than two desktop lines.
- No CTA below the first viewport.
- No case-study or personal-project route.
- No long dash in visible copy.
