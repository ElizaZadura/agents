# Notes: "Latest news" and "new companies" in agent tasks

## Context

In the current agents/tasks setup, task descriptions include phrases like:

* "search the latest news"
* "find new companies you’ve not found before"

Whether these do what you expect depends **entirely** on tool wiring and state handling — not the wording alone.

---

## 1. "Latest" only works if a search tool is actually wired

* Writing "latest news" in a prompt **does not override training cutoff** by itself.
* It only works if the framework injects a live search/browsing tool into the agent runtime.

**If a search tool *is wired*:**

* "latest" acts as a routing hint (good).

**If no search tool is wired:**

* The model will approximate “trending” using training priors → stale-ish results.

### Recommendation

Make recency explicit and bounded:

> "Search news from the last **7 days** (or **30 days**)."

This avoids vague temporal language.

---

## 2. "New companies" requires state — otherwise it’s ill-defined

You currently instruct agents to:

* "Find companies you’ve not found before"
* "Always pick new companies"

But unless the system:

* passes prior results into the prompt, **or**
* persists memory between runs

…the agent has no real definition of *before*.

In practice, this means:

* The instruction is ignored, **or**
* The model fakes novelty within a single output only.

---

## 3. Minimal ways to fix the "new" requirement

### Option A — Explicit exclusion list (cleanest)

Add a parameter like `{exclude_companies}` and inject it from orchestration:

> "Find 2–3 trending companies in {sector} from the last 7 days. Exclude any in {exclude_companies}."

Even an empty list makes the constraint explicit and extensible.

---

### Option B — Persist seen companies to disk

Since outputs are already written to files:

* Maintain something like `output/seen_companies.json`
* Update it after each run
* Inject it into the next prompt context

This gives the agent **actual memory**, not vibes.

---

## 4. Same issue applies downstream

The same state problem affects:

* `research_trending_companies`
* `stock_picker` ("don’t pick the same company twice")

Any instruction about *uniqueness across runs* requires persisted state.

---

## Quick takeaway

* "Latest" → only real if a search tool is wired
* "New" → meaningless without state
* Fix with:

  * explicit time windows
  * explicit exclusion lists
  * or lightweight persistence

This keeps the agent loop honest instead of placebo-driven.
