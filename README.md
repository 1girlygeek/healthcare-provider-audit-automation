# Healthcare Provider Audit Automation

A Python and SQLite portfolio demonstration of provider-data quality controls, SQL duplicate detection, exception reporting, and proposed batch-file corrections. **All data is synthetic.** This is not a Portico integration or a production healthcare system.

## Run

Requires Python 3.9+ and no third-party dependencies.

```bash
python audit.py
python -m unittest test_audit.py
```

## Workflow

1. Import synthetic provider records from `data/providers.csv`.
2. Load the data into an in-memory SQLite database.
3. Identify duplicate IDs using SQL and validate required names, state codes, and status values.
4. Write exceptions to `output/exceptions.csv`.
5. Write proposed safe case/whitespace corrections to `output/correction_batch.csv`.
6. Record processing counts in `output/audit.log` (generated locally and ignored by Git).

The sample network supports AL, GA, TX, and OH; valid statuses are ACTIVE and INACTIVE. Invalid and duplicate records are flagged for manual review. **No source files are changed; proposed updates are not applied.**

## Sample results

| Metric | Count |
| --- | ---: |
| Provider records processed | 7 |
| Validation exceptions | 5 |
| Proposed corrections | 2 |

## Repository files

- `audit.py` — validation, SQL duplicate checking, output generation and logging
- `test_audit.py` — automated unit test for expected sample results
- `data/providers.csv` — synthetic sample input
- `output/exceptions.csv` — example exceptions report
- `output/correction_batch.csv` — example proposed updates
- `.gitignore` — excludes logs, Python caches, and local environments

## Future enhancements

NPI checks, configurable controls, secure SFTP ingestion, persistent database reconciliation, approval workflow, and audit dashboard.

**Never commit real patient or provider data, PHI, secrets, or credentials.**
