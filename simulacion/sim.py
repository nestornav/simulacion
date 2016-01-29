#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict, namedtuple

import numpy as np


ResponseRow = namedtuple(
    "ResponseRow",
    ["iteracion", "frenos_semana_rnd", "cantidad_frenos_semana_reparar", "trabajos_atrasados_semana_anterior",
    "trabajos_realizar_semana_rnd", "cantidad_trabajos_realizar_semana", "trabajos_sin_terminar_acutal",
    "cantidad_trabajo_terciarizado"])



def numero_reparaciones(mean, std):
    return np.random.uniform(mean,std)


def simulate(numero_corridas, media_respuesta, desv_respuesta, media_consulta):

    respuestas = []
    #import ipdb;ipdb.set_trace()
    for iterations in xrange(numero_corridas):
        

    return respuestas


def to_ndarray(respuestas, key):
    return  np.array([getattr(r, key) for r in respuestas])

