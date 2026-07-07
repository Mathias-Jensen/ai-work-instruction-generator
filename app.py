# app.py

import streamlit as st
from dotenv import load_dotenv

from src.models import ExperienceLevel, WorkInstructionInput
from src.pipeline import WorkInstructionPipeline


load_dotenv()

st.set_page_config(
    page_title="AI Work Instruction Generator",
    page_icon="🛠️",
    layout="wide",
)

st.title("AI Work Instruction Generator")
st.write(
    "Convert unstructured technical notes into a structured work instruction draft."
)

with st.sidebar:
    st.header("Settings")
    mock_mode = st.toggle("Use mock mode", value=True)
    save_outputs = st.toggle("Save outputs locally", value=False)

st.header("Input")

document_title = st.text_input(
    "Document title",
    value="Sensor replacement on conveyor system",
)

equipment_or_system = st.text_input(
    "Equipment or system",
    value="Conveyor system",
)

target_user = st.text_input(
    "Target user",
    value="Maintenance technician",
)

experience_level = st.selectbox(
    "Experience level",
    options=[level.value for level in ExperienceLevel],
    index=1,
)

raw_notes = st.text_area(
    "Raw technical notes",
    height=200,
    value=(
        "Stopped conveyor. Locked out power. Removed sensor cover. "
        "Replaced defective sensor. Adjusted position. Checked signal in HMI. "
        "Ran test cycle. OK."
    ),
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