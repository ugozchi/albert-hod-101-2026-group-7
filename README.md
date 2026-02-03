# albert-hod-101-2026-group-7

**Head of Data 101 – Group 7**  
Students: Thomas ALAPHILIPPE, Feliz, Nico, Ugo

---

## Project Overview

This repository contains all the work we have done for the **Head of Data 101** course. We have centralised the different deliverables: BigQuery, Information Retrieval, Parsing, Chatbot, and SlackAPI. Each folder corresponds to a module or part of the course, with the associated scripts, queries, and documentation.

We wanted to keep a clear structure so that every member of the group can find their way around and to make it easier for instructors to review our work.

---

## Repository Structure

### BigQuery
We worked on two parts:
- **Part 1**: Deliveroo Plus – identifying subscription periods from transactional data (SQL queries, step-by-step pipeline, tests).
- **Part 2**: E-commerce data consolidation – identifying and using “validated weekly” tables, with a multi-step pipeline.

Each part has a detailed README and a `Queries/` folder with the SQL queries.

### Information Retrieval
We completed several assignments:
- **Assignment 1**: TF-IDF (part 1), cosine similarity for product search (part 2), Levenshtein distance and complexity analysis (part 3). Everything is implemented in Python without scikit-learn, as required.
- **Assignment 2**: Evaluation of the classification system (Fox) – accuracy, precision, recall, F1-score per category, confusion matrix, and reliability analysis.

Source data and scripts are organised in `source/` and `scripte/` folders per assignment.

### Parsing
Work on data parsing (HTML, etc.) with deliverables in the dedicated folder.

### Chatbot
Development of a chatbot with the necessary scripts and resources (including the Othello corpus for training or testing).

### SlackAPI
Integration and use of the Slack API (deliverable structure, scripts, and any screenshots or documentation).

---

## How to Navigate

- Each main folder (**BigQuery**, **Information Retrieval**, etc.) contains one or more READMEs describing the objectives, methodology, and how to use the files.
- **Source** data (CSV, datasets) are in `source/` folders where applicable.
- **Scripts** (Python or other) are in `scripte/` folders or at the root of subfolders depending on the module.

We made sure that paths in the scripts are consistent with this structure so that the commands given in the READMEs work as-is.

---

## Notes

- For the Information Retrieval assignments, we did not use scikit-learn; calculations (TF-IDF, cosine similarity, classification metrics, etc.) are implemented manually or with authorised libraries.
- The BigQuery queries are designed to be run in the specified environment (project, dataset, etc.); each Part’s README gives the context.

If you have questions about a specific deliverable, the local READMEs and comments in the code should provide the necessary details. Happy reading.
