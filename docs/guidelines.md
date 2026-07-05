# Development Guidelines

## Branching Strategy

- `main` — production. Only merged from `develop`.
- `develop` — integration. Only merged from feature/fix/chore branches.
- Feature branches — all work happens here. **No direct commits to `main` or `develop` ever.**

### Branch Naming

| Prefix       | When to use                         | Example                      |
|--------------|--------------------------------------|------------------------------|
| `feature/`   | New entities or features             | `feature/orders-silver`      |
| `fix/`       | Bug fixes                            | `fix/schema-date-cast`       |
| `chore/`     | Config, deps, tooling, docs          | `chore/add-dbt-packages`     |

## Workflow

1. `git checkout develop && git pull && git checkout -b <prefix>/<description>`
2. Implement changes with conventional commits (see below)
3. `git push -u origin <prefix>/<description>`
4. Create PR into `develop` via GitHub CLI or UI
5. Merge via GitHub UI (squash merge recommended)
6. Delete the remote branch after merge

## Commit Message Convention

```
<type>(<scope>): <description>
```

| Type       | Usage                             | Example                                  |
|------------|-----------------------------------|------------------------------------------|
| `feat`     | New entity, feature, or component | `feat(orders): add bronze pipeline`       |
| `fix`      | Bug fix                           | `fix(dbt): replace deprecated macro`      |
| `refactor` | Restructuring without new behavior | `refactor(silver): extract generic runner`|
| `chore`    | Config, deps, tooling, docs       | `chore(makefile): add dbt-deps target`    |
| `test`     | Adding or updating tests          | `test(customer): add schema unit tests`   |

## Coding Conventions per Entity

Every new entity follows the same template:

1. `src/schemas/<entity>_schema.py` — source Kafka schema + bronze Parquet schema
2. `src/bronze/<entity>.py` — 3-5 line runner call
3. `src/silver/<entity>.py` — transform function + runner call
4. `dbt_retail/models/silver/sources.yml` — add table entry under `snowflake_silver`
5. `dbt_retail/models/gold/dim_<entity>.sql` — incremental merge model
6. `dbt_retail/models/gold/dim_<entity>.yml` — column tests

Minimal boilerplate: schemas + transform function ~60 lines per entity.

## Order of Operations

- Bronze → Silver → dbt run → dbt test (must run in sequence)
- Delete checkpoint dirs after schema column renames (checkpoint stores column metadata)
