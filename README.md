# Structured Data Extraction from Archived HTML Emails

## Abstract

This project presents a lightweight data extraction pipeline designed to transform archived HTML emails into structured, machine-readable datasets. The system focuses on recovering actionable information from unstructured inbox data—such as food delivery confirmations and content-based emails—and exporting the extracted information into standardized JSON formats for downstream analysis.

The approach relies on deterministic HTML parsing using Python and BeautifulSoup, prioritizing interpretability, reproducibility, and ease of extension over black-box automation.

---

## Repository Structure
Parsing/
├── extract_all_mails.py        # Core extraction and parsing logic  
├── bonus.py                   # Optional post-processing and enrichment  
├── all_deliveroo_orders.json  # Parsed food delivery order dataset  
├── all_quotes.json            # Parsed textual quote dataset  
├── requirements.txt           # Project dependencies  
├── Makefile                   # Task automation  
└── README.md                  # Project documentation  

---

## Problem Statement

Large volumes of valuable personal and transactional data remain locked in archived email inboxes, typically stored as unstructured HTML files. While human-readable, this format severely limits programmatic reuse for quantitative analysis, historical auditing, or personal analytics.

This project addresses the problem by:
- Identifying recurring email templates
- Extracting semantically meaningful fields
- Normalizing the extracted content into structured datasets

---

## Methodology

The extraction pipeline follows a deterministic, rule-based process:

1. Load archived HTML email files from disk  
2. Parse document structure using BeautifulSoup  
3. Identify email type based on structural and textual cues  
4. Extract domain-specific fields (orders, prices, metadata, text)  
5. Serialize results into JSON datasets  

This approach ensures transparency, debuggability, and robustness against partial parsing failures.

---

## Scripts

### extract_all_mails.py

The primary script implementing the extraction pipeline.

**Responsibilities**
- Traverse local HTML email archives
- Detect and classify supported email types
- Extract structured fields from known templates
- Persist results as JSON files

**Generated Outputs**
- `all_deliveroo_orders.json`
- `all_quotes.json`

**Extracted Attributes (Orders)**
- Customer identification (name, phone, address)
- Merchant identification (name, address, contact details)
- Order identifiers
- Item-level details (quantity, description, options, price)
- Pricing breakdown (subtotal, delivery fees, credits, total)
- Source metadata (filename)

---

### bonus.py

An auxiliary script used for optional post-processing.

**Use cases**
- Data validation
- Filtering or aggregation
- Experimental transformations
- Feature engineering for downstream analysis

This script is intentionally decoupled from the core extraction logic.

---

## Data Outputs

### all_deliveroo_orders.json

A structured dataset representing historical food delivery orders extracted from transactional emails.

Each entry corresponds to a single order and preserves both semantic content and traceability to the original source file.

Potential analytical applications include:
- Longitudinal spending analysis
- Consumption pattern analysis
- Merchant frequency analysis
- Delivery cost evaluation

---

### all_quotes.json

A structured textual dataset composed of extracted quotations.

Each record includes:
- Quote text
- Author attribution
- Optional categorical tags

This dataset is suitable for natural language processing experiments, semantic clustering, or content indexing.

---

## Installation

A virtual environment is recommended to ensure dependency isolation.

python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  

### Dependencies
- requests  
- beautifulsoup4  

---

## Execution

Run the core extraction pipeline:

python extract_all_mails.py  

This regenerates:
- all_deliveroo_orders.json
- all_quotes.json

Optional post-processing:

python bonus.py  

---

## Automation

A Makefile is provided to streamline common workflows such as execution and cleanup. Refer directly to the Makefile for available targets.


---
