# AI Documentation Assistant

> AI-assisted generation of structured technical documentation from unstructured engineering notes.

---

## Overview

AI Documentation Assistant is an AI-powered documentation pipeline that transforms unstructured technical notes into consistent, structured documentation.

The current MVP focuses on generating **Work Instructions**, but the architecture is intentionally modular and designed to support additional document types such as:

- Standard Operating Procedures (SOPs)
- Service Reports
- Maintenance Checklists
- Risk Assessments

Rather than acting as a chatbot, the system combines Generative AI with structured validation, business rules and deterministic document generation to automate a common engineering workflow.

---

## Problem Statement

Many companies rely on experienced employees to manually transform rough technical notes into formal work instructions.

This results in:

- Time-consuming documentation
- Inconsistent formatting
- Missing safety information
- Variable document quality
- Heavy reliance on experienced personnel

---

## Solution

The application converts raw technical notes into a structured Work Instruction.

The pipeline consists of:

1. User input
2. Prompt generation
3. LLM generation
4. JSON validation
5. Business rule validation
6. Markdown document generation

Human review is always required before operational use.

---

## Features

- Streamlit user interface
- AI-assisted document generation
- Structured JSON output
- Pydantic validation
- Rule-based quality checks
- Markdown export
- JSON export
- Mock mode for offline demonstrations

---

## Architecture

```text
User Input
      │
      ▼
Prompt Builder
      │
      ▼
LLM
      │
      ▼
JSON Validation
      │
      ▼
Business Rules
      │
      ▼
Markdown Generator
      │
      ▼
Work Instruction
```

---

## Project Structure

```text
app.py
src/
prompts/
templates/
examples/
outputs/
```

---

## Installation

```bash
git clone <repo>

cd ai-work-instruction-generator

pip install -r requirements.txt
```

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key
```

Run:

```bash
streamlit run app.py
```

---

## Example Workflow

Input:

```text
Stopped conveyor.
Applied lockout/tagout.
Removed sensor.
Installed replacement.
Verified signal.
Ran test cycle.
```

Output:

- Structured work instruction
- Safety precautions
- Quality checks
- Risk assessment
- AI assumptions
- Missing information

---

## Technologies

- Python
- Streamlit
- OpenAI API
- Pydantic
- Jinja2

---

## Limitations

This application generates documentation drafts only.

Generated documents must always be reviewed and approved by qualified personnel before operational use.

---

## Future Improvements

- Multiple document types
- DOCX export
- PDF export
- Image support
- Company-specific templates
- RAG integration
- SharePoint integration
- Version history

---

## License

MIT License