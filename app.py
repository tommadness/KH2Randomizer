from randomize import Randomize
from flask import Flask, session, Response
from locationClass import worlds
from randomCmdMenu import cmdMenusChoice
from configDict import miscConfig
import flask as fl
import numpy as np
import zipfile
import base64
import string
import random
import ast
import os

app = Flask(__name__)

expTypes = ["Sora","Valor","Wisdom","Limit","Master","Final"]
app.config['SECRET_KEY'] = 'ayylmao'


@app.route('/')
def index():
    resp = fl.make_response(fl.render_template('index.html', worlds = worlds, expTypes = expTypes, miscConfig = miscConfig))
    return resp



@app.route('/seed/<hash>')
def hashedSeed(hash):
    argList = str(base64.urlsafe_b64decode(hash)).replace('b"',"").replace('"',"").split(";")
    print(argList)
    for arg in argList:
        if not arg == "":
            kv = arg.split("=")
            if kv[1].startswith("{") or kv[1].startswith("["):
                session[kv[0]] = eval(kv[1])
            elif kv[1] == "True":
                session[kv[0]] = True
            elif kv[1] == "False":
                session[kv[0]] = False
            else:
                session[kv[0]] = kv[1]
    return seed()

@app.route('/seed',methods=['GET','POST'])
def seed():
    if fl.request.method == "POST":
        if int(fl.request.form.get('keybladeMaxStat')) < int(fl.request.form.get('keybladeMinStat')):
            return "Keyblade minimum stat larger than maximum stat."
        session['seed'] = fl.escape(fl.request.form.get("seed")) or ""
        if session['seed'] == "":
            characters = string.ascii_letters + string.digits

            session['seed'] = (''.join(random.choice(characters) for i in range(30)))

        session['includeList'] = fl.request.form.getlist("include") or []

        session['formExpMult'] = {
            1: float(fl.request.form.get("ValorExp")), 
            2: float(fl.request.form.get("WisdomExp")), 
            3: float(fl.request.form.get("LimitExp")), 
            4: float(fl.request.form.get("MasterExp")), 
            5: float(fl.request.form.get("FinalExp"))
            }

        session['soraExpMult'] = float(fl.request.form.get("SoraExp"))

        session['levelChoice'] = fl.request.form.get("levelChoice")

        session['spoilerLog'] = fl.request.form.get("spoilerLog") or False

        session['keybladeMaxStat'] = int(fl.request.form.get("keybladeMaxStat"))

        session['keybladeMinStat'] = int(fl.request.form.get("keybladeMinStat"))

        session['promiseCharm'] = bool(fl.request.form.get("PromiseCharm") or False)
        session['goMode'] = bool(fl.request.form.get("GoMode") or False)

    dumpStr = ""
    for key in session:
        dumpStr += "{key}={value};".format(key=key, value=session[key])
    hashStr = str(base64.urlsafe_b64encode(bytes(dumpStr.encode('utf-8')))).replace("b'","").replace("'","")

    print(session.get('spoilerLog'))

    return fl.render_template('seed.html',
    permaLink = fl.url_for("hashedSeed",hash=hashStr, _external=True), 
    cmdMenus = cmdMenusChoice, 
    levelChoice = session.get('levelChoice'), 
    include = session.get('includeList'), 
    seed = session.get('seed'), 
    worlds=worlds, 
    expTypes = expTypes, 
    formExpMult = session.get('formExpMult'), 
    soraExpMult = session.get('soraExpMult'),
    keybladeMinStat = session.get('keybladeMinStat'),
    keybladeMaxStat = session.get('keybladeMaxStat'),
    )
    
@app.route('/download')
def randomizePage():
    excludeList = list(set(worlds) - set(session.get('includeList')))
    cmdMenuChoice = fl.request.args.get("cmdMenuChoice")
    data = Randomize(
    seedName = fl.escape(session.get('seed')), 
    exclude = excludeList, 
    formExpMult = session.get('formExpMult'), 
    soraExpMult = float(session.get('soraExpMult')), 
    levelChoice = session.get('levelChoice'), 
    cmdMenuChoice = cmdMenuChoice,
    spoilerLog = session.get('spoilerLog'),
    promiseCharm = session.get('promiseCharm'),
    goMode = session.get('goMode'),
    keybladeMinStat = int(session.get('keybladeMinStat')),
    keybladeMaxStat = int(session.get('keybladeMaxStat')),
    )

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
    dataOut = Randomize(exclude=["LingeringWill","Level","FormLevel"], cmdMenuChoice="randAll")
    f = open("randoSeed.zip", "wb")
    f.write(dataOut.read())
    f.close()