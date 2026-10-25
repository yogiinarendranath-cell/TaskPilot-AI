# TaskPilot AI - Autonomous Task Execution & Verification Agent

TaskPilot AI is a framework that receives a task, breaks it into verifiable steps, executes those steps using allowlisted tools within a sandboxed workspace, and independently verifies the results before reporting success.

This repository contains both the core **TaskPilot AI framework** and the specific **HackerRank Orchestrate Hackathon (October 2026)** submission for the "Ghost Data Still Exists" challenge.

---

## 1. HackerRank Orchestrate Hackathon (October 2026)

**Problem:** "Ghost Data Still Exists" - Build an AI-powered deletion audit agent to prove whether a user's personal data is truly gone across primary databases, secondary logs, search indexes, and backup syncs.

**Solution (`audit.py`):**
To guarantee schema compliance and avoid LLM-generated audit decisions in the final submission, the solution utilizes a deterministic rules engine. The agent:
1. Maps current email addresses to current and historical `user_id`s.
2. Reconstructs the timeline by scanning `system_activity.csv` for post-deletion recreation events (`SYNC_EXPORT`, `BACKUP_RESTORE`, `SEARCH_INDEXING`).
3. Determines the `deletion_status` (`COMPLETE`, `INCOMPLETE`, `NOT_APPLICABLE`).
4. Outputs strict JSON remediation steps required to fix the deletion pipeline.

**Hackathon Status:** Submission received. AI Judge interview completed. Evaluation underway (Results expected Oct 27, 2026).

---

## 2. TaskPilot AI Core Framework

The core `src/taskpilot` framework is a deterministic agent that executes JSON task definitions, verifies the results, and outputs a verification report.

### Workflow 1: HackerRank Audit (`audit.py`)
To run the specific hackathon submission that processes the 518 deletion requests:
```bash
python audit.py
