# Event Research: US-China Tariff Escalation

---

## 1. Confirmed Facts

| # | Fact | Source Type |
|---|------|-------------|
| F1 | **[CONFIRMED]** US announced new 25% tariffs on Chinese semiconductors and electronics, dated 2026-05-06. | Event brief (primary-equivalent for this exercise) |
| F2 | **[CONFIRMED]** China retaliated with export controls on rare earth minerals. | Event brief (primary-equivalent for this exercise) |
| F3 | **[CONFIRMED]** This represents a stated escalation in the ongoing US-China trade conflict. | Event brief |
| F4 | **[CONFIRMED]** China is the dominant global processor of rare earth minerals, controlling approximately 85–90% of processing capacity and ~60–70% of mining output (structural, pre-existing fact). | Industry data (high reliability) |
| F5 | **[CONFIRMED]** Rare earth elements are critical inputs for semiconductors, defense systems, electric vehicle motors, wind turbines, and advanced optics. | Industry reference (primary) |
| F6 | **[CONFIRMED]** The US imports a significant share of its consumer electronics and semiconductor components from China or via Chinese-controlled supply chains. | Trade data (high reliability) |

---

## 2. Unconfirmed Claims

| # | Claim | Status | Notes |
|---|-------|--------|-------|
| U1 | **[UNCONFIRMED]** Specific product codes / HTS classifications covered by the 25% tariff. | Not yet verified | Determines whether finished goods vs. components are targeted. Material to impact assessment. |
| U2 | **[UNCONFIRMED]** Scope of China's rare earth export controls — which specific minerals (light vs. heavy rare earths), quantities, and duration. | Not yet verified | Heavy rare earths (dysprosium, terbium) are more critical for defense and high-temp magnets. Scope matters enormously. |
| U3 | **[UNCONFIRMED]** Whether back-channel negotiations are underway that could de-escalate within weeks. | Rumor / speculative | Common in geopolitical events but unverified. |
| U4 | **[UNCONFIRMED]** Whether China will extend controls to gallium, germanium, or antimony (already controlled since 2023 but could tighten). | Speculative extension | Would affect compound semiconductors (GaAs, GaN, SiC). |
| U5 | **[UNCONFIRMED]** Market has already partially priced in tariffs (extent of pricing). | Needs evidence | Options skew, credit spreads, and analyst revisions needed to assess. |
| U6 | **[UNCONFIRMED]** Third-country rerouting (Vietnam, Mexico, Malaysia) will effectively neutralize tariffs. | Plausible but unverified | Depends on rules of origin enforcement. |

---

## 3. Transmission Map

```
PRIMARY SHOCK
├── Shock A: 25% tariff on Chinese semiconductors & electronics
│   └── Direct impact on import cost structure
│
└── Shock B: Chinese export controls on rare earth minerals
    └── Direct impact on raw material availability & pricing

TRANSMISSION CHANNELS
│
├── [COMMODITY] Rare earth prices spike
│   ├── Heavy rare earths (Dy, Tb) → defense, EVs, wind
│   ├── Light rare earths (Nd, Pr) → magnets, motors
│   └── Upstream: non-Chinese miners benefit; downstream: cost pressure
│
├── [SUPPLY CHAIN] Semiconductor input costs rise
│   ├── Fabless companies sourcing from China → margin pressure
│   ├── US fabs with domestic sourcing → relative advantage
│   └── Inventory buffers mask short-term impact; 2–4 quarter lag possible
│
├── [SUPPLY CHAIN] Electronics assembly & finished goods
│   ├── Consumer electronics (phones, laptops, IoT) → price increases or margin compression
│   ├── Industrial electronics → slower CapEx cycle if prices rise
│   └── Auto electronics → cost pressure on already thin margins
│
├── [POLICY] Potential escalation paths
│   ├── Further tariff rounds → broader economic damage
│   ├── CHIPS Act / IRA incentives accelerate for domestic producers
│   ├── Allied coordination (Japan, Netherlands) on semiconductor equipment
│   └── WTO challenge → unlikely to resolve quickly
│
├── [INFLATION / CURRENCY]
│   ├── Tariffs → input cost inflation (electronics, autos)
│   ├── Export controls → raw material inflation
│   ├── USD safe-haven flows → stronger dollar offsets some commodity upside
│   └── PBOC response → CNY management affects relative pricing
│
├── [SENTIMENT]
│   ├── Equity risk premium rises for China-exposed names
│   ├── Rotation into "reshoring" and "friend-shoring" beneficiaries
│   └── Defense / national security premium expands
│
└── [FINANCIAL]
    ├── Insurance costs for China-trade routes may rise
    ├── Trade finance availability could tighten
    └── Working capital needs increase if inventory hoarding begins

AFFECTED SECTORS
│
├── POTENTIAL POSITIVE (beneficiaries)
│   ├── US domestic semiconductor manufacturers (reshoring theme)
│   ├── Non-Chinese rare earth miners & processors
│   ├── Defense contractors (demand security, but rare earth cost risk)
│   ├── Commodity infrastructure (warehousing, logistics for re-routed supply)
│   └── Semiconductor equipment makers (US/EU/Japan) if fab build-out accelerates
│
├── POTENTIAL NEGATIVE (at risk)
│   ├── Import-dependent consumer electronics
│   ├── Fabless semiconductor companies with Chinese foundry exposure
│   ├── EV manufacturers reliant on Chinese rare earth magnets
│   ├── Chemical companies using rare earth catalysts
│   ├── Airlines & travel (secondary: confidence, fuel cost, demand)
│   └── Broad China-revenue-exposed multinationals
│
└── MIXED / UNCLEAR
    ├── TSMC — benefits from shift away from Chinese foundries but geopolitical risk to Taiwan
    ├── Apple — massive China assembly base but ability to re-route and pricing power
    └── US automakers — tariff protection vs. rare earth cost risk

DISCONFIRMING PATHS (what makes this thesis wrong)
│
├── Quick negotiated settlement (weeks, not months)
├── Third-country rerouting effectively neutralizes tariff impact
├── Rare earth export controls are narrowly scoped and non-binding
├── Inventory buffers (6–12 months for many rare earths) prevent near-term disruption
├── Alternative supply chains (Australia, US, Canada) scale faster than expected
└── Market has already priced in the full impact (check forward estimates, options skew)
```

---

## 4. Candidate Screen

### Tier 1 — Worth Immediate Deep Research

```yaml
- ticker: MP
  tier: 1
  direction: positive
  mechanism: >
    Sole US-based rare earth miner with active mining and processing at Mountain Pass, CA.
    China export controls create supply squeeze → rare earth prices rise → MP's
    realized pricing increases materially. MP has been building downstream processing
    (Stage 2 magnet manufacturing). Government contracts and DOD funding likely to
    accelerate. Revenue is directly leveraged to rare earth oxide pricing.
  key_tests:
    - What is MP's current production capacity vs. China-controlled supply?
    - Is MP's processing facility fully operational or still scaling?
    - What is MP's cost curve position vs. Chinese producers?
    - Has MP secured DOD or government supply agreements?
    - How much of MP's output goes to magnet vs. catalyst applications?
  disconfirming_tests:
    - China export controls are narrowly scoped to heavy rare earths MP doesn't produce
    - Rare earth prices have already spiked and MP's contract structure is fixed-price
    - MP's processing remains unprofitable at current scale
    - Government funding is political and not contractually committed
  required_next_step: >
    Update MP stock memo. Collect evidence on current production volumes,
    pricing mechanisms, contract structure, DOD relationships, and cost curve position.
    Check options market for implied volatility and positioning.

- ticker: INTC
  tier: 1
  direction: positive
  mechanism: >
    Intel is the largest US-headquartered semiconductor manufacturer with domestic fabs.
    25% tariff on Chinese semiconductors makes US-sourced chips relatively cheaper.
    Intel's foundry strategy (IFS) directly benefits from reshoring mandates.
    CHIPS Act funding + tariff protection creates a dual tailwind for domestic
    production economics. Government contracts (DOD, infrastructure) increasingly
    require US-origin chips.
  key_tests:
    - What percentage of Intel's output is manufactured in US fabs?
    - How much revenue comes from customers who would switch from Chinese sources?
    - What is Intel's current utilization rate and spare capacity?
    - Has Intel secured specific government/defense contracts requiring US origin?
    - What is the timeline for IFS foundry ramp?
  disconfirming_tests:
    - Intel's competitive position is weak regardless of tariff (process node lag)
    - IFS foundry business is too early-stage to capture near-term demand
    - Tariff exemptions are granted for semiconductor components Intel doesn't make
    - Chinese semiconductor imports were already declining before tariffs
  required_next_step: >
    Update INTC stock memo. Assess foundry pipeline, utilization, government
    contract exposure, and competitive positioning vs. TSMC and Samsung.
    Check if tariff language covers advanced nodes Intel produces.

- ticker: AAPL
  tier: 1
  direction: negative
  mechanism: >
    Apple assembles the vast majority of its hardware in China through Foxconn,
    Pegatron, and Luxshare. 25% tariffs on Chinese electronics directly hit
    Apple's cost structure. While Apple has begun diversifying to India and Vietnam,
    China remains the dominant production base. Rare earth controls add incremental
    cost to magnets, speakers, haptics, and camera modules in iPhones/Macs.
    Margin compression or price increases are the two outcomes; either damages
    the investment case.
  key_tests:
    - What is Apple's current China assembly exposure (percentage of units)?
    - Does the tariff cover finished consumer electronics or just components?
    - Can Apple pass tariff costs to consumers without demand destruction?
    - How fast is the India/Vietnam diversification actually progressing?
    - Does Apple have rare earth inventory buffers?
  disconfirming_tests:
    - Apple has already shifted majority of assembly out of China
    - Tariff exemptions cover smartphones and consumer electronics
    - Apple's pricing power fully offsets tariff costs with no demand impact
    - Rare earth controls don't affect Apple's specific component needs
  required_next_step: >
    Update AAPL stock memo. Quantify China assembly exposure, diversification
    timeline, tariff pass-through ability, and rare earth input costs.
    Check analyst consensus estimate revisions post-announcement.

- ticker: LLY (or broader pharma/biotech with rare earth dependency — replaced with more directly exposed)
```

Correction — replacing with a more directly exposed Tier 1:

```yaml
- ticker: LYSCF
  tier: 1
  direction: positive
  mechanism: >
    Lynas Rare Earths is the only significant non-Chinese rare earth processor
    at scale (Malaysia processing facility, Australian mining). China export
    controls make Lynas the primary alternative supply source globally. Lynas
    is building a US-based processing facility (funded partly by DOD). Direct
    revenue leverage to rare earth pricing increases.
  key_tests:
    - What is Lynas's current production capacity for NdPr and heavy rare earths?
    - What is the status of the US processing facility (Seadrift, TX)?
    - What are Lynas's offtake agreements and contract structure?
    - Is Lynas's cost curve competitive with Chinese producers?
    - What is Lynas's heavy rare earth production capability?
  disconfirming_tests:
    - China export controls are temporary and quickly reversed
    - Lynas's Malaysia operating license faces regulatory risk
    - Customers have 6–12 months of inventory and won't need spot purchases
    - Alternative suppliers (Vale, Iluka, Arafura) scale faster
  required_next_step: >
    Initiate stock memo for Lynas. Assess production capacity, cost position,
    contract structure, DOD relationship, and Malaysia regulatory status.
    Compare directly with MP Materials as alternative western rare earth play.
```

### Tier 2 — Watchlist / Monitor

```yaml
- ticker: TXN
  tier: 2
  direction: positive
  mechanism: >
    Texas Instruments manufactures analog and embedded processors primarily in
    US fabs (Richardson, TX; Lehi, UT; new Sherman, TX fab). Less direct
    exposure to Chinese semiconductor imports. Could benefit from reshoring
    tailwind, but analog semis are less tariff-sensitive than digital/logic.
  key_tests:
    - What percentage of TI's manufacturing is US-based?
    - Does the tariff cover analog semiconductor categories?
    - What is TI's China revenue exposure (end-market)?
  disconfirming_tests:
    - TI's end markets (auto, industrial) slow due to broader tariff uncertainty
    - Analog semis are excluded from tariff scope
    - TI's China revenue decline offsets any reshoring benefit
  required_next_step: Monitor tariff scope for analog inclusion; assess China revenue risk.

- ticker: LMT
  tier: 2
  direction: mixed
  mechanism: >
    Defense demand likely increases (national security rationale strengthens).
    However, rare earth export controls create supply risk for defense systems
    (missiles, fighters, radar). LMT has been building rare earth inventory
   