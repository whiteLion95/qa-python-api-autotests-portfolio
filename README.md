# Python API Autotests — JSONPlaceholder

Automated API test suite built with **Python + pytest** for QA portfolio purposes.

## Tech Stack
- Python 3.11+
- pytest 8.x
- requests
- jsonschema
- pytest-html

## What's Covered
| Endpoint     | Methods Tested              |
|--------------|-----------------------------|
| `/posts`     | GET, POST, PUT, PATCH, DELETE |
| `/users`     | GET, POST                   |
| `/comments`  | GET (with filtering)        |

## Test Types Used
- ✅ Status code validation
- ✅ JSON schema validation
- ✅ Response body assertions
- ✅ Query parameter filtering
- ✅ Response time checks
- ✅ Parametrized tests
- ✅ Edge cases (404s, empty bodies)

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run Tests

```bash
pytest                    # run all, generate HTML report
pytest -v                 # verbose
pytest -k "delete"        # filter by name
```

## HTML Report
After running, open `reports/report.html` in your browser.
