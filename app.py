from randomize import Randomize
from flask import Flask
import flask as fl
import numpy as np

app = Flask(__name__)

worlds = ["LoD","BC","LingeringWill","DataOrg","Level","FormLevel"]

@app.route('/')
def index():
    return fl.render_template('index.html', worlds = worlds)


@app.route('/download')
def randomizePage():
    includeList = fl.request.args.getlist("include") or []
    excludeList = list(set(worlds) - set(includeList))
    print(includeList)
    print(excludeList)
    seed = fl.request.args.get('seed') or ""
    print(seed)
    data = Randomize(seedName = fl.escape(seed), exclude = excludeList, formExpMult={1:5,2:3,3:3,4:3,5:3})
    if isinstance(data,str):
        return data

    return fl.send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='randoseed.zip'
    )

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
    
if __name__ == '__main__':
    Randomize(exclude=[])