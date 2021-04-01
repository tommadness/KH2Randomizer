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

if __name__ == '__main__':
    Randomize(exclude=[])