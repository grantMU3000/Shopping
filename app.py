import os # For working with operating system (We're working with files)
from pathlib import Path  # For creating a path to my CSV file
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from shopping import load_data, train_model, evaluate, splitTrainTest

