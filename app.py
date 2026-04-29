import json
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import datetime as dt
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

    if frequency == "daily":
        default_date = dt.date.today()
    elif frequency == "weekly":
        default_date = dt.date.today() + dt.timedelta(weeks=1)
    else:  # monthly
        default_date = dt.date.today() + dt.timedelta(days=30)

    col5, col6 = st.columns(2)
    with col5:
        task_time = st.time_input("Time", value=dt.time(8, 0), key="task_time_input")
    with col6:
        task_date = st.date_input("Date", value=default_date)

    if st.button("➕ Add Task"):
        new_task = Task(
            task_id=len(st.session_state.tasks) + 1,
            description=task_title,
            duration=int(duration),
            frequency=frequency,
            priority=priority,
            time=task_time.strftime("%H:%M"),
            due_date=dt.datetime.combine(task_date, task_time),
        )
        selected_pet.add_task(new_task)
        st.session_state.tasks.append(
            {
                "task_id": new_task.task_id,
                "pet": selected_pet_name,
                "description": new_task.description,
                "duration": new_task.duration,
                "frequency": new_task.frequency,
                "priority": new_task.priority,
                "time": new_task.time,
                "date": task_date.strftime("%Y-%m-%d"),
                "is_complete": False,
            }
        )
        st.success(f"✅ Task added to {selected_pet_name}!")
    
else:
    st.warning("⚠️ Add at least one pet before adding tasks!")

# Display current tasks with edit and delete controls
if st.session_state.tasks:
    st.write("**Current Tasks:**")
    for i, task_dict in enumerate(st.session_state.tasks):
        if st.session_state.get("editing_task_idx") == i:
            with st.container(border=True):
                ec1, ec2, ec3 = st.columns(3)
                with ec1:
                    e_desc = st.text_input("Description", value=task_dict["description"], key=f"e_desc_{i}")
                    e_freq = st.selectbox("Frequency", ["daily", "weekly", "monthly"],
                                          index=["daily", "weekly", "monthly"].index(task_dict["frequency"]),
                                          key=f"e_freq_{i}")
                with ec2:
                    e_dur = st.number_input("Duration (min)", min_value=1, max_value=240,
                                            value=int(task_dict["duration"]), key=f"e_dur_{i}")
                    e_prio = st.selectbox("Priority", ["low", "medium", "high"],
                                          index=["low", "medium", "high"].index(task_dict["priority"]),
                                          key=f"e_prio_{i}")
                with ec3:
                    e_time = st.text_input("Time (HH:MM)", value=task_dict["time"], key=f"e_time_{i}")
                    try:
                        e_date_default = dt.date.fromisoformat(task_dict["date"])
                    except ValueError:
                        e_date_default = dt.date.today()
                    e_date = st.date_input("Date", value=e_date_default, key=f"e_date_{i}")

                sc, cc = st.columns(2)
                with sc:
                    if st.button("💾 Save", key=f"save_{i}"):
                        st.session_state.tasks[i].update({
                            "description": e_desc,
                            "duration": e_dur,
                            "frequency": e_freq,
                            "priority": e_prio,
                            "time": e_time,
                            "date": e_date.strftime("%Y-%m-%d"),
                        })
                        pet_obj = next((p["pet_obj"] for p in st.session_state.pets if p["name"] == task_dict["pet"]), None)
                        if pet_obj:
                            task_obj = next((t for t in pet_obj.tasks if t.task_id == task_dict["task_id"]), None)
                            if task_obj:
                                task_obj.description = e_desc
                                task_obj.duration = e_dur
                                task_obj.frequency = e_freq
                                task_obj.priority = e_prio
                                task_obj.time = e_time
                                try:
                                    task_obj.due_date = dt.datetime.combine(e_date, dt.datetime.strptime(e_time, "%H:%M").time())
                                except ValueError:
                                    pass
                        st.session_state.editing_task_idx = None
                        st.rerun()
                with cc:
                    if st.button("✖ Cancel", key=f"cancel_{i}"):
                        st.session_state.editing_task_idx = None
                        st.rerun()
        else:
            is_complete = task_dict.get("is_complete", False)
            rc0, rc1, rc2, rc3 = st.columns([1, 6, 1, 1])
            with rc0:
                checked = st.checkbox("", value=is_complete, key=f"chk_{i}", label_visibility="collapsed")
                if checked != is_complete:
                    st.session_state.tasks[i]["is_complete"] = checked
                    pet_obj = next((p["pet_obj"] for p in st.session_state.pets if p["name"] == task_dict["pet"]), None)
                    if pet_obj:
                        task_obj = next((t for t in pet_obj.tasks if t.task_id == task_dict["task_id"]), None)
                        if task_obj:
                            task_obj.mark_complete() if checked else task_obj.mark_incomplete()
                    st.rerun()
            with rc1:
                pet = task_dict["pet"]
                desc = task_dict["description"]
                meta = f"{task_dict['time']} | {task_dict['date']} | {task_dict['duration']} min | {task_dict['frequency']} | {task_dict['priority']}"
                if checked:
                    st.markdown(
                        f'<span style="text-decoration: line-through; color: gray;">🐾 <b>{pet}</b> — {desc} | {meta}</span>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.write(f"🐾 **{pet}** — {desc} | {meta}")
            with rc2:
                if st.button("✏️", key=f"edit_btn_{i}"):
                    st.session_state.editing_task_idx = i
                    st.rerun()
            with rc3:
                if st.button("🗑️", key=f"del_btn_{i}"):
                    pet_obj = next((p["pet_obj"] for p in st.session_state.pets if p["name"] == task_dict["pet"]), None)
                    if pet_obj:
                        task_obj = next((t for t in pet_obj.tasks if t.task_id == task_dict["task_id"]), None)
                        if task_obj:
                            pet_obj.remove_task(task_obj)
                    st.session_state.tasks.pop(i)
                    st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("🧠 AI-assisted task request")
st.caption("Describe a task and Claude will propose scheduling details based on your existing tasks and past decisions.")

if "embedding_manager" not in st.session_state:
    st.session_state.embedding_manager = EmbeddingManager()
if "decision_logger" not in st.session_state:
    st.session_state.decision_logger = DecisionLogger()

if st.session_state.pets:
    ai_pet_names = [p["name"] for p in st.session_state.pets]
    ai_selected_pet_name = st.selectbox("Select pet for this task", ai_pet_names, key="ai_pet_select")
    ai_selected_pet = next(p["pet_obj"] for p in st.session_state.pets if p["name"] == ai_selected_pet_name)
else:
    st.warning("⚠️ Add at least one pet before using AI task requests.")
    ai_selected_pet = None
    ai_selected_pet_name = None

request_text = st.text_input("Describe the task request for AI guidance", value="Schedule grooming for Mochi", key="ai_task_request")

if st.button("🔍 Build grounded proposal", key="build_proposal"):
    if not ai_selected_pet:
        st.warning("Add a pet first.")
    else:
        with st.spinner("Generating task proposal with Claude..."):
            try:
                existing_tasks = st.session_state.scheduler.owner.get_all_tasks()
                fields = st.session_state.embedding_manager.generate_task_proposal(
                    request=request_text,
                    existing_tasks=existing_tasks,
                )
                st.session_state.ai_task_fields = fields
                st.session_state.ai_proposal = json.dumps(fields)
            except Exception as e:
                st.error(f"Failed to generate proposal: {e}")

if st.session_state.get("ai_task_fields"):
    fields = st.session_state.ai_task_fields
    st.markdown("**Proposed task:**")
    st.info(fields.get("rationale", ""))

    col1, col2 = st.columns(2)
    with col1:
        prop_description = st.text_input("Description", value=fields.get("description", request_text), key="prop_desc")
        prop_frequency = st.selectbox(
            "Frequency", ["daily", "weekly", "monthly"],
            index=["daily", "weekly", "monthly"].index(fields.get("frequency", "weekly")),
            key="prop_freq",
        )
        prop_priority = st.selectbox(
            "Priority", ["low", "medium", "high"],
            index=["low", "medium", "high"].index(fields.get("priority", "medium")),
            key="prop_priority",
        )
    with col2:
        prop_time = st.text_input("Time (HH:MM)", value=fields.get("time", "09:00"), key="prop_time")
        try:
            prop_date_default = dt.date.fromisoformat(fields.get("date", str(dt.date.today())))
        except ValueError:
            prop_date_default = dt.date.today()
        prop_date = st.date_input("Date", value=prop_date_default, key="prop_date")
        prop_duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240,
            value=max(1, min(240, int(fields.get("duration", 30)))), key="prop_duration",
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm and save task", key="confirm_task"):
            if ai_selected_pet:
                try:
                    time_obj = dt.datetime.strptime(prop_time.strip(), "%H:%M").time()
                    new_task = Task(
                        task_id=len(st.session_state.tasks) + 1,
                        description=prop_description.strip(),
                        duration=int(prop_duration),
                        frequency=prop_frequency,
                        priority=prop_priority,
                        time=prop_time.strip(),
                        due_date=dt.datetime.combine(prop_date, time_obj),
                    )
                    ai_selected_pet.add_task(new_task)
                    st.session_state.tasks.append({
                        "task_id": new_task.task_id,
                        "pet": ai_selected_pet_name,
                        "description": new_task.description,
                        "duration": new_task.duration,
                        "frequency": new_task.frequency,
                        "priority": new_task.priority,
                        "time": new_task.time,
                        "date": prop_date.strftime("%Y-%m-%d"),
                        "is_complete": False,
                    })
                    st.session_state.decision_logger.log_decision(
                        request=request_text,
                        proposal=st.session_state.ai_proposal,
                        outcome="approved",
                        final_task=prop_description.strip(),
                    )
                    st.session_state.ai_task_fields = None
                    st.success("✅ Task confirmed and added.")
                    st.rerun()
                except ValueError:
                    st.error("Invalid time format. Use HH:MM (e.g. 09:00).")
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
            st.session_state.ai_task_fields = None
            st.warning("Proposal rejected. No task was saved.")

st.divider()

# st.subheader("🧠 AI Task Proposal")
# st.caption("Use past decision examples to ground a proposed task before confirming it.")

# if "embedding_manager" not in st.session_state:
#     st.session_state.embedding_manager = EmbeddingManager()

# request_text = st.text_input("Describe the task you want help with", value="Schedule vet appointment for Mochi")

# if st.button("Generate AI prompt"):
#     if request_text.strip():
#         augmented_prompt = st.session_state.embedding_manager.build_prompt(request_text)
#         st.markdown("**Prompt with retrieved context:**")
#         st.code(augmented_prompt, language="text")
#     else:
#         st.warning("⚠️ Enter a task request first.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = st.session_state.scheduler
    sorted_tasks = scheduler.sort_by_time()

    # Build set of (date, time) slots that have more than one task
    schedule_map = {}
    for pet in scheduler.owner.pets:
        for task in pet.tasks:
            key = (task.due_date.date(), task.time)
            schedule_map.setdefault(key, []).append(task)
    conflicted_slots = {key for key, slot_tasks in schedule_map.items() if len(slot_tasks) > 1}

    st.subheader("Daily Schedule")
    if sorted_tasks:
        for task in sorted_tasks:
            key = (task.due_date.date(), task.time)
            status = "✅" if task.is_complete else "⬜"
            detail = f"{task.duration} min, {task.frequency}, {task.priority} priority"
            if key in conflicted_slots:
                style = "text-decoration: line-through; color: gray;" if task.is_complete else ""
                st.markdown(
                    f'<div style="background-color: rgba(255,186,0,0.2); padding: 0.5rem 1rem;'
                    f' border-radius: 0.25rem; margin: 0.2rem 0;">'
                    f'{status} <span style="{style}"><b>{task.time}</b>: {task.description}'
                    f' ({detail})</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            elif task.is_complete:
                st.markdown(
                    f'{status} <span style="text-decoration: line-through; color: gray;">'
                    f'**{task.time}**: {task.description} ({detail})</span>',
                    unsafe_allow_html=True,
                )
            else:
                st.write(f"{status} **{task.time}**: {task.description} ({task.duration} min, {task.frequency}, **{task.priority} priority**)")
    else:
        st.info("No tasks to schedule.")

    conflicts = scheduler.detect_scheduling_conflicts()
    if conflicts:
        st.warning("⚠️ Scheduling Conflicts Detected:")
        for conflict in conflicts:
            st.markdown(conflict)
    else:
        st.success("✅ No scheduling conflicts detected.")
