import os
import json
import glob
import urllib.request
from flask import Flask, flash, request, redirect, render_template, jsonify, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

all_cases = sorted(glob.glob('static/detections/*'))
all_statuses = ['Incorrect']*len(all_cases)

@app.route('/display_case/<ix>')
def display_case(ix):
    global all_cases
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
    return render_template('tagger.html', image_path = pages[0], response_json = resp, current_ix=ix, total_cases = len(all_cases))

@app.route('/status/<ix>', methods=['POST'])
def status(ix):
    all_statuses[int(ix)] = request.form['status']
    next_ix = min( int(ix)+1, len(all_cases)-1)
    print(request.form['status'], next_ix)
    return redirect( url_for('display_case',ix=str(next_ix)) )


@app.route('/')
def tool():
    return display_case(0)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)