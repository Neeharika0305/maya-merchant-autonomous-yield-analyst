# MAYA — Merchant Autonomous Yield Analyst

> **Let AI discover. Test. Prove. Adapt.**

**MAYA** is an autonomous AI growth analyst designed for merchants. Instead of simply reporting what happened in a business, MAYA continuously **discovers growth opportunities, generates competing hypotheses, runs controlled experiments, validates economic impact, detects failures, and adapts its strategy autonomously.**

Built for the **Razorpay AI Buildathon 2026**.

---

## 🚀 The Problem

Most merchant analytics systems stop at:

* What happened?
* Which products sold?
* Which customers converted?
* Where did revenue decrease?

But analytics alone does not create growth.

A merchant needs an intelligent system that can answer:

> **What should we test next, why should we test it, and did it actually work?**

MAYA turns merchant data into an **autonomous experimentation and decision-making loop.**

---

## 🎯 Objectives

The primary objective of MAYA is to build an autonomous, AI-driven growth intelligence system that can move beyond traditional analytics and actively discover, validate, and learn from merchant growth opportunities.

### Key Objectives

* **Autonomously discover growth opportunities** from merchant transaction, customer, and product behavior data.

* **Generate and compare competing hypotheses** instead of relying on a single recommendation.

* **Design controlled experiments** with clear targets, metrics, control groups, and treatment strategies.

* **Validate economic impact** by considering conversion lift, incremental revenue, incentive cost, margin, ROI, and statistical confidence.

* **Detect and diagnose experiment failures** rather than treating unsuccessful experiments as dead ends.

* **Adapt strategies autonomously** by refining audiences, offers, or experiment parameters based on observed outcomes.

* **Create a continuous learning loop** of **Discover → Test → Measure → Diagnose → Adapt → Re-test**.

* **Prioritize profitable and sustainable growth**, ensuring that increased conversions do not come at the cost of merchant profitability.

* **Prove growth through measurable evidence**, transforming AI recommendations into validated and repeatable business outcomes.

---


## 💡 What MAYA Does

MAYA follows a closed-loop growth intelligence workflow:

```text
Merchant Data
     ↓
Opportunity Discovery
     ↓
Hypothesis Generation
     ↓
Hypothesis Competition
     ↓
Experiment Design
     ↓
Safety & Economic Validation
     ↓
Experiment Execution
     ↓
Outcome Analysis
     ↓
Failure Detection
     ↓
Root-Cause Diagnosis
     ↓
Audience / Strategy Adaptation
     ↓
Re-test
     ↓
Proven Growth
```

The key idea is:

> **MAYA does not just recommend growth. It tries to prove it.**

---

## 🧠 Core Capabilities

### 1. Autonomous Opportunity Discovery

MAYA analyzes merchant transaction and customer behavior data to identify potential growth opportunities such as:

* Cross-sell opportunities
* Product affinity
* Customer segments
* Underperforming audiences
* Revenue leakage
* Conversion opportunities

### 2. Competing Hypotheses

Instead of immediately accepting the first idea, MAYA evaluates competing explanations and opportunities.

For example:

```text
Opportunity:
Earbuds customers may need an additional accessory.

Candidate hypotheses:
→ USB-C Cable
→ Protective Case
→ Wireless Charger
```

MAYA evaluates which opportunity has the strongest potential.

### 3. Experiment Design

MAYA converts an opportunity into a measurable experiment.

Example:

```text
Target:
Earbuds purchasers

Experiment:
USB-C Cable cross-sell

Treatment:
Personalized incentive

Control:
No incentive

Metric:
Conversion Lift

Guardrails:
Margin + Discount Limits
```

### 4. Economic Validation

A growth experiment should not be considered successful simply because conversions increase.

MAYA evaluates:

* Conversion lift
* Incremental revenue
* Incentive cost
* Margin impact
* ROI
* Statistical confidence
* Safety constraints

This prevents the system from recommending growth that destroys profitability.

### 5. Failure Detection

MAYA does not assume every experiment will succeed.

If an experiment performs poorly, MAYA identifies the failure instead of hiding it.

Example:

```text
Experiment Result

Status: FAILED

Observed:
Low conversion lift

Diagnosis:
Audience too broad

Action:
Refine target audience
```

### 6. Autonomous Adaptation

After detecting failure, MAYA changes its strategy.

```text
Broad Audience
      ↓
Experiment Failed
      ↓
Root Cause Analysis
      ↓
Audience Narrowing
      ↓
Re-test
      ↓
Positive Lift
```

This creates a genuine **learn → adapt → re-test** loop.

---

## 📊 Demonstrated Outcome

In the demonstrated MAYA workflow:

| Metric              |        Result |
| ------------------- | ------------: |
| Revenue Recovered   |   **₹39,477** |
| Conversion Lift     |   **+8.3 pp** |
| Recovery Multiplier |     **3.93×** |
| Final Status        | **RECOVERED** |

The important result is not just the revenue number.

MAYA:

**discovered → challenged → tested → measured → failed → diagnosed → adapted → recovered**

---

## 🏆 What Makes MAYA Different?

Traditional analytics:

```text
DATA
 ↓
DASHBOARD
 ↓
HUMAN DECISION
```

Recommendation systems:

```text
DATA
 ↓
RECOMMENDATION
 ↓
HUMAN ACTION
```

MAYA:

```text
DATA
 ↓
DISCOVER
 ↓
HYPOTHESIZE
 ↓
EXPERIMENT
 ↓
MEASURE
 ↓
DIAGNOSE
 ↓
ADAPT
 ↓
PROVE
```

MAYA is designed as an **agentic decision system**, not just a dashboard or chatbot.

---

## 🛡️ Safety-First Growth

Autonomous experimentation requires guardrails.

MAYA incorporates constraints around:

* Discount limits
* Margin protection
* Experiment validity
* Economic viability
* Audience targeting
* Failure detection
* Recovery validation

The objective is not:

> **Maximize conversions at any cost.**

It is:

> **Find profitable, measurable, and repeatable growth.**

---

## 🏗️ Architecture



```text
                    ┌──────────────────────┐
                    │   Merchant Data      │
                    │ Transactions / Users │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Opportunity Engine   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Hypothesis Engine    │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Experiment Planner   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Safety & Economics   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Experiment Execution │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Outcome Analyzer     │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Failure Diagnosis    │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Adaptive Strategy    │
                    └──────────┬───────────┘
                               │
                               └──────→ Re-test
```

---

## 🧰 Tech Stack

### Frontend

* React
* Vite
* Modern responsive UI

### Backend

* Python
* FastAPI

### Data & Analytics

* Pandas
* NumPy
* Statistical experimentation
* Customer segmentation
* Revenue / conversion analysis

### AI

* LLM-powered reasoning
* Autonomous hypothesis generation
* Experiment planning
* Failure diagnosis
* Adaptive decision-making

### Deployment

* Vercel

---

## 🎯 Example Autonomous Journey

### Step 1 — Discover

MAYA identifies a potential cross-sell opportunity:

**Earbuds → USB-C Cable**

### Step 2 — Challenge

MAYA evaluates alternative products and selects the strongest opportunity.

### Step 3 — Experiment

It designs a USB-C Cable incentive experiment.

### Step 4 — Detect Failure

The initial broad audience does not produce sufficient lift.

**Status: FAILED**

### Step 5 — Diagnose

MAYA determines that the audience is too broad.

### Step 6 — Adapt

The system narrows the audience to a higher-propensity segment.

### Step 7 — Re-test

The adapted experiment produces:

**+8.3 percentage points conversion lift**

### Step 8 — Prove

MAYA validates the resulting economics and marks the opportunity:

**RECOVERED**

---

## 🌟 Key Innovation

MAYA's central innovation is its **closed-loop autonomous experimentation architecture**.

It does not treat failure as the end of an experiment.

Instead:

> **Failure becomes a signal for adaptation.**

This enables MAYA to move from:

**Analytics → Recommendations → Autonomous Growth Learning**

---

## 🔮 Future Scope

MAYA can evolve toward production-scale merchant intelligence with:

* Real-time payment and transaction signals
* Automated campaign execution
* Multi-armed bandit experimentation
* Reinforcement learning
* Long-term customer lifetime value optimization
* Multi-channel experimentation
* Real-time anomaly detection
* Merchant-specific AI agents
* Automated budget allocation
* Continuous experimentation across merchant portfolios

---

## 🎥 Demo

**Live Demo:** [https://maya-nine-theta.vercel.app/](https://maya-nine-theta.vercel.app/)

Click “Run MAYA” to start the autonomous growth workflow.

The demo showcases MAYA’s complete agentic workflow — from opportunity discovery and hypothesis generation to experimentation, failure diagnosis, adaptive decision-making, and recovery.

Workflow: 
Discover → Decide → Experiment → Detect Failure → Diagnose → Adapt → Recover
---

## 🏁 Built For

### Razorpay AI Buildathon 2026

**MAYA — Merchant Autonomous Yield Analyst**

> **Don't tell merchants where they can grow.
> Let AI discover, test, and prove it.**
