# ReconcileX

**A desktop-based data reconciliation tool for comparing financial and operational datasets.**

ReconcileX helps identify records that match exactly, records that differ within a configurable numeric tolerance, and records that may represent the same transaction despite minor text variations. It provides a guided desktop workflow for importing files, mapping columns, reviewing reconciliation results, and exporting an Excel report.

> **Project status:** Initial development release (v1.0). Review the implementation notes below before using the application for production or financial close processes.

---

## Overview

Reconciling two files manually can be time-consuming when the files come from different systems and use different column names, formats, or descriptions. ReconcileX brings the two datasets into a common structure and applies a staged matching process to help users investigate differences.

Typical use cases include:

- Comparing sales invoices with bank transactions.
- Matching vendor or customer records across systems.
- Reviewing differences between two operational exports.
- Identifying possible matches where descriptions contain spelling or formatting variations.
- Producing a structured Excel workbook for further review.

## Key capabilities

| Capability | Description |
|---|---|
| CSV and Excel import | Load two datasets from CSV or Excel files. |
| Column mapping | Map columns from Dataset B to the corresponding fields in Dataset A, with automatic suggestions for simple header similarities. |
| Exact matching | Identify records that match across the selected key columns. |
| Tolerance matching | Identify candidate records with matching key fields and a numeric difference within a configured threshold. |
| Fuzzy text matching | Compare text values using similarity scoring after matching the other selected key fields. |
| Results dashboard | Review exact matches, tolerance matches, fuzzy matches, and unmatched records in separate tabs. |
| Search and filtering | Search across the result tables to locate records quickly. |
| Excel export | Export the reconciliation result groups to an Excel workbook. |
| Background processing | Run reconciliation in a Qt worker thread so the interface can remain responsive during processing. |

## How it works

ReconcileX follows a guided, three-stage workflow:

1. **Import datasets** — Select Dataset A and Dataset B. The application reads the files and removes completely blank rows and columns.
2. **Map columns and configure matching** — Review the suggested column mappings, choose the fields to compare, and configure tolerance and fuzzy-match settings.
3. **Run reconciliation and review results** — The engine processes the datasets and displays the results in separate tabs. Export the results to Excel for further analysis.

### Reconciliation logic

The reconciliation engine uses a staged approach:

| Stage | Matching method | Result |
|---|---|---|
| 1 | Exact matching | Records with identical values across the selected match columns. |
| 2 | Tolerance matching | Remaining records that match on the other key fields and whose configured numeric difference is within the tolerance. |
| 3 | Fuzzy matching | Remaining records that match on the other selected fields and whose text similarity score meets the threshold. |

The application keeps records that are not matched in separate Dataset A and Dataset B result groups.

**Important:** Tolerance and fuzzy matching are intended to identify candidate matches for review. A similarity score or an in-tolerance difference should not, by itself, be treated as proof that two transactions are equivalent.

## Technology stack

- **Language:** Python
- **Desktop UI:** PySide6 (Qt for Python)
- **Data processing:** pandas and NumPy
- **Excel input/output:** openpyxl and XlsxWriter
- **Text similarity:** TheFuzz / RapidFuzz / python-Levenshtein
- **Testing:** pytest-compatible test dependencies and standalone test scripts
- **Windows installer configuration:** Inno Setup script

## Project structure

```text
ReconcileX/
├── assets/
│   ├── app_icon.ico
│   ├── RecX.ico
│   └── style.qss
├── core/
│   ├── column_mapper.py
│   ├── file_reader.py
│   ├── matcher_exact.py
│   ├── matcher_fuzzy.py
│   ├── matcher_tolerance.py
│   ├── normalization.py
│   └── reconciliation_engine.py
├── reports/
│   └── excel_exporter.py
├── ui/
│   ├── import_screen.py
│   ├── main_window.py
│   ├── mapping_screen.py
│   └── results_screen.py
├── workers/
│   └── recon_worker.py
├── main.py
├── requirements.txt
├── setup_builder.iss
├── create_test_data.py
├── test_engine.py
├── test_fuzzy.py
├── test_mapper.py
├── test_matcher.py
├── test_normalization.py
├── test_reader.py
└── test_tolerance.py
```

### Main modules

- `core/file_reader.py` — Loads CSV and Excel data into pandas DataFrames and removes fully blank rows and columns.
- `core/column_mapper.py` — Suggests and applies Dataset B-to-Dataset A column mappings.
- `core/normalization.py` — Provides reusable helpers for standardizing text, numeric values, and dates.
- `core/matcher_exact.py` — Performs exact matching using a pandas outer merge.
- `core/matcher_tolerance.py` — Finds candidates that meet a numeric tolerance.
- `core/matcher_fuzzy.py` — Calculates text similarity scores for candidate records.
- `core/reconciliation_engine.py` — Orchestrates the matching stages and returns the result DataFrames.
- `workers/recon_worker.py` — Runs the reconciliation engine in a background Qt thread.
- `ui/` — Contains the import, mapping, main-window, and results screens.
- `reports/excel_exporter.py` — Creates the Excel output workbook.

## Requirements

- Windows, macOS, or Linux with a supported Python installation.
- Python version compatible with the pinned packages in `requirements.txt`.
- pip.

The repository includes a Windows installer definition, but the installer must be built from a packaged application first. See the packaging note below.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/senguptajeet/ReconcileX.git
cd ReconcileX
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the application

From the repository root, run:

```bash
python main.py
```

The application opens the ReconcileX desktop interface.

## Using ReconcileX

### Step 1 — Select the source files

- Choose **Dataset A**, such as a sales ledger or invoice register.
- Choose **Dataset B**, such as a bank statement or another system export.
- Select **Load and Proceed**.

Both datasets should contain a header row and the fields needed for reconciliation.

### Step 2 — Map the columns

- Review the suggested mappings.
- For each Dataset B field, select the corresponding Dataset A field or choose not to map it.
- Ensure the fields you intend to compare are mapped correctly.
- Select the text field to use for fuzzy matching, if required.
- Enter the tolerance and fuzzy threshold values.
- Select **Confirm Mapping & Run Reconciliation**.

### Step 3 — Review the results

The results screen provides separate views for:

- **Exact Matches**
- **Tolerance Matches**
- **Fuzzy Matches**
- **Unmatched (A)**
- **Unmatched (B)**

Use the search field to filter the result tables.

### Step 4 — Export the report

Select **Export Results to Excel**, choose a destination, and save the generated workbook.

## Test scripts

The repository includes focused scripts for the main processing components. Run them from the project root with the virtual environment activated:

```bash
python test_reader.py
python test_mapper.py
python test_normalization.py
python test_matcher.py
python test_tolerance.py
python test_fuzzy.py
python test_engine.py
```

The reader test creates and removes a temporary CSV file as part of its run. These scripts use sample data and are intended as component-level checks; they are not a substitute for validating the application against representative business data.

## Input and output

**Input formats:** CSV and Excel files are handled by the file reader. The file dialog currently offers CSV, XLSX, and XLS selections. Legacy XLS support may require an additional Excel engine such as `xlrd`, which is not currently listed in the pinned requirements.

**Output format:** Excel workbook (`.xlsx`) containing the reconciliation result groups produced by the application.

For best results, use consistent date conventions, numeric amount columns, clear headers, and stable transaction identifiers in both source files.

## Implementation notes and limitations

Please read these notes before relying on reconciliation results in a business-critical workflow:

1. **Review candidate matches.** Tolerance and fuzzy matching can produce false positives, especially when identifiers are duplicated or the source data contains repeated values.
2. **Tolerance configuration.** The current desktop worker passes `Amount` as the tolerance field to the engine. The selected matching configuration must therefore include a mapped `Amount` field for tolerance matching to run as intended.
3. **Normalization helpers.** Text, number, and date standardization functions are available in `core/normalization.py`; the current orchestration path does not automatically apply these helpers to every imported dataset.
4. **Excel formats.** XLSX is supported through the installed Excel dependencies. Legacy XLS files may need `xlrd` installed separately.
5. **Data quality and duplicates.** Duplicate keys can create multiple candidate combinations during merges. Review source data and result counts before accepting a reconciliation.
6. **Sensitive information.** Use appropriately protected files and storage locations. Do not commit real bank statements, customer records, credentials, or other confidential business data to the repository.

## Packaging for Windows

The repository contains `setup_builder.iss`, an Inno Setup configuration that expects a PyInstaller application bundle at `dist/ReconcileX/`.

A typical packaging workflow is:

1. Install PyInstaller in the active virtual environment.
2. Build and test the application bundle, ensuring the Qt plugins, SVG support, stylesheet, and application assets are included.
3. Confirm that `dist/ReconcileX/ReconcileX.exe` launches correctly.
4. Open `setup_builder.iss` with Inno Setup Compiler and compile the installer.

The exact PyInstaller command and asset collection may need adjustment for the local environment. The installer script alone does not create the application bundle.

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make focused changes and add or update tests.
4. Run the relevant test scripts.
5. Submit a pull request describing the change and its impact.

For substantial changes, please include sample input data that contains no confidential information and explain the expected reconciliation outcome.

## Security

If you discover a security issue, avoid publishing sensitive details in a public issue. Contact the repository owner through the GitHub profile instead.

## License

No license file is currently present in this repository. Unless a license is added, the project should be treated as having **no explicit open-source license**; do not assume that reuse, modification, or redistribution is permitted.

---

**Repository:** https://github.com/senguptajeet/ReconcileX  
**Maintainer:** [@senguptajeet](https://github.com/senguptajeet)
