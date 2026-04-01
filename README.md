# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.


## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


## Summary
Application allows owner to put their information and allows them to add multiple pets and their information, such as their name, and type of animal. The user can then create tasks and include details such as time duration, priority, and repeat frequency. The tasks can also be assigned to a specific pet. The tasks can then be put in a list and organized in different ways, such as priority, time, time it was added, etc. The owner can then declare when a task is finished. There is also a feature that can warn the owner of task scheduling conflicts.

## "Testing PawPal+".

Summary of my tests: ...
This has my confidence based on the systems results. It collected 28 items and all 28 had passed in 0.1s.

# UML diagrams:
<a href="" target="_blank"><img src='' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

# Demo Screenshots
<a href="" target="_blank"><img src='' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

<a href="" target="_blank"><img src='' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.

<a href="" target="_blank"><img src='' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>.