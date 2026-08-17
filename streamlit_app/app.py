import streamlit as st
import sys
import tempfile
import zipfile
import shutil
from pathlib import Path

# ==========================================================
# Project Imports
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

import config
from process_script import process_script

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Storyboard Generation Pipeline",
    page_icon="🎬",
    layout="wide"
)

# ==========================================================
# Initialize Session State
# ==========================================================

if "generated" not in st.session_state:
    st.session_state.generated = False
if "completed" not in st.session_state:
    st.session_state.completed = []
if "failed" not in st.session_state:
    st.session_state.failed = []
if "zip_data" not in st.session_state:
    st.session_state.zip_data = None

# ==========================================================
# Header
# ==========================================================

st.title("🎬 Storyboard Generation Pipeline")

st.markdown(
    """
Generate standardized educational storyboards using the
Lernkys AI Storyboard Pipeline.
"""
)

st.divider()

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.header("⚙️ Generation Settings")

talking_head_percentage = st.sidebar.slider(
    "Talking Head %",
    min_value=0,
    max_value=100,
    value=config.TALKING_HEAD_PERCENTAGE,
    step=5
)

animation_complexity = st.sidebar.selectbox(
    "Animation Complexity",
    ["Low", "Medium", "High"],
    index=["Low", "Medium", "High"].index(
        config.ANIMATION_COMPLEXITY
    )
)

target_audience = st.sidebar.text_input(
    "Target Audience",
    value=config.CREATIVE_BRIEF["target_audience"]
)

visual_style = st.sidebar.text_input(
    "Visual Style",
    value=config.CREATIVE_BRIEF["visual_style"]
)

# ==========================================================
# Main Inputs
# ==========================================================

st.subheader("📝 Previous Context")

previous_context = st.text_area(
    "Previous Context",
    value=config.CREATIVE_BRIEF["previous_context"],
    height=120,
    label_visibility="collapsed"
)

st.subheader("📋 Storyboard Requirements")

storyboard_requirements = st.text_area(
    "Storyboard Requirements",
    value=config.CREATIVE_BRIEF["storyboard_requirements"],
    height=220,
    label_visibility="collapsed"
)

st.divider()

# ==========================================================
# Upload Scripts
# ==========================================================

st.subheader("📂 Upload Scripts")

uploaded_files = st.file_uploader(
    "Upload one or more DOCX files",
    type=["docx"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(
        f"{len(uploaded_files)} script(s) uploaded."
    )

    cols = st.columns(2)

    for index, file in enumerate(uploaded_files):
        with cols[index % 2]:
            st.info(f"📄 {file.name}")

st.divider()

generate = st.button(
    "🚀 Generate Storyboards",
    use_container_width=True
)

# ==========================================================
# Execute Pipeline
# ==========================================================

if generate:

    # ------------------------------------------------------
    # Validate Upload
    # ------------------------------------------------------

    if not uploaded_files:
        st.error("Please upload at least one script.")
        st.stop()

    # Reset session state before running a new generation
    st.session_state.generated = False
    st.session_state.completed = []
    st.session_state.failed = []
    st.session_state.zip_data = None

    # ------------------------------------------------------
    # Update Runtime Config
    # ------------------------------------------------------

    config.TALKING_HEAD_PERCENTAGE = talking_head_percentage
    config.ANIMATION_COMPLEXITY = animation_complexity
    config.CREATIVE_BRIEF["previous_context"] = previous_context
    config.CREATIVE_BRIEF["storyboard_requirements"] = storyboard_requirements
    config.CREATIVE_BRIEF["target_audience"] = target_audience
    config.CREATIVE_BRIEF["visual_style"] = visual_style

    # ------------------------------------------------------
    # Temporary Workspace
    # ------------------------------------------------------

    temp_workspace = Path(tempfile.mkdtemp())
    scripts_folder = temp_workspace / "scripts"
    output_folder = temp_workspace / "output"

    scripts_folder.mkdir(parents=True, exist_ok=True)
    output_folder.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------
    # Save Uploaded Files
    # ------------------------------------------------------

    saved_scripts = []

    for uploaded_file in uploaded_files:
        file_path = scripts_folder / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_scripts.append(file_path)

    st.divider()

    st.subheader("🚀 Storyboard Generation Progress")

    overall_progress = st.progress(0)
    current_module = st.empty()
    spinner_placeholder = st.empty()

    completed = []
    failed = []
    total = len(saved_scripts)

    # ------------------------------------------------------
    # Process Every Script
    # ------------------------------------------------------

    for index, script_path in enumerate(saved_scripts):
        module_name = script_path.stem

        # UI Progress Update - Completed, Current, and Remaining modules
        remaining_modules = [p.stem for p in saved_scripts[index + 1:]]

        status_text = f"### 🔄 Processing Module **{index + 1}** of **{total}**\n\n"
        status_text += f"**Current Module:** `{module_name}`\n\n"

        if completed:
            status_text += "**Completed:**\n" + "\n".join([f"✅ `{m}`" for m in completed]) + "\n\n"
        if failed:
            status_text += "**Failed:**\n" + "\n".join([f"❌ `{f['module']}` - {f['error']}" for f in failed]) + "\n\n"
        if remaining_modules:
            status_text += "**Remaining:**\n" + "\n".join([f"⏳ `{m}`" for m in remaining_modules]) + "\n\n"

        current_module.markdown(status_text)

        with spinner_placeholder:
            with st.spinner(f"Generating storyboard for {module_name}..."):
                try:
                    module_output = output_folder / module_name
                    process_script(
                        script_path,
                        module_output
                    )
                    completed.append(module_name)
                except Exception as e:
                    failed.append(
                        {
                            "module": module_name,
                            "error": str(e)
                        }
                    )

        overall_progress.progress((index + 1) / total)

    # ------------------------------------------------------
    # Clean Up Progress Display when Done
    # ------------------------------------------------------
    status_text = f"### ✅ Pipeline Execution Completed\n\n"
    if completed:
        status_text += "**Completed:**\n" + "\n".join([f"✅ `{m}`" for m in completed]) + "\n\n"
    if failed:
        status_text += "**Failed:**\n" + "\n".join([f"❌ `{f['module']}` - {f['error']}" for f in failed]) + "\n\n"
    current_module.markdown(status_text)
    spinner_placeholder.empty()

    # ======================================================
    # Create ZIP of Generated Storyboards
    # ======================================================

    zip_path = temp_workspace / "Storyboards.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for module in completed:
            module_dir = output_folder / module
            storyboard_docx = module_dir / "generated_storyboard.docx"
            if storyboard_docx.exists():
                zipf.write(
                    storyboard_docx,
                    arcname=f"{module}.docx"
                )

    # ------------------------------------------------------
    # Read ZIP into Memory and Clean Up Disk Workspace
    # ------------------------------------------------------
    zip_data = None
    if zip_path.exists():
        with open(zip_path, "rb") as f:
            zip_data = f.read()

    try:
        shutil.rmtree(temp_workspace)
    except Exception as e:
        print(f"Error cleaning up temp workspace: {e}")

    # Store results in Session State for persistence across reruns
    st.session_state.completed = completed
    st.session_state.failed = failed
    st.session_state.zip_data = zip_data
    st.session_state.generated = True

    # Play UI effects
    if completed:
        st.toast("🎉 Storyboards generated successfully!")
        st.balloons()
    elif failed:
        st.toast("⚠️ Generation failed for all modules.")

# ==========================================================
# Display Summary and Download Button from Session State
# ==========================================================

if st.session_state.generated:
    st.divider()

    st.subheader("📊 Execution Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Successful Modules",
            len(st.session_state.completed)
        )

    with col2:
        st.metric(
            "Failed Modules",
            len(st.session_state.failed)
        )

    if st.session_state.completed:
        st.success("Generated Storyboards")
        for module in st.session_state.completed:
            st.write(f"✅ {module}")

    if st.session_state.failed:
        st.error("Failed Modules")
        for item in st.session_state.failed:
            st.write(f"❌ {item['module']}")
            st.caption(f"Reason: {item['error']}")

    if st.session_state.zip_data:
        st.divider()
        st.subheader("📦 Download Storyboards")

        st.download_button(
            label="⬇ Download Storyboards.zip",
            data=st.session_state.zip_data,
            file_name="Storyboards.zip",
            mime="application/zip",
            use_container_width=True
        )