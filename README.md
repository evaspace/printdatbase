# printdatbase
This program is quick, efficient and very user-friendly. made to displays those .db files in your command prompt.


# SQLite Interactive Table Viewer (CLI)

## Overview

This project is a **command-line interface (CLI) utility** written in Python, designed to **explore and visualize SQLite databases** in a structured, readable, and color-enhanced tabular format.

The program allows the user to:
- Open any SQLite database file
- Enumerate available tables
- Select specific columns to display
- Apply ordering (ascending or descending)
- Limit the number of displayed rows
- Render results in a formatted ASCII table with semantic color coding

The tool is **database-agnostic**: it operates on *any* SQLite database without prior schema knowledge.

---

## Key Features

- Dynamic database inspection (no hardcoded schema)
- Interactive table and column selection
- Optional sorting by any column
- Row limiting for large datasets
- Readable ASCII table output
- Semantic color highlighting:
  - `NULL` → red
  - Empty values → red
  - Zero values → yellow
- Graceful error handling
- No external services, no telemetry

---

## Preview

At launch, the program displays a banner and guides the user step by step:

