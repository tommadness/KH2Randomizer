from randomize import Randomize
from flask import Flask, session, Response
from randomCmdMenu import cmdMenusChoice
from configDict import miscConfig, locationType, expTypes, keybladeAbilities
import flask as fl
import numpy as np
from urllib.parse import urlparse
import os, base64, string, random, ast, zipfile, redis, json

app = Flask(__name__)

url = urlparse(os.environ.get("REDIS_TLS_URL"))
r = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

@app.route('/', methods=['GET','POST'])
def index(message=""):
    session.clear()
    return fl.render_template('index.jinja', locations = locationType, expTypes = expTypes, miscConfig = miscConfig, keybladeAbilities = keybladeAbilities, message=message)



@app.route('/seed/<hash>')
def hashedSeed(hash):
    session.clear()
    sessionVars = r.hgetall(hash)
    for var in sessionVars:
        session[str(var, 'utf-8')] = json.loads(sessionVars[var])
    
    includeList = session['includeList'][:]
    session['includeList'].clear()

    for location in includeList:
        session['includeList'].append(locationType(location))

    print(session)
    return seed()

@app.route('/seed',methods=['GET','POST'])
def seed():
    if fl.request.method == "POST":
        session['keybladeAbilities'] = fl.request.form.getlist('keybladeAbilities')

        if session['keybladeAbilities'] == []:
            return fl.redirect(fl.url_for("index", message="Please select at least one keyblade ability type."), code=307)

        if int(fl.request.form.get('keybladeMaxStat')) < int(fl.request.form.get('keybladeMinStat')):
            return fl.redirect(fl.url_for("index", message="Keyblade minimum stat larger than maximum stat."), code=307)
        session['seed'] = fl.escape(fl.request.form.get("seed")) or ""
        if session['seed'] == "":
            characters = string.ascii_letters + string.digits

            session['seed'] = (''.join(random.choice(characters) for i in range(30)))

        includeList = fl.request.form.getlist('include') or []

        session['includeList'] = [locationType[location.replace("locationType.","")] for location in includeList]


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



        session['permaLink'] = ''.join(random.choice(string.ascii_uppercase) for i in range(8))
        with r.pipeline() as pipe:
            for key in session.keys():
                pipe.hmset(session['permaLink'], {key.encode('utf-8'): json.dumps(session.get(key)).encode('utf-8')})
            pipe.execute()

    return fl.render_template('seed.jinja',
    spoilerLog = session.get('spoilerLog'),
    permaLink = fl.url_for("hashedSeed",hash=session['permaLink'], _external=True), 
    cmdMenus = cmdMenusChoice, 
    levelChoice = session.get('levelChoice'), 
    include = session.get('includeList'), 
    seed = session.get('seed'), 
    worlds=locationType, 
    expTypes = expTypes, 
    formExpMult = session.get('formExpMult'), 
    soraExpMult = session.get('soraExpMult'),
    keybladeMinStat = session.get('keybladeMinStat'),
    keybladeMaxStat = session.get('keybladeMaxStat'),
    keybladeAbilities = session.get('keybladeAbilities'),
    )
    
@app.route('/download')
def randomizePage():
    excludeList = list(set(locationType) - set(session.get('includeList')))
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
    keybladeAbilities = session.get('keybladeAbilities'),
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
    dataOut = Randomize(exclude=[], cmdMenuChoice="randAll")
    f = open("randoSeed.zip", "wb")
    f.write(dataOut.read())
    f.close()