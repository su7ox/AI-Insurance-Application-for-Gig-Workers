# GigInsurance — AI-Powered Parametric Income Insurance for Gig Workers

> **Persona:** Grocery & Q-Commerce Delivery Partners (Zepto / Blinkit)



## 🔍 Problem Statement

India's Q-Commerce delivery partners (Zepto, Blinkit etc.) are the backbone of the hyperlocal delivery economy. These gig workers operate in high-frequency, outdoor environments and are uniquely vulnerable to external disruptions — extreme weather, flooding, curfews, and platform outages — that directly cut into their daily earnings.

**Key pain points:**
- Gig workers can lose **20–30% of monthly income** during disruption events
- No existing income safety net is tailored to their week-to-week earning cycle
- Traditional insurance products are too slow, too complex, and don't cover income loss parametrically
- Workers bear the full financial burden with zero compensation when they cannot work through no fault of their own

> **Coverage Scope:** This platform exclusively covers **Loss of Income**. It does NOT cover health, life, accidents, vehicle repairs, or medical bills.

---

## 💡 Our Solution

**GigInsurance** is an AI-enabled, fully automated parametric income insurance platform built exclusively for Q-Commerce delivery partners. It:

- Calculates a **dynamic weekly premium** using real-time risk signals
- Triggers **automatic payouts** when verified disruptions occur — no claim filing needed
- Uses **platform-verified data** to prevent fraud at the source
- Operates on a **B2B2C model** where platforms co-fund the base cost

---

## 👤 Persona & Scenarios

**Primary Persona:** Rahul, a Zepto delivery partner in Noida
- Works 8–10 hours/day, 6 days/week
- Earns approximately ₹600–₹900/day
- Operates across 3–4 delivery zones in his area

### Scenario A — Heavy Rain Event
> Rahul's zone receives 85mm of rainfall in 6 hours. His platform marks deliveries as paused. GigShield detects the weather trigger via API, cross-references Rahul's active shift window, and automatically credits ₹280 to his wallet within minutes.

### Scenario B — Curfew / Section 144
> An unplanned curfew is imposed in Rahul's zone at 6 PM. GigShield detects the event via news and government feeds, validates that Rahul was logged in and active at curfew onset, and initiates a payout proportional to his remaining shift hours.

### Scenario C — App / Platform Outage
> The Zepto platform goes down for 3 hours during Rahul's peak shift. GigShield's platform API integration detects the outage duration and triggers a partial payout for verified affected hours.

---

## 🔄 Application Workflow

```
Worker Registration
       │
       ▼
Zone & Shift Profiling (via Platform API)
       │
       ▼
Weekly Premium Calculation (AI Risk Engine)
       │
       ▼
Policy Activation (48–72 hr waiting period)
       │
       ▼
Real-Time Disruption Monitoring
       │
  [Trigger Fired?]
       │
      YES
       │
       ▼
Automated Eligibility Verification
  ├── Is worker in affected zone? ✔
  ├── Was worker actively logged in? ✔
  └── Is disruption within shift window? ✔
       │
       ▼
Payout Calculation Engine
       │
       ▼
Instant Wallet Credit (Razorpay / UPI)
       │
       ▼
Worker Notification + Dashboard Update
```

---

## 💰 Weekly Premium Model

Our pricing system dynamically calculates a weekly insurance premium based on real-world risk factors. Unlike flat-fee models, GigShield uses AI-driven risk scoring to ensure fair, location-aware pricing.

### Core Formula

```
Weekly Premium = Base Fee + [Σ (Pᵢ × Max Payout × Sᵢ)] × (1 + M)
```

| Variable | Description |
|----------|-------------|
| `Pᵢ` | Probability of disruption event *i* (from AI model) |
| `Sᵢ` | Severity weight of event *i* |
| `Max Payout` | Maximum daily payout cap — ₹500 |
| `M` | Solvency margin — 10% |
| `Base Fee` | ₹20/week, covered by the platform (B2B2C) |

### Premium Tiers

| Risk Level | Risk Score (R) | Estimated Weekly Premium |
|------------|---------------|--------------------------|
| Low Risk | 0.1 – 0.3 | ₹30 – ₹60 |
| Medium Risk | 0.4 – 0.6 | ₹80 – ₹120 |
| High Risk | 0.7 – 1.0 | ₹120+ |

### B2B2C Cost Split

- **Platform (Zepto / Blinkit):** Pays base fee (~₹20/week/worker) — ensures operational sustainability
- **Worker:** Pays only the risk-adjusted premium on top — keeps pricing affordable

---

## ⚡ Parametric Triggers

Payouts are fully automated — no claims need to be filed by the worker. The system monitors the following triggers in real time:

| Trigger Type | Event | Data Source |
|---|---|---|
| 🌧️ Environmental | Heavy Rain (>50mm/6hr) | Weather API |
| 🌊 Environmental | Flood / Waterlogging | Government / Geospatial API |
| 🌡️ Environmental | Extreme Heat (>45°C) | Weather API |
| 😷 Environmental | Severe AQI (>300) | Pollution Monitoring API |
| 🌀 Environmental | Cyclone / Storm Warning | IMD API |
| 🚫 Social | Curfew / Section 144 | News / Government Feed |
| 🪧 Social | Local Strikes / Bandh | News / Event API |
| 📴 Platform | App / Platform Outage | Platform API (Mock) |
| 🌐 Social | Internet Shutdown | ISP / Government Alert Feed |

Each trigger is validated against:
- Worker's active GPS zone
- Platform-confirmed login/shift activity
- Cross-referenced disruption duration

---

## 🤖 AI/ML Integration

### 1. Risk Scoring Model

We use a **tree-based ensemble model (XGBoost)** trained on structured tabular inputs to generate a weekly Risk Score `R ∈ [0, 1]`.

**Feature Inputs:**
- Rainfall (mm), Temperature (°C), AQI levels
- Flood-zone classification (geospatial)
- Historical disruption frequency for the worker's zone
- Scheduled events (strikes, elections, holidays)
- Platform-specific demand patterns

**Output:** Risk Score `R` used directly in the premium formula.

### 2. Dynamic Premium Recalculation

Premiums are recalculated every Monday using the latest week's forecast data — ensuring workers in a zone with an upcoming cyclone pay a risk-appropriate premium before the event.

### 3. Anomaly Detection (Fraud Layer)

A lightweight **Isolation Forest / rule-based anomaly detector** flags:
- Sudden spikes in claim density from a single zone
- Claims filed for events that did not overlap a logged shift
- Workers claiming from zones they were not assigned to

---

## 🔐 Fraud Prevention

### Problem → Solution Matrix

| Fraud Vector | Detection Mechanism |
|---|---|
| GPS Spoofing / Fake Location | Zone matching via Platform API — not device GPS |
| Fake Shift Hours | Only platform-recorded activity counts — no manual input |
| Last-Minute Policy Purchase | **48–72 hour waiting period** before policy activates |
| Coordinated Mass Fraud | Anomaly detection flags unusual claim clusters |
| Duplicate Claims | De-duplication at the database layer (PostgreSQL constraints) |
| Unauthorized Zone Claims | Worker zone must match disruption zone exactly |

### System Load Factor (SLF)

During large-scale disruptions where many workers claim simultaneously, a **System Load Factor** smoothly scales individual payouts to maintain solvency:

```
SLF = 1 / (1 + α × C)
```

Where `C` = claim density (0–1) and `α` ≈ 0.5.

This prevents financial instability while remaining fair — no sudden or arbitrary cuts.

---

## 💸 Payout Engine

### Step-by-Step Calculation

**Step 1 — Protected Hourly Rate (PHR)**
```
PHR = (Premium / Risk Score) × k     [k ≈ 0.4]
```
Normalizes payout fairness across high-risk and low-risk zones.

**Step 2 — Effective Hours**
```
Effective Hours = Shift Window ∩ Disruption Window
```
Only hours where the worker's shift overlapped with the disruption count.

**Step 3 — Apply System Load Factor**
```
Adjusted Rate = PHR × SLF
```

**Step 4 — Final Payout**
```
Final Payout = min(Adjusted Rate × Effective Hours, ₹500)
```

**Payment Channel:** Razorpay (Test Mode) / UPI Simulator — credited to worker's in-app wallet within minutes of trigger verification.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Mobile Frontend** | Flutter (Android + iOS) | Cross-platform worker app, real-time notifications |
| **Backend API** | Node.js + Express.js | REST APIs, authentication, business logic |
| **AI / ML** | Python, XGBoost, Scikit-learn | Risk scoring, anomaly detection |
| **Database** | PostgreSQL | Policies, payouts, user data — structured financial records |
| **Cloud** | AWS / GCP | Backend hosting, scalable API deployment |
| **Weather Data** | OpenWeatherMap API / IMD (mock) | Rainfall, temperature, AQI forecasts |
| **Platform Data** | Zepto / Blinkit API (mock/simulated) | Worker verification, zone, shift data |
| **Payments** | Razorpay (Test Mode) / UPI Simulator | Simulated instant payout to worker wallet |
| **Auth** | JWT (JSON Web Tokens) | Secure session management |
| **Monitoring** | Firebase / Custom Dashboard | Claim tracking, payout analytics, loss ratios |

---

## 📱 Platform Choice Justification

**We chose a Mobile-First approach (Flutter)** for the following reasons:

- Q-Commerce delivery workers are smartphone-native — they already use Zepto/Blinkit apps on mobile for all work activity
- Push notifications are essential for real-time disruption alerts and payout confirmations
- Flutter enables a single codebase for both Android (dominant in India's gig workforce) and iOS
- A web dashboard is additionally provided for insurers / admins to view analytics and loss ratios

---

## 📅 Development Plan

### Phase 1 — Ideation & Foundation (Weeks 1–2) ✅
- [x] Persona definition and scenario mapping
- [x] Weekly premium model design
- [x] Parametric trigger selection and justification
- [x] Tech stack finalization
- [x] README and repository setup
- [x] 2-minute prototype walkthrough video

### Phase 2 — Automation & Protection (Weeks 3–4)
- [ ] Worker registration and onboarding flow
- [ ] Insurance policy creation with weekly pricing
- [ ] Dynamic premium calculation engine (XGBoost model)
- [ ] Claims management module
- [ ] 3–5 automated disruption trigger integrations (mock APIs)
- [ ] Zero-touch claim initiation prototype

### Phase 3 — Scale & Optimise (Weeks 5–6)
- [ ] Advanced fraud detection (GPS spoofing, coordinated claims)
- [ ] Instant payout simulation (Razorpay test mode / UPI)
- [ ] Worker dashboard: earnings protected, active coverage
- [ ] Insurer/admin dashboard: loss ratios, predictive analytics
- [ ] Final 5-minute demo video
- [ ] Final pitch deck (PDF)

---

## 👥 Team

> *(Add team name and member details here)*

---

## 📎 Submission Links

| Deliverable | Link |
|---|---|
| GitHub Repository | *(this repo)* |
| 2-Minute Video (Phase 1) | *(add link)* |
| Demo Video (Phase 2) | *(add link after Phase 2)* |
| Final Demo Video (Phase 3) | *(add link after Phase 3)* |
| Final Pitch Deck | *(add link after Phase 3)* |

---

> *"We verify real work, prevent fake claims, and ensure fair payouts — even during large-scale disruptions."*

---
