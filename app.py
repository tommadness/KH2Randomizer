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
    includeList = fl.request.args.get('include') or []
    excludeList = list(np.setdiff1d(includeList,worlds))
    seed = fl.request.args.get('seed')
    data = Randomize(seedName = fl.escape(seed), exclude = excludeList, formExpMult={1:5,2:3,3:3,4:3,5:3})
    return fl.send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='randoseed.zip'
    )
    
Randomize(exclude = ["ExcludeFrom50","Atlantica","DataOrg","LingeringWill"], formExpMult={1:5,2:3,3:3,4:3,5:3})