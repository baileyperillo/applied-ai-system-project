# PawPal+ Project Reflection

## 1. System Design

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


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

There were some design changes in the implementation. The way the relationships were managed was a probem. For example, if pet information was edited or deleted, the pet information according to the owner info would not be updated on the change. This is very important if the owner is supposed to be able to edit their info while keeping the PetInfo separated.

There was also no sorting method for the list of tasks. So the tasks were not really being sorted by priority in the lists. This is an important feature for the project if we need to add priority.

There was also a validation concern according the the AI, where everything inputted needed to be validated, along with making sure that it is correct. This might become an issue if this was not just used by the owner or you are relating a task with a pet and an owner.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?


Time, date, duration, and priority are greatly considered when making tasks for the schedule and finding conflicts. Time and priority was the constraint that mattered the most due to scheduling a task in the next available time, and organizing the list based on priority. Frequency and completion status were also considered but to a much less degree.

- The scheduler doesn't allow for allow intentional same-time tasks. An example could be making a task to walk two dogs at the same time.
- Tasks don't take into account other factors when suggested (time traveling, overtime, etc.) 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

## Tradeoffs:
- Because the feature is RAG instead of agentic workflow, the program would not self-check itself or correct when user rejects generated tasks
- AI only looks at the last 3 tasks from user history similar to the input. This is dependent on how long the history is.
- relies on Claude API for generated tasks, expecially time and date
- schedule only displays
- memory won't be saved if refresh app
- Long history can slow down decision making (except for decisions.csv, decisions_embeddings.npy)
- Dual object representation: Task is stored in two different ways, possibly causing problems in the future.

For the first tradeoff, I wanted eventually change this feature from RAG to agentic workflow so it can correct it's answer before giving an answer to the user and adjusting it's answer based on the user's choices previous tasks. Right now, the scheduler only finds best availabile space that is similar to the last 3 similar previous tasks from the user's history.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI for brainstorming, such as understanding what each required feature does and ideas on how it can it be implemented. I used AI to design a diagram. I used AI to create steps to implement, then implement those steps. I used AI solve debugging issues or changes I wanted to create.
I asked prompts asking for definitions and how things could be implemented, such as what is RAG, how does it work, how can it be implemented in my project (give me 3 ideas), how this idea differnt from agentic workflow. I gave it prompts when debugging like "what are the differnce between these two functions or features? How does this work? Do I need to use an API for this?". I then used it to help me debug by giving descriptions about what I want "I want the comment out this function since it's used for debugging but is redundent in the application. I don't want to see the prompts in the function but print them in the console. Add an error handling this can't be prompted". 


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Use human evaluation to test features and try to break app.Features were implemented but when challenged, Multiple problems arose. This included redundent features and features not working when conflicting. Automated tests (unit tests) were done in #tests/test_pawpal.py, testing (add_task(), mark_complete()), recurrence tests when looking at user's data, filtering when organizing by different catagories, and conflict detection with scheduling conflicts. Logging and Error Handling was done if missing information when adding taskss, or giving warnings for scheduling conflicts.

## Problems that I came across
- generated task isn't specific - no time or date
- generated task won't show in task list once confirmed
- nothing happens after generated task is rejected; should propose again
- start time is not input by user so there will always be scheduling conflicts
- if I add another task in the AI Task proposal, it would not show in the to edit text box
- rejected first generated response then tried again. Gave same response
- generating new task after not rejecting or confirming old task will keep old task

**See checklist at bottom of [text](README.md)**

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am satisfied the overall application so far. I think it is at a place that I am happy to submit even though I have a bunch of ideas for the future. It works well and I think that the features were thought through. I am most satisfied with the list making and the AI generated task request. It's working how I intended it to be.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

## Future Plans
- make feature agentic workflow so it can check itself and fix itself in a loop
- when generated response is rejected, AI will generate a new response (agentic)
- show a monthly calender of all the tasks already scheduled
- visually appealing list
- visual calender
- make owner info important? (depends on if this is used for personal or business)
- be able to prompt for editing tasks
- edit tasks on schedule. If completed, can press complete to remove from schedule and mark as complete on current tasks
- find a way to schedule certain tasks without scheduling conflicts (ex: I want to schedule walks for my two dogs at the same time)
- warn user of scheduling conflict beforehand?
- make the shedule more interactive (currently just displaying)

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned how important it is to test your app and how long it could take to fix or change a feature in an app, especially done by AI, but also how fast it is compared to if I do it. I learned how important it is to know what you are designing or how you want your app to look or have when working with AI.








