# app.py

import streamlit as st
from dotenv import load_dotenv

from src.models import ExperienceLevel, WorkInstructionInput
from src.pipeline import WorkInstructionPipeline


load_dotenv()

import os

print("API KEY:", os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="AI Documentation Assistant",
    page_icon="🛠️",
    layout="wide",
)

st.title("AI Documentation Assistant")
st.write(
    "Convert unstructured technical notes into a structured work instruction draft."
)

with st.sidebar:
    st.header("Settings")
    mock_mode = st.toggle("Use mock mode", value=True)
    save_outputs = st.toggle("Save outputs locally", value=False)

EXAMPLES = {
    "Sensor replacement": {
        "document_title": "Sensor replacement on conveyor system",
        "equipment_or_system": "Conveyor system",
        "target_user": "Maintenance technician",
        "experience_level": "intermediate",
        "raw_notes": (
            "Stopped conveyor. Applied lockout/tagout. Removed sensor cover. "
            "Found defective photoelectric sensor. Disconnected old sensor cable. "
            "Installed replacement sensor. Adjusted sensor position until object detection was stable. "
            "Checked sensor signal in HMI. Removed lockout/tagout. Ran one test cycle. "
            "Conveyor started and stopped correctly. No alarms. OK."
        ),
    },
    "Servo motor calibration": {
        "document_title": "Servo motor calibration on pick-and-place unit",
        "equipment_or_system": "Pick-and-place unit",
        "target_user": "Automation technician",
        "experience_level": "experienced",
        "raw_notes": (
            "Machine stopped after position error on vertical axis. Put machine in maintenance mode. "
            "Checked mechanical movement by hand. No obstruction found. Opened servo drive diagnostics. "
            "Encoder position looked offset after motor replacement. Homed axis slowly. "
            "Adjusted zero position in controller. Saved calibration parameters. "
            "Ran manual jog test up and down. Then ran automatic pick-and-place test with empty tray. "
            "Movement smooth. Position error cleared."
        ),
    },
    "Camera housing cleaning": {
        "document_title": "Cleaning procedure for inspection camera housing",
        "equipment_or_system": "Vision inspection station",
        "target_user": "Production operator",
        "experience_level": "beginner",
        "raw_notes": (
            "Image quality was poor. Stopped machine at end of batch. Opened camera housing. "
            "Lens cover had dust and product residue. Wiped lens cover with approved cleaning cloth "
            "and cleaning liquid. Did not touch camera lens directly. Checked light ring for dirt. "
            "Cleaned inside of housing. Closed cover. Started machine. Ran inspection test with reference item. "
            "Image sharp again. Inspection passed."
        ),
    },
}

st.header("Input")

selected_example = st.selectbox(
    "Load example",
    options=["Custom input"] + list(EXAMPLES.keys()),
)

example = EXAMPLES.get(selected_example, None)

document_title = st.text_input(
    "Document title",
    value=example["document_title"] if example else "",
)

equipment_or_system = st.text_input(
    "Equipment or system",
    value=example["equipment_or_system"] if example else "",
)

target_user = st.text_input(
    "Target user",
    value=example["target_user"] if example else "",
)

experience_level = st.selectbox(
    "Experience level",
    options=[level.value for level in ExperienceLevel],
    index=(
        [level.value for level in ExperienceLevel].index(example["experience_level"])
        if example
        else 1
    ),
)

raw_notes = st.text_area(
    "Raw technical notes",
    height=200,
    value=example["raw_notes"] if example else "",
)

if st.button("Generate Work Instruction", type="primary"):
    try:
        input_data = WorkInstructionInput(
            document_title=document_title,
            equipment_or_system=equipment_or_system,
            target_user=target_user,
            experience_level=ExperienceLevel(experience_level),
            raw_notes=raw_notes,
        )

        pipeline = WorkInstructionPipeline(mock_mode=mock_mode)
        result = pipeline.run(input_data)

        if save_outputs:
            pipeline.save_outputs(result)
            st.success("Outputs saved to outputs/work_instruction.json and outputs/work_instruction.md")

        st.subheader("Rule Check")

        if result.rule_check.passed:
            st.success("All rule checks passed.")
        else:
            for warning in result.rule_check.warnings:
                st.warning(warning)

        st.subheader("Generated Work Instruction")

        st.markdown(result.markdown)

        st.download_button(
            label="Download Markdown",
            data=result.markdown,
            file_name="work_instruction.md",
            mime="text/markdown",
        )

        st.download_button(
            label="Download JSON",
            data=result.work_instruction.model_dump_json(indent=2),
            file_name="work_instruction.json",
            mime="application/json",
        )

    except Exception as e:
        st.error(str(e))