# Contract Revenue Radar Report

- Backend: qdrant-local-memory
- Sections searched: 5
- Revenue risk score: 96/100

## Priority Actions
- Ask for Net 15/30, milestone billing, or acceptance deemed after a fixed review window.
- Add annual renewal, longer notice, migration fee, or success review before termination.
- Define change orders, revision limits, support hours, and out-of-scope rates.
- Prepare a security appendix, DPA, incident process, and approved subprocessor list.
- Tie credits to measurable SLA misses and cap credits to monthly fees paid.

## Findings

### Payment delay - severity 5/5
- Source: acme_services_agreement.md / 2. Payment Terms
- Match score: 0.552
- Matched terms: net 90, after acceptance, sole discretion
- Why it matters: Cash conversion risk: payment timing depends on buyer action or long terms.
- Recommended move: Ask for Net 15/30, milestone billing, or acceptance deemed after a fixed review window.

> Customer will pay invoices on Net 90 terms after acceptance by the Customer project owner. Acceptance may be delayed at Customer's sole discretion until all internal stakeholders approve the deliverables.

### Renewal loss - severity 4/5
- Source: acme_services_agreement.md / 3. Renewals and Termination
- Match score: 0.738
- Matched terms: terminate for convenience, 30 days notice, without cause, month-to-month
- Why it matters: Retention risk: the customer can leave quickly or renewal is not protected.
- Recommended move: Add annual renewal, longer notice, migration fee, or success review before termination.

> The subscription is month-to-month after the initial launch. Customer may terminate for convenience without cause with 30 days notice.

### Scope creep - severity 4/5
- Source: acme_services_agreement.md / 1. Services
- Match score: 0.709
- Matched terms: reasonable requests, as requested, additional support, included at no charge
- Why it matters: Margin risk: vague service language can expand work without expanding fees.
- Recommended move: Define change orders, revision limits, support hours, and out-of-scope rates.

> Vendor will provide implementation support, training, and additional support as requested by Customer. Vendor agrees that reasonable requests connected to rollout are included at no charge.

### Data/security blocker - severity 3/5
- Source: acme_services_agreement.md / 5. Data Handling
- Match score: 0.668
- Matched terms: personal data, confidential information, audit rights, delete all data
- Why it matters: Sales cycle risk: security or data terms can block signature if not answered quickly.
- Recommended move: Prepare a security appendix, DPA, incident process, and approved subprocessor list.

> Vendor may process personal data and confidential information. Customer reserves audit rights and may require Vendor to delete all data within five business days after termination.

### Refund or credit exposure - severity 3/5
- Source: acme_services_agreement.md / 4. Service Levels
- Match score: 0.476
- Matched terms: service credits
- Why it matters: Revenue leakage risk: broad refund or credit language can erase earned revenue.
- Recommended move: Tie credits to measurable SLA misses and cap credits to monthly fees paid.

> ... he service is unavailable for more than four hours in a calendar month, Customer may request service credits against future invoices.

# Revenue Risk Agent Brief

## Executive Summary

The reviewed documents show a 96/100 revenue risk score. Highest-priority issues: payment delay, renewal loss, scope creep. Route these clauses through business review before legal markup.

## Priority Questions
- Can acme_services_agreement.md / 2. Payment Terms be changed so payment is due on a fixed date or milestone?
- Who approves the termination or non-renewal language in acme_services_agreement.md / 3. Renewals and Termination?
- Where is the change-order boundary for acme_services_agreement.md / 1. Services?
- Who owns the security and data obligations in acme_services_agreement.md / 5. Data Handling?
- Are credits or refunds capped in acme_services_agreement.md / 4. Service Levels?

## Fallback Positions
- Replace open-ended acceptance with deemed acceptance after 5 business days. Use Net 15 or milestone billing for implementation work.
- Move month-to-month service terms to annual renewal where possible. Use at least 60 days notice before non-renewal.
- Add a written change-order requirement for work outside the SOW. Define included support hours, revision limits, and out-of-scope rates.
- Route security terms to a standard security appendix, DPA, incident process, and approved subprocessor list.
- Cap credits to fees paid for the affected month. Make credits the sole remedy for verified SLA misses.

## Sales/Ops Checklist
- Confirm payment due date is not dependent on unilateral customer acceptance.
- Confirm change requests require written approval before work begins.
- Confirm renewals, non-renewals, and convenience termination have business owner approval.
- Confirm credits, refunds, or SLA remedies are capped.
- Confirm data/security obligations map to an approved appendix or review owner.

## Limit

This is business-risk review, not legal advice. Counsel should approve final language.
