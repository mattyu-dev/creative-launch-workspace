# Creative Launch Workspace design-system selection

Date: 2026-07-11

Source: [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md)

Pinned source commit: `664b3e78fd1a298ba11973822da988483256d4b4`

## Decision

Use **Airtable as the reference system**, adapted into an original product language named **Editorial Operations**.

This is not an Airtable clone. The product takes the reference system's editorial restraint, workflow fit, modest type weights, 4px spacing grid, hairline depth, and rare warm signature surfaces. It rejects Airtable's brand palette, proprietary Haas type, pricing pills, marketing-page whitespace, rainbow treatment, and brand-specific composition.

Airtable wins because this product is simultaneously:

- a dense operational queue;
- a creative-asset review surface;
- a master-detail decision tool;
- a portfolio piece that must not look like the Carbon-inspired AGCP project.

IBM is marginally stronger for pure table density, Superhuman for triage speed, and PostHog for personality. Airtable is the only candidate that scores at the top across all four needs without making the product feel like a developer console, a fintech dashboard, or a generic AI website.

## Audit method

Three independent review lanes read all **74 `DESIGN.md` files** in full: 40,372 lines total. Each system was scored for this product, not as a general brand ranking.

| Criterion | Weight |
| --- | ---: |
| Creative-operations fit | 25% |
| Dense dashboard and queue fit | 20% |
| Distinctivity and taste | 15% |
| Resistance to generic AI/SaaS styling | 15% |
| Accessibility | 10% |
| Responsive behavior | 10% |
| Adaptability without brand copying | 5% |

## Complete ranking evidence

Scores are normalized to `/10` using the weights above. The table preserves catalogue order so every inspected system is auditable.

| # | System | Score | # | System | Score |
| ---: | --- | ---: | ---: | --- | ---: |
| 1 | Airbnb | 6.57 | 38 | Nintendo 2001 | 6.97 |
| 2 | **Airtable** | **9.27** | 39 | Notion | 7.15 |
| 3 | Apple | 6.60 | 40 | NVIDIA | 8.33 |
| 4 | Binance | 7.10 | 41 | Ollama | 6.97 |
| 5 | BMW M | 5.20 | 42 | OpenCode | 7.80 |
| 6 | BMW | 6.02 | 43 | Pinterest | 8.03 |
| 7 | Bugatti | 5.15 | 44 | PlayStation | 6.65 |
| 8 | Cal | 7.78 | 45 | PostHog | 8.90 |
| 9 | Claude | 6.57 | 46 | Raycast | 7.60 |
| 10 | Clay | 7.22 | 47 | Renault | 7.53 |
| 11 | ClickHouse | 7.32 | 48 | Replicate | 7.55 |
| 12 | Cohere | 8.05 | 49 | Resend | 7.25 |
| 13 | Coinbase | 7.40 | 50 | Revolut | 6.83 |
| 14 | Composio | 5.42 | 51 | Runway | 7.33 |
| 15 | Cursor | 8.49 | 52 | Sanity | 7.10 |
| 16 | Dell 1996 | 6.00 | 53 | Sentry | 6.55 |
| 17 | ElevenLabs | 5.72 | 54 | Shopify | 8.53 |
| 18 | Expo | 6.22 | 55 | Slack | 7.53 |
| 19 | Ferrari | 5.13 | 56 | SpaceX | 5.78 |
| 20 | Figma | 7.97 | 57 | Spotify | 7.40 |
| 21 | Framer | 5.30 | 58 | Starbucks | 7.28 |
| 22 | HashiCorp | 7.73 | 59 | Stripe | 7.83 |
| 23 | HP | 6.97 | 60 | Supabase | 7.88 |
| 24 | IBM | 9.12 | 61 | Superhuman | 9.07 |
| 25 | Intercom | 8.48 | 62 | Tesla | 6.05 |
| 26 | Kraken | 6.20 | 63 | The Verge | 7.75 |
| 27 | Lamborghini | 5.35 | 64 | Together.ai | 6.65 |
| 28 | Linear | 7.75 | 65 | Uber | 8.08 |
| 29 | Lovable | 6.68 | 66 | Vercel | 7.05 |
| 30 | Mastercard | 6.40 | 67 | Vodafone | 6.08 |
| 31 | Meta | 7.15 | 68 | VoltAgent | 6.75 |
| 32 | MiniMax | 6.52 | 69 | Warp | 8.20 |
| 33 | Mintlify | 7.30 | 70 | Webflow | 7.97 |
| 34 | Miro | 7.57 | 71 | Wired | 7.92 |
| 35 | Mistral | 7.47 | 72 | Wise | 8.18 |
| 36 | MongoDB | 7.15 | 73 | xAI | 6.05 |
| 37 | Nike | 8.28 | 74 | Zapier | 8.88 |

## Final shortlist

| Rank | System | Score | Why it did not win |
| ---: | --- | ---: | --- |
| 1 | Airtable | 9.27 | Winner: best balance of workflow, creative material, density, and portfolio differentiation. |
| 2 | IBM | 9.12 | Excellent density and accessibility; too austere and too close to AGCP's existing Carbon language. |
| 3 | Superhuman | 9.07 | Superb triage model; its extracted system is more marketing-led and needs a product shell invented around it. |
| 4 | PostHog | 8.90 | Warm and memorable; its mascot/illustration grammar is too brand-bound for direct adaptation. |
| 5 | Zapier | 8.88 | Strong automation fit; the orange signature competes with operational status colors. |

## Borrowed interaction discipline

The visual reference stays Airtable. Two non-visual lessons are retained as product heuristics:

- Superhuman: fast queue triage, persistent selection, one dominant decision per context.
- Wise: semantic status colors must remain separate from decorative brand surfaces.

These are interaction and accessibility constraints, not a visual-system mashup.

## Rejected patterns

- gradients, glows, glassmorphism, aurora backgrounds, and AI constellations;
- a wall of identical rounded metric cards;
- large display type at bold weights;
- pills as a universal component shape;
- decorative color that can be confused with readiness state;
- a 17-column table on mobile;
- fake product imagery or claims of real customer assets;
- copied logos, mascots, proprietary fonts, or brand-specific motifs.
