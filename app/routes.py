from flask import Blueprint, render_template
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
def index():
    try:
        df = pd.read_csv("logs_dataset/logs_summary.csv")
        logs = df.to_dict(orient='records')
    except Exception as e:
        logs = []
    return render_template("index.html", logs=logs)
