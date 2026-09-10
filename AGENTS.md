# Repository Guidelines

## Project Structure & Module Organization

Root-level Python files contain Collatz experiments; `collatz.py` implements
the classical map and `main.py` provides the CLI. `.lean` files contain proofs.
Read `RutaTeoremas.md` for research status and `CLAUDE.md` for working conventions.

`depuracion/` holds claim specifications (`fichas/`), independent Python
checks (`py/`), Lean proofs (`lean/`), and `veredictos.jsonl`, the authoritative
audit record. `revision*_adv*/` contains review reproductions. Research
artifacts include `*_salida.txt`, notes, SQLite databases, and archived
sessions in `transcripciones/`.

## Companion Repository: zootheorem

`../zootheorem/`, also on the Desktop, publishes results from this laboratory.
It contains articles in `papers/`, integer sequences in `seqs/`, independent
dependency-free Python checks in `verify/`, and the Lean mirror theorem in
`lean/mirror_theorem.lean`. `drafts/` holds publication and OEIS submission work.
From that repository, run `python verify/verify_merging_classes.py`,
`python verify/verify_q_family.py`, or `lean lean/mirror_theorem.lean`.
Keep published statements consistent with verified laboratory results and
distinguish proved, computed exactly, and measured claims.

## Build, Test, and Development Commands

Run commands from the repository root:

- `python -m pip install -r requirements.txt`: install NumPy, Matplotlib, and Plotly.
- `python main.py camino 27`: print one classical Collatz trajectory.
- `python main.py verificar --limite 10000`: check a bounded seed range.
- `python main.py records --limite 10000`: report trajectory records.
- `python verificar_constantes.py`: run the independent constants audit.
- `lean --version`: confirm the separately installed Lean 4 toolchain.
- `lean depuracion/lean/A1.lean`: check an individual proof using Lean's core.

There is no package build step. Inspect script parameters before expensive sweeps.

## Coding Style & Naming Conventions

Use four-space Python indentation, descriptive Spanish `snake_case` names,
and simple standalone scripts. Preserve mathematical notation. No formatter
or linter is configured. Prefer integers or `fractions.Fraction` for exact
claims; label floating-point measurements explicitly.

## Testing Guidelines

There is no centralized test framework, CI, or coverage threshold. Use
`verificar_*.py` checks and claim-specific `depuracion/py/A<number>.py` and
`A<number>_comp.py` scripts. For mathematical changes, pair an independent
calculation with a Lean proof where applicable and compare their assumptions.
Check boundary cases, identify classical versus accelerated steps, and record
parameters and failures. Finite sweeps are evidence, never universal proofs.

## Commit & Pull Request Guidelines

History uses Spanish, descriptive research summaries, often with uppercase
lead phrases and detailed evidence; it does not follow Conventional Commits.
Describe the finding or correction and its verification. Keep changes focused.
PRs should identify affected claims, link relevant issues or audit records,
list reproduction commands and results, and state unresolved limitations.
Update research notes when conclusions change; preserve historical evidence.
