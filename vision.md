This diagram illustrates an automated, AI-driven **Code Migration** workflow. It utilizes **crewAI** to orchestrate various "Harnesses" (agentic workflows) that handle everything from planning to validation.

The process follows a loop: **Analyze $\rightarrow$ Plan $\rightarrow$ Implement $\rightarrow$ Validate.**

---

### 1. The AI Harnesses (The Engine)
Each "Harness" represents a specialized stage in the migration pipeline, powered by **crewAI** agents and specific technical tools.

*   **Project Tracking HARNESS:** The starting point. It analyzes the migration needs to **Plan** and **Generate** a User Story Backlog. It acts as the "manager" that feeds tasks into the loop.
*   **Test HARNESS:** Focuses on creating a safety net. It uses `openCode` and `OpenSpec` to generate **Characterization Tests** (to capture current behavior) and **Functional Tests** to ensure code coverage.
*   **Code HARNESS:** The implementation phase. It uses `openrewrite` and `openCode` to perform **Spec-Driven Refactors**, automatically transforming the code based on the generated specifications.
*   **Evaluation HARNESS:** Uses `DeepEval` to generate **Evaluation Metrics** and test scores. This stage determines if the AI's refactoring meets the required quality and logic standards.
*   **Benchmark HARNESS:** A generic builder that compiles the successful code and tests into a formal **Benchmark / Test Suite**.
*   **CI HARNESS:** The final automation step before human review. It **prepares the Merge Request (MR)** to be sent to the CI platform.

---

### 2. CI Platform & Kanban Boards (The Environment)
This section represents the traditional DevOps infrastructure where the AI's work is verified.

*   **CI PLATFORM (GitLab):** Runs the **CI Pipeline**. It acts as a gatekeeper with a logic check:
    *   **No (Pass):** If tests pass and no human is needed, the Merge Request is **Closed/Merged**.
    *   **Yes (Fail/Review):** If tests fail or human intervention is flagged, **OpenLIT** generates KPI metrics to analyze the failure.
*   **KANBAN BOARDS:** Visually tracks the status of user stories. Both the CI platform and the Human operator interact here to move tasks between "Backlog," "In Progress," and "Done."

---

### 3. The Human Factor (The Supervisor)
The red icon at the top right represents the human developer or architect. Their role is to:
1.  **Update documentation:** Refine `rule.md` or `tasks.md` to guide the AI.
2.  **Request Root Cause Analysis:** If the AI fails, the human can ask for a deeper look.
3.  **Manage the Backlog:** Manually return failed or complex issues to the backlog for another iteration.

---

### Summary of Relationships
The workflow is a **recursive loop**. The **Project Tracking HARNESS** initiates a loop for every user story. The data flows linearly through testing, coding, and evaluation until it reaches the **CI Platform**. 

If the CI pipeline detects an issue, the feedback loop (represented by the dotted lines) sends the task back to the **Kanban Boards** or the **Project Tracking HARNESS** to be refined and re-processed by the AI.
