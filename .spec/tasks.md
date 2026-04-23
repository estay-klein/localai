# Project Tasks - LocalAI Stack

## Task Status Legend
- **TODO** – Not started
- **IN_PROGRESS** – Actively being implemented
- **BLOCKED** – Waiting on external dependency or decision
- **DONE** – Completed and verified
- **CANCELLED** – Abandoned (with reason)

## Current Tasks

### [DONE] TASK-004: Eliminate redis and supervisord profiles, clarify only 2 profiles exist
**Created:** 2026-04-20
**Assignee:** Roo (AI Agent)
**Priority:** Medium
**Description:**
Remove references to redis and supervisord as Docker Compose profiles, as the project only supports two profiles: `cpu` and `gpu-nvidia`. Update documentation to clarify that only these two profiles exist in the LocalAI Stack.

**Subtasks:**
- [x] Analyze current profiles in the project
- [x] Remove redis profile references from docker-compose.yml and service files
- [x] Remove supervisord profile references from docker-compose.yml and service files
- [x] Update .spec/spec.md to clarify only 2 profiles exist
- [x] Verify all changes are consistent

**Dependencies:** None
**Estimated Effort:** 30 minutes
**Related Spec:** `.spec/spec.md` (Section 4)
**Constitutional Compliance:** Yes

---

### [DONE] TASK-002: Clarify portable path principles and clean up .env
**Created:** 2026-04-20
**Assignee:** Roo (AI Agent)
**Priority:** High
**Description:**
Ensure the project is fully portable and adheres to the principle that persistent volumes must reside in a sibling folder (`../.LocalAI`), not inside the project. Remove unused active variables from `.env`, update network name to `LocalAI`, and reinforce clarity in `.spec/` documents.

**Subtasks:**
- [x] Gather context about current .env variables and their usage
- [x] Remove active variables from .env file (USER, PASS, MAIL, POSTGRES_*)
- [x] Update network name in docker-compose.yml to "LocalAI"
- [x] Review .spec files for path clarity
- [x] Update .spec/instructions.md with explicit portable path rules
- [x] Update .spec/spec.md with explicit portable path rules
- [x] Update .spec/tasks.md to reflect this task
- [x] Verify all changes and ensure consistency

**Dependencies:** None
**Estimated Effort:** 1 hour
**Related Spec:** `.spec/spec.md` (Sections 4, 5, 6)
**Constitutional Compliance:** Yes

---

### [DONE] TASK-003: Eliminate docker/ folder and consolidate resources in services/
**Created:** 2026-04-20
**Assignee:** Roo (AI Agent)
**Priority:** Medium
**Description:**
Remove the `docker/` folder and move all Docker-specific resources into their corresponding service directories under `services/`. Update architecture rules in `.spec/` to reflect that all Docker-related resources must reside within service subdirectories.

**Subtasks:**
- [x] Move Dockerfile.supervisord to services/supervisord/
- [x] Move supervisord.conf to services/supervisord/
- [x] Update docker-compose-supervisord.yaml references
- [x] Delete docker/ folder
- [x] Add architecture rules to .spec/ files
- [x] Verify consistency and update tasks.md

**Dependencies:** None
**Estimated Effort:** 30 minutes
**Related Spec:** `.spec/instructions.md` (Section 6)
**Constitutional Compliance:** Yes

---

## Completed Tasks

### [DONE] TASK-001: Align project with updated constitution
**Created:** 2026-04-19
**Assignee:** Roo (AI Agent)
**Priority:** High
**Description:**
Update the project structure, directories, and configurations to comply with the revised constitution (`.spec/instructions.md`). This includes creating missing directories, implementing Spec-Driven Development workflow, updating data persistence paths, and restructuring code into modular components.

**Subtasks:**
- [x] Analyze updated constitution and identify gaps
- [x] Create `.spec/spec.md` technical specification
- [x] Create `.spec/tasks.md` (this file)
- [x] Create missing directories (`/docker/`, `/scripts/`, `/src/`)
- [x] Update Docker volumes to use host paths (`~/.LocalAI/`)
- [x] Implement supervisord for process supervision
- [x] Restructure `n8n_pipe.py` into modular components in `/src/`
- [x] Add missing services from `.env` (redis, jaeger, etc.)
- [x] Update README.md to reflect new architecture

**Dependencies:** None
**Estimated Effort:** 2-3 hours
**Related Spec:** `.spec/spec.md` (Sections 3, 5, 7)
**Constitutional Compliance:** Yes

---

## Task Template (for future use)
```
### [DONE] TASK-005: Fix model storage location and implement COMPOSE_FILE approach
**Created:** 2026-04-20
**Assignee:** Roo
**Priority:** High
**Description:**
Fixed issue where models were downloading inside project folder (`services/.LocalAI/models/ollama`) instead of outside project (`../.LocalAI/models/ollama`). Implemented `COMPOSE_FILE` approach in `.env` to ensure relative paths resolve correctly from project root. Updated `.gitignore` to ignore `services/.LocalAI/` directory.

**Subtasks:**
- [x] Investigate why models were downloading to wrong location
- [x] Update `.env` with `COMPOSE_FILE` variable merging all service files
- [x] Remove `include` section from `docker-compose.yml`
- [x] Update `.gitignore` to ignore `services/.LocalAI/`
- [x] Update documentation in `.spec/spec.md`

**Dependencies:** TASK-004
**Estimated Effort:** 1 hour
**Related Spec:** `.spec/spec.md` (Sections 5, 6)
**Constitutional Compliance:** Yes

### [TODO] TASK-XXX: [Brief title]
**Created:** YYYY-MM-DD
**Assignee:** [Name]
**Priority:** [Low/Medium/High]
**Description:**
[Detailed description of what needs to be done]

**Subtasks:**
- [ ] Subtask 1
- [ ] Subtask 2

**Dependencies:** [Task IDs or external factors]
**Estimated Effort:** [X hours/days]
**Related Spec:** [Section of spec.md]
**Constitutional Compliance:** [Yes/No]
```

---
*This file follows the Spec‑Driven Development (SDD) workflow. Before starting any task, read `.spec/spec.md`. Update this file when a task is started, completed, or blocked.*