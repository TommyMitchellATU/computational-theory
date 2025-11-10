# Computational Theory Exercises

This repository contains implementations and explanatory notebooks for core computational theory and low-level bitwise functions (e.g., rotations, logical mixing functions) that underpin cryptographic hash constructions and other algorithms.

## Repository Structure
```
computational-theory/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ notebooks/
│  └─ problems.ipynb
├─ assets/
│  └─ screenshot_2025-10-15_113458.png
```

## Environment Setup
Prerequisites: Python 3.11 (recommended), `pip`.

Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

Launch Jupyter:
```bash
jupyter lab
```
Open `notebooks/problems.ipynb`.

## Core Concepts Implemented
- Bitwise rotation (`rotr`) and logical shift (`shr`)
- Boolean combination functions (`parity`, `ch`)
- 32-bit word normalization (`to_uint32`) to ensure correctness under overflow

Each function is annotated with docstrings and accompanied by validation examples.

## References
- SHA-256 specification (FIPS 180-4) – basis for functions like `Ch` and rotation semantics: [FIPS 180-4 PDF](https://csrc.nist.gov/publications/detail/fips/180/4/final) (Used to guide function definitions.)
- NumPy unsigned integer scalar behavior: [NumPy uint types](https://numpy.org/doc/stable/reference/arrays.scalars.html#numpy.uint32) (Ensures correct casting/wrap-around.)
- Python bitwise operators: [Python Docs – Expressions](https://docs.python.org/3/reference/expressions.html#binary-bitwise-operations) (Clarifies operator precedence and behavior.)

References are placed inline in notebook sections where they directly inform implementation.

## Running & Reproducing
1. Open the notebook.
2. Restart the kernel.
3. Run all cells top to bottom.
4. Confirm validation outputs match expected hex values.