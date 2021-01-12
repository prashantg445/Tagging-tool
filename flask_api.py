import os
import json
import glob
import urllib.request
from flask import Flask, flash, request, redirect, render_template, jsonify, url_for
from werkzeug.utils import secure_filename
from datetime import *
import pandas as pd

app = Flask(__name__)

all_cases = sorted(glob.glob('static/detections/*'))
output_path = 'output_'+ datetime.now().strftime("%Y-%m-%d_%H:%M")+'.csv'
with open(output_path, 'w') as f:
    f.write('filepath,status\n')
    for each in all_cases:
        f.write(each+',Incorrect\n')

output = pd.read_csv(output_path)

@app.route('/display_case/<ix>')
def display_case(ix):
    global all_cases
    global output
    ix = int(ix)
    if ix<0 or ix>len(all_cases)-1:
        return 'Please correct the url as you reached out of the indices !!'

    case_folder = all_cases[ix]
    json_path = os.path.join(case_folder, 'result.json')
    with open(json_path) as f:
        resp = json.load(f)
        # making it prettier
        resp = json.dumps(resp, indent=4, sort_keys=False)

    pages = glob.glob(os.path.join(case_folder, '*.jpeg'))
    # removing static from the image path
    pages = [page.split('static/')[1] for page in pages]
    status = output.iloc[ix]['status']
    print(status)
    return render_template('tagger.html', image_path = pages[0], response_json = resp, current_ix=ix, status=status, total_cases = len(all_cases))

@app.route('/getStatus/<ix>', methods=['POST'])
def getStatus(ix):
    global output
    ix = int(ix)
    output.iloc[ix]['status'] = request.form['status']
    output.to_csv(output_path, index=False)
    next_ix = min( ix+1, len(all_cases)-1)
    print(request.form['status'], next_ix)
    return redirect( url_for('display_case',ix=str(next_ix)) )


@app.route('/')
def tool():
    return display_case(0)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)