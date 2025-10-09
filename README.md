# Shopping — CS50 AI Project (Flask + ML)

A clean, production-ready template for Harvard’s CS50 AI Shopping project, adapted for a Flask web app with ML model training and prediction.

Replace placeholders marked with TODO to fit your repo.

## Repository

- Source: https://github.com/grantMU3000/Shopping

## Overview

- Goal: Predict whether a user session will result in a purchase (Revenue) from online shopping session data.
- Task: Binary classification.
- Data: 18 input features per session plus the target label (Revenue).
- App: Flask web interface for uploading CSVs, validating input, running predictions, and viewing metrics.

## Features

- Upload a CSV (Shopping.csv-compatible) and validate file structure/types.
- Choose data source:
  - Upload your dataset
  - Use a sample dataset (optional)
- Train and persist an ML model (e.g., k-NN or Logistic Regression).
- Predict on new data and view metrics (accuracy, sensitivity/recall, specificity).
- Friendly error handling with custom exceptions surfaced in the UI.

## Project Structure

Adjust to match your repo.

- app.py — Flask app (routes, request handling)
- ml_core.py — ML logic (load data, validate, preprocess, train, evaluate, predict)
- models/ — Saved model artifacts (e.g., .joblib)
- templates/
  - index.html — Main page (file upload, radio buttons for data source, results)
  - results.html — Metrics/predictions view (optional)
- static/
  - css/ js/ images/ — Front-end assets
- data/
  - Shopping.csv — Training/evaluation data (optional)
  - sample.csv — Example input (optional)
- tests/ — Unit tests for validation, preprocessing, model
- requirements.txt — Python dependencies
- README.md — This file
- generate_shopping_csv.py — Script to synthesize a compatible CSV (optional)
- Dockerfile / Procfile — Deployment (optional)

## Dataset Schema (Shopping.csv)

Expected column order (18 features + 1 label if included):
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
- Month (string: e.g., Feb, Mar, May, June, Jul, Aug, Sep, Oct, Nov, Dec)
- OperatingSystems (int 1–8)
- Browser (int 1–13)
- Region (int 1–9)
- TrafficType (int 1–20)
- VisitorType (Returning_Visitor, New_Visitor, Other)
- Weekend (TRUE/FALSE)
- Revenue (TRUE/FALSE) — label (may be required for training, optional for inference)

Tip: Keep headers exactly as above, in order. Encode booleans as TRUE/FALSE strings.

## Tech Stack

- Python 3.10+
- Flask
- pandas, numpy, scikit-learn, joblib
- Jinja2 templates
- Optional: gunicorn (production), Docker

## Getting Started

1. Clone the repo:
   - git clone https://github.com/grantMU3000/Shopping
   - cd Shopping

2. Create a virtual environment (recommended):
   - python -m venv .venv
   - On Windows: .venv\Scripts\activate
   - On macOS/Linux: source .venv/bin/activate

3. Install dependencies:
   - pip install -r requirements.txt

4. Run the app (development):
   - set FLASK_APP=app.py (Windows) or export FLASK_APP=app.py (macOS/Linux)
   - flask run
   - Open http://127.0.0.1:5000

Alternatively:
- python app.py

## Configuration

Set via environment variables or a .env file (if using python-dotenv).

- FLASK_ENV=development
- SECRET_KEY=TODO-generate-a-secret
- MODEL_PATH=models/model.joblib
- UPLOAD_FOLDER=./uploads
- MAX_CONTENT_LENGTH=5_000_000 (bytes)

## Usage

- Web UI:
  - Visit the home page.
  - Choose your data source (radio buttons).
  - If “Upload” is selected, pick a CSV that matches the schema.
  - Submit; the app validates file, trains or loads a model, and shows metrics/predictions.

- CLI (optional; if you expose scripts):
  - Train: python ml_core.py --train data/Shopping.csv --save models/model.joblib
  - Predict: python ml_core.py --predict data/new_sessions.csv --load models/model.joblib --out predictions.csv

Adjust to your actual script names/flags.

## Validation and Error Handling

Example validation flow (ml_core.py):
- checkValidFile(filename) returns an error string if invalid; empty string if OK.
- If invalid, raise MyCustomError(message).

Catching the error in Flask (app.py):
- Wrap ML calls in try/except and surface the message via flash() or a rendered template.

Example:

```python
from flask import render_template, request, flash
from ml_core import MyCustomError, run_pipeline

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        flash('Please select a file.', 'error')
        return render_template('index.html'), 400
    try:
        results = run_pipeline(file)  # may raise MyCustomError
        return render_template('results.html', **results)
    except MyCustomError as e:
        flash(str(e), 'error')
        return render_template('index.html'), 400
```

Front-end toggle (index.html):
- JavaScript enabling/disabling the file input based on the selected radio:

```html
<script>
  const radios = document.querySelectorAll('input[name="data_source"]');
  const fileInput = document.getElementById('file');
  radios.forEach(r => {
    r.addEventListener('change', () => {
      fileInput.disabled = (r.value !== 'upload' || r.checked);
    });
  });
</script>
```

Adjust logic to your desired UX.

## Modeling

Default (CS50 AI baseline):
- Model: k-Nearest Neighbors (k=1) or similar simple classifier.
- Evidence preprocessing:
  - Cast numeric columns
  - Encode Month to ordinal/categorical
  - Encode VisitorType
  - Map Weekend/Revenue from TRUE/FALSE to booleans or 0/1
- Metrics:
  - Accuracy
  - Sensitivity (Recall for positive Revenue)
  - Specificity (Recall for negative Revenue)

Consider experimenting with:
- Normalization/standardization
- Cross-validation
- Logistic Regression, Random Forests
- Hyperparameter tuning (GridSearchCV)

## API Endpoints (if you expose a JSON API)

- GET / — Index page
- POST /upload — Accepts a CSV; returns HTML with metrics/predictions
- POST /api/predict — JSON upload or CSV file; returns JSON predictions
- GET /health — Health check

Document request/response formats and error codes if you publish the API.

## Testing

- Add unit tests for:
  - checkValidFile
  - preprocess (dtypes, encodings)
  - train/evaluate (shape, metric sanity)
- Run tests:
  - pytest -q

## Deployment

- Production server (example): gunicorn wsgi:app --bind 0.0.0.0:8000
- Procfile (Heroku/Render):
  - web: gunicorn wsgi:app
- Docker (optional):
  - Build: docker build -t shopping-app .
  - Run: docker run -p 8000:8000 shopping-app

Remember to:
- Set SECRET_KEY
- Persist models/volumes if training in production
- Enforce MAX_CONTENT_LENGTH and file validation

## Sample Data

- data/Shopping.csv — Original training data
- data/sample.csv — Minimal valid input for quick testing
- generate_shopping_csv.py — Script to synthesize 1,000+ rows for development

## Known Issues / Troubleshooting

- Header mismatch: Ensure exact column names and order.
- Bad types: Cast numbers; TRUE/FALSE for booleans; valid Month strings.
- Unicode errors: Save CSV as UTF-8.
- Large files: Increase MAX_CONTENT_LENGTH or downsample.
- Model not found: Train first or ship a pre-trained model in models/.

## Acknowledgments

- Harvard CS50 AI — Shopping project (classification).
- Dataset: Online Shoppers Purchasing Intention (adapted in CS50). Review original terms before distribution.

## License

- TODO: Choose a license (e.g., MIT) and include LICENSE file.
