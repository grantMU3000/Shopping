import os # For working with operating system (We're working with files)
from pathlib import Path  # For creating a path to my CSV file
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename 
from shopping import load_data, train_model, evaluate, splitTrainTest

# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')  # for flashing messages
app.config['UPLOAD_FOLDER'] = os.path.join('instance', 'uploads')  # Uses Flask's file management system to store uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
ALLOWED_EXTENSIONS = {'csv'}

# Ensure upload folder exists by ensuring the Parent folders are in the path, and creating the directory
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

# Points to my CSV file in a safe way (In a location that's reliable & won't change)
DEFAULT_CSV_PATH = Path(app.root_path) / 'shopping.csv'

# Global state. 
# Model: Stores the trained model. 
# Metrics: Stores evaluation results. 
# CSV_Source: Where the data came from
MODEL_STATE = {
    'model': None,
    'metrics': None,
    'csv_source': None
}

def allowedFile(filename) -> bool:
    # Checking if the file is a CSV file
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Segment for the home page. Index function is associated with the root URL in Flask
@app.route('/', methods='GET')
def index():
    return render_template('index.html', metrics=MODEL_STATE['metrics'], csv_source=MODEL_STATE['csv_source'])

# The user Completes the training form, so this is ran
@app.route('/train', method='POST')
def train():
    choice = request.form.get('data_source')


    # For determining the CSV path
    csvPath = None
    tempPath = None

    try:
        if choice == 'default':
            csvPath = DEFAULT_CSV_PATH
            if not csv_path.exists():
                # Message for the user categorized as an error
                flash('Default CSV not found', 'error')
                return redirect(url_for('index'))

        elif choice == 'upload':
            if 'file' not in request.files:
                flash('No file part in the request.', 'error')
                return redirect(url_for('index'))
            
            file = request.files['file']
            if file.filename == '':
                flash('No file selected.', 'error')
                return redirect(url_for('index'))
            
            # File is valid
            if file and allowedFile(file.filename):
                filename = secure_filename(file.filename)
                tempPath = Path(app.config['UPLOAD_FOLDER']) / filename  # Append the filename to the upload folder
                file.save(tempPath)
                csvPath = tempPath
            else:
                flash('Invalid file type. Please upload .csv files only.', 'error')
                return redirect(url_for('index'))
            
        else:
            flash('Invalid file type. Please upload a .csv file.', 'error')
            return redirect(url_for('index'))
        
        # Load data from spreadsheet and split into train and test sets
        evidence, labels = load_data(str(csvPath))
        X_train, X_test, y_train, y_test = splitTrainTest(evidence, labels)

        model = train_model(X_train, y_train)
        predictions = model.predict(X_test)
        sensitivity, specificity = evaluate(y_test, predictions)

        

    except Exception as e:
        flash(f'Error during training: {e}')
    
    finally:
        # Removing the uploaded file from the temporary path after training
        if tempPath and Path(tempPath).exists():
            try:
                Path(tempPath).unlink()
            except Exception:
                pass
