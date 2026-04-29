# PawPal+ Project Reflection

## 1. System Design

Original Design:
There should be a class named Ticket. It should have attributes:
string owner
string pet name
string dogDescription?
string task_title
string taskDescription?
int time = how long it takes to do task/ time owner should take to complete
OR
int timeHours = how many hours
int timeMinutes = how many minutes it

int priority = 1,2,3 OR string priority = high, med, low

Methods:
enter owner info = enter owner info (owner + pet + petDescription?)
edit owner info = selected info can change the existing info and save
enter task = enter task (task title, taskDescription?, timeDuration, priority)
edit task = edit info in selected task and save
task organizer = organizes the task based on priority or based on time entered
completed = task is erased from list when selected as completed

After modifications, Prompt:
I am designing a pet care app with the four classes: ownerInfo, Task, List, and another class I don't know, maybe petInfo. 
ownerInfo is how the owner can enter their information along with their pet and number of pets. The user could also edit their info.

petInfo is the info the user puts for their pet. It should include pet name, type of animal. The usesr should be able to add multiple pets and edit this information.

Task should is the task the owner can make, such as walk the dog. Each task should have time duration it would take to complete task and priority.

List should show the list of tasks. Can add the which pet the task is for if they want. The List should be organized by priority or when they were inputted.

Use Mermaid Live Demo to create a Mermaid.js UML class diagram


UML Diagram (created by Claude)
classDiagram
    class OwnerInfo {
        +String ownerName
        +String email
        +String phone
        +int numberOfPets
        +enterInfo()
        +editInfo()
        +addPet()
        +removePet()
    }

    class PetInfo {
        +int petId
        +String petName
        +String animalType
        +String breed
        +int age
        +enterPetInfo()
        +editPetInfo()
    }

    class Task {
        +int taskId
        +String taskName
        +String description
        +int duration
        +String priority
        +Date dateAdded
        +createTask()
        +editTask()
        +deleteTask()
    }

    class TaskList {
        +List~Task~ tasks
        +addTask()
        +removeTask()
        +sortByPriority()
        +sortByDateAdded()
        +displayList()
    }

    OwnerInfo "1" --> "0..*" PetInfo : owns
    OwnerInfo "1" --> "1" TaskList : has
    TaskList "1" --> "0..*" Task : contains
    Task "0..1" --> "0..1" PetInfo : assigned to



# Copilot UML Diagram
UML Diagram (created by CoPilot) - used
**CoPilot asked for more clarification
OwnerInfo:
    - name
    - numberOfPets
    -     classDiagram
        class OwnerInfo {
            -int ownerID
            -string name
            -string email
            -string phone
            -int numberOfPets
            +addOwnerInfo()
            +editOwnerInfo()
        }
        
        class PetInfo {
            -int petID
            -string petName
            -string animalType
            -string breed [optional]
            -int age [optional]
            +addPet()
            +editPet()
        }
        
        class Task {
            -int taskID
            -string taskName
            -int duration
            -int priority
            -datetime createdAt
            -PetInfo assignedPet [optional]
            +createTask()
            +editTask()
            +deleteTask()
        }
        
        class List {
            -int listID
            -string listName
            -string sortBy
            +addTask()
            +removeTask()
            +getTasks()
            +updateSortOrder()
        }
        
        OwnerInfo "1" --> "many" PetInfo : owns
        OwnerInfo "1" --> "many" Task : creates
        OwnerInfo "1" --> "many" List : manages
        Task "many" --> "many" PetInfo : assigns to
        List "1" --> "many" Task : contains


**a. Initial design**

Three things user should be able to do:
1. user should enter info on themselves and their pet
2. user can enter their task, time duration, and priority and see it displayed
3. user can edit task with the time duration to do task and priority


- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

The UML diagram has 4 classes. OwnerInfo, PetInfo, Task, List. Owner can own many Pets and make many Lists and Tasks. All Pets have one Owner and can have a List assigned to them. A Task is created by the Owner and can be assigned a time duration, priority, and Pet as a list if it is specific to it. A List is made up of Tasks and a list of Tasks can be assigned to a specific Pet.
OwnerInfo is how the user enters their information along with their pets. they can edit their info. PetInfo is the information the owner enters about their pet. It can be edited. The Task is what the owner wants to complete. It should have the priority, the time duration it would take to complete it, and optionally the pet it may be assigned to. It can be edited. The List should organize the group of tasks, whether it is assigned to specific pets or not, depending on priority or order of input.

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

Some constraints that the scheduler considers is the start time, duration or how long the task takes, the date it's due, and scheduling conflicts such as if two tasks share the same start time and due date. The scheduler also has priority and frequency it repeats, and status, completed or not.
I followed the description of the application to know some of the things I needed to add constraints. Time mattered and priority mattered the most because of how many times those things are considered when making or deciding on tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

A tradeoff was detecting scheduling conflicts by the exact time rather than time overlap, such as if a tasks take 1 hour and one starts 30 mins after another one. This is a reasonable tradeoff because it is can be checked easily with the attributes we have compared to time overlap where you have count the more exact timing it conflicts. It's something some owners don't really think about.


---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
