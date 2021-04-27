from flask import Flask, session, Response
from Module.randomCmdMenu import RandomCmdMenu
from Module.randomBGM import RandomBGM
from Module.startingInventory import StartingInventory
from List.configDict import miscConfig, locationType, expTypes, keybladeAbilities
import flask as fl
import numpy as np
from urllib.parse import urlparse
import os, base64, string, random, ast, zipfile, redis, json, asyncio
from khbr.randomizer import Randomizer as khbr
from Module.hints import Hints
from Module.randomize import KH2Randomizer

app = Flask(__name__, static_url_path='/static')

url = urlparse(os.environ.get("REDIS_TLS_URL"))
r = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

@app.route('/', methods=['GET','POST'])
def index(message=""):
    session.clear()
    return fl.render_template('index.jinja', locations = locationType, expTypes = expTypes, miscConfig = miscConfig, keybladeAbilities = keybladeAbilities, message=message, bossEnemyConfig = khbr()._get_game(game="kh2").get_options(), hintSystems = Hints.getOptions(), startingInventory = StartingInventory.getOptions())



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
        session['bossEnemy'] = bool(fl.request.form.get("bossEnemy") or False)
        enemyOptions = {
            "boss": fl.request.form.get("boss"),
            "nightmare_bosses": bool(fl.request.form.get("nightmare_bosses")),
            "selected_boss": None if fl.request.form.get("selected_boss") == "None" else fl.request.form.get("selected_boss"),
            "enemy": fl.request.form.get("enemy"),
            "selected_enemy": None if fl.request.form.get("selected_enemy") == "None" else fl.request.form.get("selected_enemy"),
            "nightmare_enemies": bool(fl.request.form.get("nightmare_enemies"))
        }
        session['enemyOptions'] = json.dumps(enemyOptions)

        session['hintsType'] = fl.request.form.get("hintsType")

        session['startingInventory'] = fl.request.form.getlist("startingInventory")



        session['permaLink'] = ''.join(random.choice(string.ascii_uppercase) for i in range(8))
        with r.pipeline() as pipe:
            for key in session.keys():
                pipe.hmset(session['permaLink'], {key.encode('utf-8'): json.dumps(session.get(key)).encode('utf-8')})
            pipe.execute()

    return fl.render_template('seed.jinja',
    spoilerLog = session.get('spoilerLog'),
    permaLink = fl.url_for("hashedSeed",hash=session['permaLink'], _external=True), 
    cmdMenus = RandomCmdMenu.getOptions(),
    bgmOptions = RandomBGM.getOptions(), 
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
    enemyOptions = json.loads(session.get("enemyOptions")),
    hintsType = session.get("hintsType"),
    startingInventory = session.get("startingInventory"),
    idConverter = StartingInventory.getIdConverter()
    )
    
@app.route('/download')
def randomizePage():
    platform = fl.request.args.get("platform")
    excludeList = list(set(locationType) - set(session.get('includeList')))
    excludeList.append(session.get("levelChoice"))
    cmdMenuChoice = fl.request.args.get("cmdMenuChoice")
    randomBGM = fl.request.args.get("randomBGM")

    randomizer = KH2Randomizer(seedName = session.get("seed"))
    randomizer.populateLocations(excludeList)
    randomizer.populateItems(promiseCharm = session.get("promiseCharm"), startingInventory = session.get("startingInventory"))
    if randomizer.validateCount():
        randomizer.setKeybladeAbilities(
            keybladeAbilities = session.get("keybladeAbilities"), 
            keybladeMinStat = int(session.get("keybladeMinStat")), 
            keybladeMaxStat = int(session.get("keybladeMaxStat"))
        )
        randomizer.setRewards(levelChoice = session.get("levelChoice"))
        randomizer.setLevels(session.get("soraExpMult"), formExpMult = session.get("formExpMult"))
        randomizer.setBonusStats()
        try:
            zip = randomizer.generateZip(randomBGM = randomBGM, platform = platform, startingInventory = session.get("startingInventory"), hintsType = session.get("hintsType"), cmdMenuChoice = cmdMenuChoice, spoilerLog = bool(session.get("spoilerLog")), enemyOptions = json.loads(session.get("enemyOptions")))
            return fl.send_file(
                zip,
                mimetype='application/zip',
                as_attachment=True,
                attachment_filename='randoseed.zip'
            )
        except ValueError as err:
            print("ERROR: ", err.args)

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
    randomizer = KH2Randomizer("fdh6h34q6h4q6g62g6h6w46hw464vbvherby39")
    randomizer.populateLocations([locationType.LoD, "ExcludeFrom50"])
    randomizer.populateItems(startingInventory=["138","537","369"])
    if randomizer.validateCount():
        randomizer.setKeybladeAbilities()
        randomizer.setRewards()
        randomizer.setLevels(soraExpMult = 1.5, formExpMult = {'1':6, '2':3, '3':3, '4':3, '5':3})
        randomizer.setBonusStats()
        zip = randomizer.generateZip(hintsType="JSmartee").getbuffer()
        open("randoSeed.zip", "wb").write(zip)