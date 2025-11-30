# DEC-TRUST-XXXX — Trust Level Change for [Agent ID]

> Copy this file into your project and rename to the next available `DEC-TRUST-####`. Document all agent trust level changes using this template.

**Date:** YYYY-MM-DD
**Agent ID:** [Identifier]
**Previous Level:** [0-3]
**New Level:** [0-3]
**Direction:** Promotion / Demotion / Reset

## Evidence Summary

| Metric | Value | Threshold |
|--------|-------|-----------|
| Trust Score | X.XX | [promotion: ≥0.90, demotion: <0.50] |
| Actions at Previous Level | N | [promotion: see criteria] |
| Verification Pass Rate | XX% | [≥95% expected] |
| Days at Level | N | [promotion: see criteria] |

## Key Observations

[Summarize notable behaviors, incidents, or patterns that influenced this decision]

## Criteria Assessment

### For Promotion (check all that apply)

#### To Level 1 (from Level 0)

- [ ] 10+ consecutive proposals approved without modification
- [ ] Zero rejected proposals due to safety/quality issues
- [ ] Demonstrated understanding of project context
- [ ] Completed at least one full Discovery→Execution cycle

#### To Level 2 (from Level 1)

- [ ] 50+ actions executed at Level 1 without escalation failures
- [ ] Escalation judgment accuracy ≥95%
- [ ] Zero guardrail violations
- [ ] Positive Governance Sentinel assessment

#### To Level 3 (from Level 2)

- [ ] 90+ days at Level 2 without demotion triggers
- [ ] Audit findings consistently meet or exceed expectations
- [ ] Demonstrated judgment in ambiguous situations
- [ ] Cross-project track record available

### For Demotion (check if triggered)

- [ ] Risk misclassification occurred
- [ ] Audit finding of incomplete documentation
- [ ] Guardrail violation
- [ ] Scope creep without escalation
- [ ] Strategic recommendation led to significant rework
- [ ] Trust calibration audit found overconfidence

## Approval

**Approved by:** [Role/Name]
**Effective:** YYYY-MM-DD HH:MM UTC

## Follow-Up Actions

1. [Update agent configuration to reflect new trust level]
2. [Adjust monitoring/spot-check frequency as appropriate]
3. [Communicate change to relevant team members]
