# HR Evaluation System — Business Prospect: Practical Cost (India)

**Document purpose:** Estimate the **practical monthly cost** of running the HR Evaluation System in India using **AWS EC2** (Mumbai region) and **Groq** for AI (resume parsing, psychometric grading, text assessment, and final rationale).  
All figures are indicative and based on Indian market context (INR, ap-south-1).

---

## 1. Cost components overview

| Component | Role | Billing |
|-----------|------|--------|
| **AWS EC2** | Hosting backend (Flask), frontend (static/build), and DB (e.g. on same instance or RDS) | Per hour (instance) + storage |
| **Groq** | LLM APIs: resume → JSON, psychometric grading, text grading, final AI rationale | Per token (input + output) |

**Exchange rate used:** 1 USD = ₹84 (indicative, for calculation only).

---

## 2. AWS EC2 (ap-south-1 — Mumbai)

### 2.1 Instance choice (practical for India)

Typical setup for small–medium usage (e.g. 50–500 candidates/month, few concurrent users):

| Option | Instance | vCPU | RAM | Use case |
|--------|----------|------|-----|----------|
| **A** | **t3.small** | 2 | 2 GiB | Low traffic, dev / pilot |
| **B** | **t3.medium** | 2 | 4 GiB | Production, moderate traffic |

### 2.2 Indicative pricing (ap-south-1, On-Demand, INR/month)

- **t3.small:** ~\$0.021/hr → **₹1,270/month** (24×30 hrs).  
- **t3.medium:** ~\$0.042/hr → **₹2,520/month** (24×30 hrs).

*Source: AWS EC2 On-Demand pricing ap-south-1; converted at ₹84/USD.*

### 2.3 Storage (EBS, gp3, ap-south-1)

- **~30 GB** for OS, app, logs, DB: ~\$0.10/GB-month → **~₹250/month**.

### 2.4 Data transfer

- First **100 GB out/month** (to internet) often free; beyond that ~\$0.12/GB.  
- For typical HR portal traffic (few TB/month unlikely), assume **₹0–500/month** unless you have heavy media/video.

### 2.5 AWS EC2 — Total (monthly, India)

| Setup | Instance | EBS (30 GB) | Approx. total (INR/month) |
|-------|----------|-------------|---------------------------|
| **Small** | t3.small | gp3 | **~₹1,520** |
| **Production** | t3.medium | gp3 | **~₹2,770** |

*If you use RDS (e.g. db.t3.micro) instead of DB on EC2, add roughly **₹1,500–2,000/month** for a small DB instance in ap-south-1.*

---

## 3. Groq — Practical figures (India context)

### 3.1 How the project uses Groq

- **llama-3.1-8b-instant:** Resume parsing, psychometric grading, psychometric narrative, text-response grading.  
- **llama-3.3-70b-versatile:** Final AI rationale (technical + soft skills + psychometric + resume fit + hire decision).

### 3.2 Groq pricing (token-based, USD)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|------------------------|------------------------|
| **Llama 3.1 8B (instant)** | $0.05 | $0.08 |
| **Llama 3.3 70B (versatile)** | $0.59 | $0.79 |

*Source: Groq public pricing; convert to INR at ₹84/USD.*

### 3.3 Token estimate per candidate (one full evaluation)

Rough per-candidate usage (one resume + one psychometric + one text assessment + one final rationale):

| Step | Model | Input (tokens) | Output (tokens) |
|------|--------|----------------|-----------------|
| Resume → JSON | 8B | ~2,500 | ~600 |
| Psychometric grading | 8B | ~1,200 | ~400 |
| Psychometric narrative | 8B | ~800 | ~150 |
| Text response grading | 8B | ~2,000 | ~400 |
| **Final rationale** | **70B** | ~5,000 | ~1,200 |
| **Total (approx.)** | — | **~11,500** | **~2,750** |

### 3.4 Cost per candidate (USD → INR)

- **8B share:** (8.5k input × $0.05 + 1.55k output × $0.08) / 1e6 ≈ **$0.00052**.  
- **70B share:** (5k input × $0.59 + 1.2k output × $0.79) / 1e6 ≈ **$0.0041**.  
- **Total per candidate:** ≈ **$0.0046** → **~₹0.39 per candidate** (at ₹84/USD).

So in practice: **under **₹0.50 per candidate** for AI (Groq) per full evaluation.**

### 3.5 Groq — Monthly cost (INR) by volume

| Candidates/month | Approx. Groq cost (INR/month) |
|------------------|-------------------------------|
| 100 | ~₹40 |
| 500 | ~₹200 |
| 1,000 | ~₹400 |
| 5,000 | ~₹2,000 |
| 10,000 | ~₹4,000 |

*Assumes same token mix as above; actual cost may vary with prompt size and output length.*

---

## 4. Combined practical cost (India)

### 4.1 Small setup (pilot / low volume)

- **EC2:** t3.small + 30 GB EBS → **~₹1,520/month**.  
- **Groq:** 200 candidates → **~₹80/month**.  
- **Total:** **~₹1,600/month**.

### 4.2 Production (medium volume)

- **EC2:** t3.medium + 30 GB EBS → **~₹2,770/month**.  
- **Groq:** 1,000 candidates → **~₹400/month**.  
- **Total:** **~₹3,170/month**.

### 4.3 Higher volume (e.g. 5,000 candidates)

- **EC2:** t3.medium (or larger) → **~₹2,770/month**.  
- **Groq:** 5,000 candidates → **~₹2,000/month**.  
- **Total:** **~₹4,770/month**.

*For very high concurrency, consider moving to a larger instance (e.g. t3.large) or multi-instance; DB on RDS would add ~₹1,500–2,000/month.*

---

## 5. Summary table (India, indicative)

| Item | Unit | Small (pilot) | Production (1k candidates) |
|------|------|----------------|----------------------------|
| **AWS EC2** | t3.small / t3.medium | ₹1,520 | ₹2,770 |
| **Groq** | Per candidate (~₹0.40) | ₹80 (200) | ₹400 (1,000) |
| **Total (INR/month)** | — | **~₹1,600** | **~₹3,200** |

---

## 6. Notes and caveats

1. **AWS:** Prices are On-Demand; 1-year or 3-year Reserved Instances can reduce EC2 cost by roughly **30–50%** in exchange for commitment.  
2. **Groq:** Free tier may cover initial testing; production usage is pay-per-token. Rates above are from public Groq pricing; verify on [Groq Pricing](https://groq.com/pricing).  
3. **Database:** If you use **Amazon RDS** in ap-south-1 instead of DB on EC2, add **~₹1,500–2,500/month** for a small instance.  
4. **Other costs:** Domain, SSL (e.g. ACM free), backup storage, and any third-party services (e.g. Supabase for storage) are not included; add as per your design.  
5. **Tax:** GST and TDS (if applicable) are not included; treat figures as pre-tax.

---

*This prospect is for planning only. Actual costs depend on usage, region, and current AWS/Groq pricing. Revisit figures at the time of budgeting or scaling.*
