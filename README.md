# Applied AI System
# Title: PawPal++
## Original Project: PawPal+ (Module 2 Project)


## Summary

PawPal+ just got an update. Introducting **PawPal++**, where along with being able to schedule pet care tasks, you can also ask the built in AI to do it for you. The AI uses RAG to look through your previous history of tasks to find you the perfect time to do a task, like scheduling vet appointments or giving your pet their medication. If you want to spend less time looking at your calender, this is the tool you need


## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan


## Original Project Summary
Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## New Project Summary
The final app after updates should:

 - User can enter a task they want on their schedule
 - Execution gardrail: make AI ask for confirmation before implementing task

 This is important and really good feature because a lot of people wouldn't want to make the time to schedule small tasks or they forget to make and schedule tasks at the moment. If they have a way to automate the task, especially if the task repeats, like medication or such, it would be great to do that!

 Application allows user to create add their pet name and species, and then create tasks, edit, and remove tasks for each pet. Application also allows user to make a request to create a task. Application will look through data of past tasks to find and suggest the best available date for task. The user will then confirm or decline the suggested date and time of task. If confirmed, the task will officially be added. If declined the application will try again.


 ## Architecture Overview
 ![alt text](<Pet Owner Task Management-2026-04-27-065215.png>)
 PawPal+ System Architecture Summary

The system is organized around a two-pipeline design that separates scheduling from AI-assisted task proposals.

Built (current)
The owner enters pet info, tasks, and constraints through a Streamlit UI. A backend data model (Owner → Pet → Task) feeds a Scheduler that sorts, filters, handles recurrences, and detects conflicts — outputting a clean daily plan back to the owner. An automated test suite (28 tests) validates the scheduler independently.

Next (RAG pipeline)
When the owner submits a new task request, a Retriever searches a Decision Log corpus of past approved, edited, and rejected decisions using vector similarity. The top matches are injected as few-shot examples into a prompt sent to Claude (the Agent), which generates a grounded proposal with a rationale. That proposal is surfaced to the owner as an Evaluator step — they confirm, edit, or reject it before anything touches the data model. Every decision is logged back to the corpus, so retrieval improves over time.

Mermaid Diagram (using Claude)

 Plan:
 implement RAG feature, agentic workflow later

 graph TD
    OWNER(["Pet Owner"])

    subgraph BUILT["✅ BUILT"]
        MODEL["Data Model\nOwner · Pet · Task"]
        SCHEDULER["Scheduler\nsort · filter · conflicts · recurrence"]
    end

    subgraph RAG_PIPE["🔜 NEXT — RAG Pipeline"]
        RETRIEVER["Retriever\nvector similarity search"]
        CORPUS[("Decision Log\napproved · edited · rejected")]
        AGENT["Agent\nClaude LLM\nproposal + rationale"]
    end

    PLAN_OUT["Daily Schedule\nw/ rationale"]

    subgraph HUMAN_REVIEW["Human-in-the-Loop"]
        EVALUATOR["Evaluator\nOwner: Confirm · Edit · Reject"]
    end

    subgraph AUTO_TESTING["Automated Testing"]
        TESTER["Tester\n28 passing tests"]
    end

    FUTURE(["Agentic Workflow 🔮\nplanned later"])

    OWNER -->|"pets · tasks · constraints"| MODEL
    OWNER -->|"new task request"| RETRIEVER

    MODEL --> SCHEDULER
    SCHEDULER -->|"sorted, conflict-free plan"| PLAN_OUT
    PLAN_OUT --> OWNER

    RETRIEVER <-->|"semantic search"| CORPUS
    RETRIEVER -->|"request + few-shot examples"| AGENT
    AGENT -->|"grounded proposal"| EVALUATOR

    EVALUATOR -->|"log decision"| CORPUS
    EVALUATOR -->|"confirmed task"| MODEL

    TESTER -.->|"validates"| SCHEDULER

    RAG_PIPE -.->|"foundation for"| FUTURE


## Getting started

### Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 -m pip install scikit-learn
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Think and decide on a feature that fits into one of the requirements (RAG, Agentic Workflow, Fine-Tuned or Specialized Model, Reliability or Testing System)
3. Create/ Draft the Architecture with a System Diagram (including the current features of the project and the planned)
4. Create a README.md to log the plan and current features (original project, new project summary, architecture system design, Setup Instructions, etc. )
4. Implement RAG logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Tradeoffs:
Because the feature is RAG instead of agentic workflow, the program would not self-check itself


## "Testing PawPal++".

Summary of my tests: ...


