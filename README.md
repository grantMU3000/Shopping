# Shopping — CS50 AI Project Deployed Through Flask

Production-grade implementation of Harvard’s CS50 AI Shopping project. This app predicts whether a user session will result in a purchase based on online shopping session features. The project is completed and live.

- Live site: [rgnta.pythonanywhere.com](https://rgnta.pythonanywhere.com/)
- Repository: [github.com/grantMU3000/Shopping](https://github.com/grantMU3000/Shopping)

## Status

- Project: MVP Done
- Deployment: Live on PythonAnywhere
- Stack: Python, Flask, scikit-learn, Pandas, HTML

## Overview

- Goal: Binary classification of Revenue (TRUE/FALSE) from session features.
- Input: 18 feature columns (below) per session.
- Output: Purchase likelihood (Revenue), plus basic metrics and summaries.
- UI: Upload CSV compatible with Shopping.csv, run prediction/evaluation, and see results in-browser.
- Error handling: Invalid files get clear messages returned from the server.

## Live Demo

- App URL: [https://rgnta.pythonanywhere.com/](https://rgnta.pythonanywhere.com/)
- Suggested flow:
  1. Download or prepare a CSV matching the schema below.
  2. Use the Upload form to validate and run predictions.
  3. Review metrics/results on the results page.

## Dataset Schema (Shopping.csv compatible)

Columns (in order):

- Administrative (int)
- Administrative_Duration (float)
- Informational (int)
- Informational_Duration (float)
- ProductRelated (int)
- ProductRelated_Duration (float)
- BounceRates (float 0–1)
- ExitRates (float 0–1)
- PageValues (float ≥ 0)
- SpecialDay (float in {0, 0.2, 0.4, 0.6, 0.8})
- Month (string in {Feb, Mar, May, June, Jul, Aug, Sep, Oct, Nov, Dec})
- OperatingSystems (int 1–8)
- Browser (int 1–13)
- Region (int 1–9)
- TrafficType (int 1–20)
- VisitorType (Returning_Visitor, New_Visitor, Other)
- Weekend (TRUE/FALSE)
- Revenue (TRUE/FALSE)

Notes:

- Header row must match exactly.
- Types should be valid per column.
- Common validation errors: wrong column count/order, invalid Month or VisitorType values, non-boolean Weekend/Revenue.

## Features

- CSV upload with structural and type validation.
- Server-side error messaging for invalid files.
- Model training/evaluation (binary classification).
- Predict on new data and display metrics (e.g., accuracy, sensitivity/recall, specificity).
- Simple, clean Flask UI.

## Project Structure (high-level)

- app.py — Flask app (routes, error handlers).
- shopping.py — Data loading, validation, preprocessing, model train/predict.
- templates/ — HTML templates.
- requirements.txt — Python dependencies.
- README.md — You’re here.

## Getting Started (Local)

1. Clone

   ```bash
   git clone https://github.com/grantMU3000/Shopping.git
   cd Shopping
   ```

2. Create and activate a virtual environment

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Run locally

   ```bash
   # If the app uses Flask’s CLI:
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run

   # Or, if it’s a simple entrypoint:
   python app.py
   ```

5. Open <http://127.0.0.1:5000/>

## Configuration

Environment variables (typical):

- SECRET_KEY: Flask session/signing key.
- FLASK_ENV: development or production.

Store secrets outside version control. On PythonAnywhere, set environment variables via the web console or WSGI config.

## Usage

- From the home page, choose your data source:
  - Upload a CSV file in the Shopping.csv format.
- Submit to validate and process the file.
- If valid, the app will train/evaluate or run predictions and render results.
- If invalid, you’ll see a clear error message describing what to fix.

## Error Handling

- Server raises custom exceptions for invalid CSVs (e.g., wrong header, bad value types).
- Flask catches these and returns a friendly explanation to the UI.
- Typical issues:
  - Non-boolean strings for Weekend/Revenue.
  - Unknown Month values.
  - Mismatched number of columns.
  - Commas inside fields without quotes.

## Model

- Task: Binary classification (Revenue).
- Preprocessing: Numeric casting, category normalization (e.g., Month, VisitorType), boolean parsing.
- Baseline: k-Nearest Neighbor classifier was used.
- Metrics: Accuracy, sensitivity/recall, specificity.

## Deployment (PythonAnywhere)

- Code hosted on GitHub and pulled into PythonAnywhere.
- Virtualenv created on PythonAnywhere to match requirements.txt.
- WSGI file points to the Flask app.
- Static files configured via the PythonAnywhere dashboard if needed.
- Set environment variables and reload the web app.

Helpful docs:
- Flask on PythonAnywhere: <https://help.pythonanywhere.com/pages/Flask/>

## Testing

- Unit tests for:
  - CSV validation (schema, types, categorical values).
  - Preprocessing functions.
  - Model train/predict paths.
- Optional: Integration tests for the upload route and error handling.

Run tests:

```bash
pytest -q
```

> Add a tests/ directory with fixtures for valid/invalid CSVs.

## Screenshots

- Home/Upload page: 
- Results page: TODO add screenshot

## Acknowledgments

- Harvard CS50 AI — Project Specification: Shopping.
- Deployed with PythonAnywhere.
- Thanks to open-source libraries used (Flask, scikit-learn, Pandas).

