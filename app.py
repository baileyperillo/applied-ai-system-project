import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler, DecisionLogger, EmbeddingManager

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("🐾 Manage Pets")

# Initialize pets list in session state
if "pets" not in st.session_state:
    st.session_state.pets = []

# Pet creation section
col1, col2, col3 = st.columns(3)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"], key="species_input")
with col3:
    if st.button("➕ Add Pet"):
        # Check if pet already exists
        if not any(p['name'] == new_pet_name for p in st.session_state.pets):
            new_pet = Pet(pet_id=len(st.session_state.pets) + 1, name=new_pet_name, animal_type=new_pet_species)
            st.session_state.pets.append({"pet_obj": new_pet, "name": new_pet_name, "species": new_pet_species})
            st.success(f"✅ Added {new_pet_name} the {new_pet_species}!")
        else:
            st.warning(f"⚠️ {new_pet_name} already exists!")

# Display all pets
if st.session_state.pets:
    st.write("**Your Pets:**")
    for i, pet_info in enumerate(st.session_state.pets):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"🐾 **{pet_info['name']}** ({pet_info['species']})")
        with col2:
            st.caption(f"{len(pet_info['pet_obj'].tasks)} tasks")
        with col3:
            if st.button("🗑️", key=f"delete_pet_{i}"):
                st.session_state.pets.pop(i)
                st.rerun()
else:
    st.info("No pets yet. Add one above!")

# Update owner with current pets
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id=1, name="", email="")

st.session_state.owner.name = st.text_input("Owner name", value="Jordan", key="owner_name")
st.session_state.owner.pets = [pet_info["pet_obj"] for pet_info in st.session_state.pets]

# Initialize scheduler
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)
else:
    st.session_state.scheduler.owner = st.session_state.owner

st.divider()

st.subheader("📋 Add Tasks")
st.caption("Select a pet and add care tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Task input section
if st.session_state.pets:
    # Select which pet to add task to
    pet_names = [p["name"] for p in st.session_state.pets]
    selected_pet_name = st.selectbox("Select pet for this task", pet_names)
    selected_pet = next(p["pet_obj"] for p in st.session_state.pets if p["name"] == selected_pet_name)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly"])
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)

    if st.button("➕ Add Task"):
        new_task = Task(
            task_id=len(st.session_state.tasks) + 1,
            description=task_title,
            duration=int(duration),
            frequency=frequency,
            priority=priority,
        )
        selected_pet.add_task(new_task)
        st.session_state.tasks.append(
            {"pet": selected_pet_name, "description": new_task.description, "duration": new_task.duration, "frequency": new_task.frequency, "priority": new_task.priority}
        )
        st.success(f"✅ Task added to {selected_pet_name}!")
    
    if st.session_state.tasks:
        st.write("**Current Tasks:**")
        st.table(st.session_state.tasks)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.warning("⚠️ Add at least one pet before adding tasks!")

st.divider()

st.subheader("🧠 AI-assisted task request")
st.caption("Retrieve similar past decisions, build a grounded proposal, and confirm before saving any task.")

if "embedding_manager" not in st.session_state:
    st.session_state.embedding_manager = EmbeddingManager()
if "decision_logger" not in st.session_state:
    st.session_state.decision_logger = DecisionLogger()

request_text = st.text_input("Describe the task request for AI guidance", value="Schedule grooming for Mochi", key="ai_task_request")

if st.button("🔍 Build grounded proposal", key="build_proposal"):
    st.session_state.ai_prompt = st.session_state.embedding_manager.build_prompt(request_text)
    st.session_state.ai_proposal = f"Grounded task proposal for: {request_text}"
    st.session_state.ai_final_task = request_text

if "ai_prompt" in st.session_state and st.session_state.ai_prompt:
    st.markdown("**Retrieved few-shot examples and grounded prompt:**")
    st.code(st.session_state.ai_prompt, language="text")
    st.markdown("**Proposed task summary:**")
    st.write(st.session_state.ai_proposal)

    edited_final_task = st.text_area(
        "Edit the final task description before saving",
        value=st.session_state.get("ai_final_task", request_text),
        key="ai_final_task_text"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm and save task", key="confirm_task"):
            if not edited_final_task.strip():
                st.warning("Enter a final task description before confirming.")
            else:
                if st.session_state.pets:
                    selected_pet = st.session_state.pets[0]["pet_obj"]
                    new_task = Task(
                        task_id=len(st.session_state.tasks) + 1,
                        description=edited_final_task.strip(),
                        duration=30,
                        frequency="weekly",
                        priority="medium",
                    )
                    selected_pet.add_task(new_task)
                    st.session_state.tasks.append(
                        {
                            "pet": selected_pet.name,
                            "description": new_task.description,
                            "duration": new_task.duration,
                            "frequency": new_task.frequency,
                            "priority": new_task.priority,
                        }
                    )
                    st.session_state.decision_logger.log_decision(
                        request=request_text,
                        proposal=st.session_state.ai_proposal,
                        outcome="approved",
                        final_task=edited_final_task.strip(),
                    )
                    st.success("✅ Task confirmed and added after review.")
                else:
                    st.warning("Add a pet first before confirming a task.")
    with col2:
        if st.button("❌ Reject proposal", key="reject_task"):
            st.session_state.decision_logger.log_decision(
                request=request_text,
                proposal=st.session_state.ai_proposal,
                outcome="rejected",
                final_task="",
            )
            st.warning("Proposal rejected. No task was saved.")

st.divider()

st.subheader("🧠 AI Task Proposal")
st.caption("Use past decision examples to ground a proposed task before confirming it.")

if "embedding_manager" not in st.session_state:
    st.session_state.embedding_manager = EmbeddingManager()

request_text = st.text_input("Describe the task you want help with", value="Schedule vet appointment for Mochi")

if st.button("Generate AI prompt"):
    if request_text.strip():
        augmented_prompt = st.session_state.embedding_manager.build_prompt(request_text)
        st.markdown("**Prompt with retrieved context:**")
        st.code(augmented_prompt, language="text")
    else:
        st.warning("⚠️ Enter a task request first.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = st.session_state.scheduler
    
    # Sort tasks by scheduled time for display
    sorted_tasks = scheduler.sort_by_time()
    
    st.subheader("Daily Schedule")
    if sorted_tasks:
        for task in sorted_tasks:
            st.write(f"**{task.time}**: {task.description} ({task.duration} min, {task.frequency}, **{task.priority} priority**)")
    else:
        st.info("No tasks to schedule.")
    
    # Check for scheduling conflicts
    conflicts = scheduler.detect_scheduling_conflicts()
    if conflicts:
        st.warning("⚠️ Scheduling Conflicts Detected:")
        for conflict in conflicts:
            st.markdown(conflict)
    else:
        st.success("✅ No scheduling conflicts detected.")
