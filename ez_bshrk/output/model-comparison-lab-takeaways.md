# Takeaways: Model Comparison Lab & Jupyter Workflow

## 1. Prompt Following vs. Output Control
- Models can violate explicit constraints (e.g. “answer only with the question”) even when the prompt is clear.
- Token limits don’t guarantee compliance:
  - Too low → empty output
  - Higher → verbose overproduction
- Asking for one sentence materially changes behavior compared to open-ended prompts.

## 2. Model Behavior Differences
- Different models show strong stylistic biases:
  - Some default to consulting briefs / RFP-style outputs
  - Others aim for philosophical concision
- Several models use inclusive language (“our consciousness”) when discussing humans.
- Formatting quality varies greatly (tables, structure, polish), sometimes independent of argument quality.

## 3. Judge Models Are Fallible
- “AI judging AI” introduces its own failure modes:
  - Incorrect counting (missing competitors)
  - Ranking inconsistencies
- This reinforces that evaluation logic must be validated, not assumed correct.
- Multiple judges or sanity checks are necessary for robustness.

## 4. Token Accounting Reality
- Character length ≠ token count.
- Models may silently truncate, refuse, or reshape outputs under tight limits.
- Explicit word/token caps help, but are not strictly enforced.

## 5. Jupyter-Specific Observations
- Notebook execution order can obscure:
  - When variables were last updated
  - Which outputs correspond to which run
- Variable inspectors help, but struggle with long strings.
- HTML export works, but is fragile and not iteration-friendly.

## 6. Pretty Notebook Output
- Styled “Exercise” blocks are not special widgets.
- They are produced via:
  - Markdown cells with inline HTML/CSS, or
  - IPython.display.HTML
- Jupyter allows raw HTML inside Markdown cells.

## 7. Meta Takeaway
- The lab is less about coding and more about:
  - Model incentives
  - Instruction-following limits
  - Evaluation pitfalls
- Theoretical reasoning and skepticism matter as much as implementation.

---

Overall:  
Agentic systems amplify model quirks rather than hide them.  
Evaluation, constraints, and presentation all need explicit design.

Comments:


