# Contract Revenue Radar Report

- Backend: local-hash-vector-fallback
- Sections searched: 8
- Revenue risk score: 100/100

## Priority Actions
- Ask for Net 15/30, milestone billing, or acceptance deemed after a fixed review window.
- Carve out pre-existing IP, tools, methodologies, and generic components; grant a limited non-exclusive license instead of full assignment; retain ownership of reusable assets.
- Define change orders, revision limits, support hours, and out-of-scope rates.
- Add annual renewal, longer notice, migration fee, or success review before termination.
- Require explicit written renewal election, cap annual increases (e.g. CPI or 3%), provide easy 30-60 day opt-out, and keep renewal pricing fixed for initial term.

## Findings

### Payment delay - severity 5/5
- Source: saas_msa_example.md / 3. Payment Terms
- Match score: 0.708
- Matched terms: net 60, sole discretion
- Why it matters: Cash conversion risk: payment timing depends on buyer action or long terms.
- Recommended move: Ask for Net 15/30, milestone billing, or acceptance deemed after a fixed review window.

> Customer shall pay all undisputed invoices within Net 60 days following acceptance of the applicable deliverable by Customer's designated project manager. Acceptance shall occur only after Customer has completed internal testing and stakeholder sign-off, which may be withheld in ...

### IP ownership trap - severity 4/5
- Source: saas_msa_example.md / 2. Intellectual Property
- Match score: 0.953
- Matched terms: work made for hire, all intellectual property, assigns to customer
- Why it matters: Revenue and reuse risk: broad IP assignment prevents the agency from reusing methodologies, code patterns, frameworks, or IP developed on the engagement in future client work, directly eroding future margins.
- Recommended move: Carve out pre-existing IP, tools, methodologies, and generic components; grant a limited non-exclusive license instead of full assignment; retain ownership of reusable assets.

> ... stom configurations, reports, and materials created under this Agreement shall be considered work made for hire and shall become the sole and exclusive property of Customer upon creation. Provider hereby irrevocably assigns to Customer all right, title, and interest in and to all ...

### Scope creep - severity 4/5
- Source: saas_msa_example.md / 1. Services and Deliverables
- Match score: 0.867
- Matched terms: reasonable requests
- Why it matters: Margin risk: vague service language can expand work without expanding fees.
- Recommended move: Define change orders, revision limits, support hours, and out-of-scope rates.

> ... going support services for the SaaS platform as described in Statement of Work exhibits. All reasonable requests for assistance during the implementation phase are included at no additional charge. Provider agrees to perform all work necessary to achieve go-live success.

### Renewal loss - severity 4/5
- Source: saas_msa_example.md / 4. Term and Renewal
- Match score: 0.717
- Matched terms: non-renew
- Why it matters: Retention risk: the customer can leave quickly or renewal is not protected.
- Recommended move: Add annual renewal, longer notice, migration fee, or success review before termination.

> ... month renewal terms at the then-current rates unless either party provides written notice of non-renewal at least thirty (30) days prior to the end of the then-current term.

### Auto-renewal fee escalation - severity 3/5
- Source: saas_msa_example.md / 4. Term and Renewal
- Match score: 0.736
- Matched terms: renewal term, then-current rates
- Why it matters: Hidden cost and retention risk: automatic renewal at escalated 'then-current' rates or without price caps locks clients into compounding fees and removes leverage for renegotiation.
- Recommended move: Require explicit written renewal election, cap annual increases (e.g. CPI or 3%), provide easy 30-60 day opt-out, and keep renewal pricing fixed for initial term.

> ... months. Thereafter, the Agreement shall automatically renew for successive twelve (12) month renewal terms at the then-current rates unless either party provides written notice of non-renewal at least thirty (30) days prior to the end of the then-current term.

### Data/security blocker - severity 3/5
- Source: saas_msa_example.md / 7. Data and Security
- Match score: 0.704
- Matched terms: audit rights, subprocessor
- Why it matters: Sales cycle risk: security or data terms can block signature if not answered quickly.
- Recommended move: Prepare a security appendix, DPA, incident process, and approved subprocessor list.

> Provider shall implement reasonable security measures. Customer retains full audit rights over Provider's systems and subprocessors at any time with 24 hours notice. Upon termination, Provider shall delete all Customer data and certify destruction within ten (10) business days.

### Refund or credit exposure - severity 3/5
- Source: saas_msa_example.md / 6. Service Levels and Remedies
- Match score: 0.667
- Matched terms: service credits
- Why it matters: Revenue leakage risk: broad refund or credit language can erase earned revenue.
- Recommended move: Tie credits to measurable SLA misses and cap credits to monthly fees paid.

> ... vider commits to 99.5% uptime. In the event of any SLA breach, Customer shall be entitled to service credits equal to two times the fees attributable to the affected period, applied against future invoices, plus any direct damages.

### Refund or credit exposure - severity 3/5
- Source: saas_msa_example.md / 5. Termination
- Match score: 0.43
- Matched terms: full refund
- Why it matters: Revenue leakage risk: broad refund or credit language can erase earned revenue.
- Recommended move: Tie credits to measurable SLA misses and cap credits to monthly fees paid.

> ... venience upon sixty (60) days prior written notice. Upon termination, Customer may request a full refund of any prepaid but unused fees.

### Refund or credit exposure - severity 3/5
- Source: saas_msa_example.md / 8. Limitation of Liability
- Match score: 0.328
- Matched terms: service credits
- Why it matters: Revenue leakage risk: broad refund or credit language can erase earned revenue.
- Recommended move: Tie credits to measurable SLA misses and cap credits to monthly fees paid.

> ... in the twelve months preceding the claim. Customer's sole remedies for SLA failures are the service credits described above.

# Revenue Terms Agent Brief

## Executive Summary

The reviewed documents show a 100/100 revenue risk score. Highest-priority issues: payment delay, ip ownership trap, scope creep. Route these clauses through business review before legal markup.

## Priority Questions
- Can saas_msa_example.md / 3. Payment Terms be changed so payment is due on a fixed date or milestone?
- Does saas_msa_example.md / 2. Intellectual Property carve out pre-existing IP and reusable methodologies for the vendor?
- Where is the change-order boundary for saas_msa_example.md / 1. Services and Deliverables?
- Who approves the termination or non-renewal language in saas_msa_example.md / 4. Term and Renewal?
- Can saas_msa_example.md / 4. Term and Renewal add explicit renewal election and price caps instead of auto-escalation?

## Fallback Positions
- Replace open-ended acceptance with deemed acceptance after 5 business days. Use Net 15 or milestone billing for implementation work.
- Carve out pre-existing IP, tools, methodologies, and generic components. Grant limited license only; retain ownership of reusable IP and background assets.
- Add a written change-order requirement for work outside the SOW. Define included support hours, revision limits, and out-of-scope rates.
- Move month-to-month service terms to annual renewal where possible. Use at least 60 days notice before non-renewal.
- Require explicit written renewal election. Cap annual price increases at CPI or 3%. Add easy 30-60 day opt-out without penalty and keep initial renewal pricing fixed.

## Sales/Ops Checklist
- Confirm payment due date is not dependent on unilateral customer acceptance.
- Confirm change requests require written approval before work begins.
- Confirm renewals, non-renewals, and convenience termination have business owner approval.
- Confirm credits, refunds, or SLA remedies are capped.
- Confirm data/security obligations map to an approved appendix or review owner.
- Confirm IP clauses carve out pre-existing tools/methods and avoid full assignment of reusable work.
- Confirm auto-renewal terms include explicit election, price caps, and easy opt-out.

## Limit

This is business-risk review, not legal advice. Counsel should approve final language.
