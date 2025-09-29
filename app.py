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


