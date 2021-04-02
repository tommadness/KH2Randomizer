from randomize import Randomize
from flask import Flask
from locationClass import worlds
import flask as fl
import numpy as np
import base64
import string
import random

app = Flask(__name__)

expTypes = ["Sora","Valor","Wisdom","Limit","Master","Final"]

@app.route('/')
def index():
    return fl.render_template('index.html', worlds = worlds, expTypes = expTypes)


@app.route('/seed/<hash>')
def hashedSeed(hash):
    argsString = base64.urlsafe_b64decode(hash)
    
    return fl.redirect("/seed?"+str(argsString).replace("b'","").replace("'",""))

@app.route('/seed')
def seed():
    includeList = fl.request.args.getlist("include") or []
    seed = fl.escape(fl.request.args.get("seed")) or ""
    if seed == "":
        characters = string.ascii_letters + string.digits
        seed = (''.join(random.choice(characters) for i in range(30)))
        return fl.redirect("/seed?seed="+seed+"&"+str(fl.request.query_string).replace("seed=&","").replace("b'","").replace("'",""))
    queryString = fl.request.query_string
    formExpMult = {1: fl.request.args.get("ValorExp"), 2: fl.request.args.get("WisdomExp"), 3: fl.request.args.get("LimitExp"), 4: fl.request.args.get("MasterExp"), 5: fl.request.args.get("FinalExp")}
    soraExpMult = fl.request.args.get("SoraExp")
    hashedString = base64.urlsafe_b64encode(queryString)

    permaLink = fl.url_for('hashedSeed', hash = hashedString,_external=True)
    return fl.render_template('seed.html', permaLink = permaLink.replace("'",""), include = includeList, seed = seed, worlds=worlds, expTypes = expTypes, formExpMult = formExpMult, soraExpMult = soraExpMult)

@app.route('/download')
def randomizePage():
    includeList = fl.request.args.getlist("include") or []
    excludeList = list(set(worlds) - set(includeList))
    seed = fl.request.args.get('seed') or ""
    print(seed)
    formExpMult = {1: int(fl.request.args.get("ValorExp")), 2: int(fl.request.args.get("WisdomExp")), 3: int(fl.request.args.get("LimitExp")), 4: int(fl.request.args.get("MasterExp")), 5: int(fl.request.args.get("FinalExp"))}
    soraExpMult = int(fl.request.args.get("soraExpMult"))
    data = Randomize(seedName = fl.escape(seed), exclude = excludeList, formExpMult=formExpMult, soraExpMult=soraExpMult)
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
    Randomize(exclude=["LingeringWill","Level","FormLevel"])