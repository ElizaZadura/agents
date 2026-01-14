# CrewAI Project Plan

This document captures the *current agreed plan* for building a **spec-driven, modular CrewAI engineering team**. It is intentionally minimal and process-focused. We will extend it incrementally.

(Instructions - add structured output (output pydantic or output json). Add dynamic creation of tasks. Callbacks can be created at the task level.)

---

## Goal

Build a reusable CrewAI crew that:

- Accepts an **arbitrary product specification** as input
- Transforms it into a structured plan
- Delegates work across specialist agents
- Produces a **modular Python application** (not a single-file script)
- Operates within clear limits (iterations, scope, cost)

The focus is **workflow, delegation, and cooperation**, not feature complexity.

---

## Core Principles

- **Spec-driven**: The team is built to handle unknown specs.
- **Contract-first**: No building before interfaces/contracts exist.
- **Strict ownership**: Each agent owns a specific area.
- **Phase gates**: Work only progresses when required artifacts exist.
- **Minimalism**: Start small, add complexity later.

---

## Agents (Current)

### 1. Engineering Lead

- Owns: scope, delegation, gates, integration
- Converts raw specs into structured artifacts
- Approves or rejects work
- Does not implement features unless necessary

### 2. Core Domain Engineer

- Owns: domain logic and invariants
- Works strictly within approved contracts
- No UI or infrastructure decisions

### 3. UI Engineer

- Owns: UI layer (e.g. Gradio)
- Implements against domain contracts
- Keeps UI thin and explicit

### 4. Test / Infrastructure Engineer

- Owns: tests, dependencies, run instructions
- Defines what “done” means in verifiable terms
- Surfaces missing or optional dependencies

**Rule:** Agents do not modify areas they don’t own without review.

---

## Task Flow (Initial)

### Task 1 — Spec Intake & Framing

**Owner:** Engineering Lead

**Input:** `{spec}` (plain text product specification)

**Output:** A *Spec Pack* with fixed sections:

- Functional requirements
- Non-functional constraints
- Acceptance criteria
- Out of scope
- Open questions

**Gate:** No other task may start until the Spec Pack exists.

---

### Task 2 — Architecture & Contracts *(planned next)*

**Consumes:** Spec Pack

**Produces:**

- Module breakdown
- Ownership assignments
- Interface / contract definitions

**Gate:** No implementation before contracts are approved.

---

### Task 3 — Implementation *(planned)*

- Parallel work by specialists
- Implementation strictly follows contracts
- Tests written alongside code

---

### Task 4 — Review & Integration *(planned)*

- Lead verifies:
  - Code runs
  - Tests pass
  - Structure is modular
  - Dependencies are documented

---

## Modularity Requirements

(Default layout, subject to refinement)

- `src/<appname>/domain/`
- `src/<appname>/services/`
- `src/<appname>/ui/`
- `tests/`
- `README.md`

**Gate:** Reject if logic collapses into a single file.

---

## What We Are *Not* Doing Yet

- No advanced planning features
- No tool overload
- No domain-specific assumptions
- No premature optimization

---

## Next Step

Define **Task 2: Architecture & Contracts** in `tasks.yaml`, following the same minimal CrewAI pattern as Task 1.

---

*(This file is intentionally simple. We will extend it as the crew evolves.)*
