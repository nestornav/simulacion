#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# IMPORTS
# =============================================================================

from collections import Counter

from flask import Flask, render_template, request
from flask.ext.script import Manager, Server
from flask_bootstrap import Bootstrap

import pygal

from . import sim

# =============================================================================
# CONF
# =============================================================================

app = Flask(__name__)
cli_manager = Manager(app)
cli_manager.add_command("runserver", Server(use_reloader=True))

Bootstrap(app)

dmedia_respuesta = 3
ddesv_respuesta = 7
dnumero_semanas = 100


# =============================================================================
# ROUTES
# =============================================================================

@app.route("/")
def index():
    return render_template(
        'index.html', media_respuesta=dmedia_respuesta,
        desv_respuesta=ddesv_respuesta, numero_semanas=dnumero_semanas)


@app.route("/run_simulation",methods=["POST"])
def run_simulation():
    media_respuesta = float(request.form["media_respuesta"])
    desv_respuesta = float(request.form["desv_respuesta"])    
    numero_semanas = int(request.form["numero_semanas"])

    resultados = sim.simulate(numero_semanas, media_respuesta, desv_respuesta)

    return render_template('index.html', resultados=resultados, media_respuesta=media_respuesta,
        desv_respuesta=desv_respuesta, numero_semanas=numero_semanas)
