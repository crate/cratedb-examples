# Timeseries QA with LLMs

*Combine Telemetry Data and Manuals for Smarter Diagnostics.*

---

## Summary

In this hands-on workshop, participants will build an AI-powered assistant that can answer questions using a combination of **timeseries telemetry data** and **structured machine manuals**. 

Using **CrateDB** as a scalable time-series database and **OpenAI's large language models**, attendees will walk through how to:
- Simulate telemetry data
- Store and query with SQL
- Convert natural language into structured SQL queries
- Integrate external context (like manuals)
- Generate explanations and visualizations based on live data

This workshop combines **Table-Augmented Generation (TAG)** with best practices in prompt design, data enrichment, and telemetry monitoring — creating an interactive diagnostics assistant from scratch.

By the end of the session, participants will have a working QA system capable of answering both technical and operational questions in natural language, using real telemetry data and contextual documentation.

---

## Key Takeaways

- Understand how to build a **TAG (Table-Augmented Generation)** assistant using structured data and manuals
- Learn how to simulate, store, and analyze **timeseries data** in **CrateDB**
- Master prompt engineering techniques to guide LLMs in generating accurate SQL queries
- Combine telemetry results with structured documentation (manuals) to generate full-context answers
- Create **visualizations** from natural-language queries using **Matplotlib and Plotly**
- Explore how LLMs can reason across structured (CrateDB) and unstructured (manuals) sources

---

## Requirements from Attendees

- **Laptop + Charger** (for running Jupyter notebooks)
- **Python Basics** (e.g. working with pandas, functions, etc.)
- **Basic SQL Knowledge** (SELECT, WHERE, GROUP BY…)
- **OpenAI API Key** (required for accessing GPT)

---

## Maturity Level

**Intermediate**  
This workshop is ideal for developers, data engineers, solution architects, and tech leads who have some experience with Python and data querying. No deep ML background is needed — the focus is practical application.

---

## Type of Workshop

**Hands-On Lab**  
Participants will interactively build, run, and modify a full-stack LLM-powered assistant. Exercises are incremental, exploratory, and designed for real-world relevance.

---

## Try It Out

You can explore the full interactive notebook in two ways:

### ▶️ Run It Directly in Google Colab
Click below to launch the notebook in a ready-to-use Colab environment (no setup needed):

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crate/cratedb-examples/blob/main/topic/chatbot/table-augmented-generation/workshop/telemetry-diagnostics-assistant.ipynb)

### 📓 View the Notebook on GitHub
[🧠 Timeseries QA Notebook (Jupyter)](https://github.com/crate/cratedb-examples/blob/main/topic/chatbot/table-augmented-generation/workshop/telemetry-diagnostics-assistant.ipynb)
