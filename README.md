# 📊 COVID Case Analysis with Streamlit & OOP

This repository provides an example project for teaching Object-Oriented Programming (OOP) within a Data Science context. It demonstrates how to analyse COVID‑19 case data using a custom Python class and present the results through an interactive [Streamlit](https://streamlit.io/) dashboard.

The project is designed for degree apprentices learning how OOP principles can be applied to real-world data workflows.

---

## 🚀 Project Overview

This example shows how to:

- Load and process COVID case data
- Encapsulate data logic inside a custom OOP class
- Build an interactive Streamlit app for visualisation
- Apply good software engineering practices (structure, modularity, documentation)

The aim is to help students understand how OOP can make data analysis code cleaner, more modular, and easier to extend.

---

## 🧱 Repository Structure
```
├── analysis/                   # All the data science stuff
│   ├── constants.py
│   ├── covid_analysis.py
│   └── data_loader.py
│
├── layout/                     # All the streamlit stuff
│   ├── home.py
│   ├── charts.py
│   └── components.py
│
├── tests/                      # Any unit tests
│   ├── test_data_cleaning.py
│   ├── test_trend_analysis.py
│   └── test_streamlit.py
│
├── data/                       # Where the data is kept
│   └── covid_cases.csv
│
├── main.py
├── pyproject.toml
└── README.md
```

---

## 🧠 Why This Structure Works Well

Keeping each part of the project in its own folder makes the code easier to understand, maintain, and extend:

- **analysis/**
  Holds all data‑processing logic. Separating this from the UI keeps the analytical code clean, reusable, and easy to test.

- **layout/**
  Contains Streamlit layout files so the interface is organised and doesn’t clutter `app.py`. This makes adding new pages or components straightforward.

- **tests/**
  Keeps all tests in one place, reinforcing good engineering habits and making it easy to validate that the analysis code behaves correctly.

- **data/**
  Stores datasets separately from code, which avoids accidental modification and makes the project more reproducible.

- **main.py**
  Acts as the single entry point that ties everything together, making the project easy to run and navigate.

This structure mirrors how real data applications are organised and helps learners see the benefits of modular, well‑designed codebases.