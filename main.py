from randomize import Randomize
from flask import Flask
import flask as fl

app = Flask(__name__)

@app.route('/')
def index():
    data = Randomize(exclude = ["ExcludeFrom50","Atlantica","DataOrg","LingeringWill"], formExpMult={1:5,2:3,3:3,4:3,5:3})
    return fl.send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='randoseed.zip'
    )
    
Randomize(exclude = ["ExcludeFrom50","Atlantica","DataOrg","LingeringWill"], formExpMult={1:5,2:3,3:3,4:3,5:3})