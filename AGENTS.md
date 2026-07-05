# Agent Instructions

## Project Context
RetailCortex — medallion pipeline (bronze/silver/gold) on Snowflake + PySpark + dbt.

## Key Files
- `docs/guidelines.md` — branching, commits, coding conventions (READ BEFORE WORKING)
- `src/bronze/runner.py` — generic bronze runner
- `src/silver/runner.py` — generic silver runner
- `src/schemas/customer_schema.py` — template for new entity schemas

## Guidelines Summary
- **Never** commit to `main` or `develop` directly. Always create a feature/fix/chore branch.
- Branch off `develop`, push, create PR, merge via GitHub UI, delete branch.
- Conventional commits: `feat(<scope>):`, `fix(<scope>):`, `chore(<scope>):`, etc.
- New entities need: schema + bronze file + silver file + dbt silver source + dbt gold model + dbt gold yml.
- Run order: bronze → silver → dbt run → dbt test.
- Delete checkpoint dirs after schema changes.
