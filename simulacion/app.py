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
dnumero_politica = 1


# =============================================================================
# ROUTES
# =============================================================================

@app.route("/")
def index():
    return render_template(
        'index.html', media_respuesta=dmedia_respuesta,
        desv_respuesta=ddesv_respuesta, numero_semanas=dnumero_semanas, numero_politica=dnumero_politica)


@app.route("/run_simulation",methods=["POST"])
def run_simulation():
    media_respuesta = int(request.form["media_respuesta"])
    desv_respuesta = int(request.form["desv_respuesta"])    
    numero_semanas = int(request.form["numero_semanas"])
    numero_politica = int(request.form["numero_politica"])

    resultados = sim.simulate(numero_semanas, media_respuesta, desv_respuesta, numero_politica)    
    costo_excedente = sim.to_ndarray(resultados,"costo_excedente")

    stats = {
        "promedio_costo_excedente" : costo_excedente.mean(),
        "promedio_costo_anual_excedentes": float((costo_excedente.sum() * 52) / len(costo_excedente)),
        "promedio_capacidad_trabajo" : sim.to_ndarray(resultados,"cantidad_trabajos_realizar_semana").mean(),
        "promedio_trabajos_terciarizados" : sim.to_ndarray(resultados,"cantidad_trabajo_terciarizado").mean(),
        "cantidad_trabajos_terciarizados" : sim.to_ndarray(resultados,"cantidad_trabajo_terciarizado").sum()
    }

    return render_template('index.html', resultados=resultados, media_respuesta=media_respuesta,
        desv_respuesta=desv_respuesta, numero_semanas=numero_semanas, numero_politica=numero_politica, stats=stats)
