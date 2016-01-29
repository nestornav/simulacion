#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict, namedtuple

import numpy as np


ResponseRow = namedtuple(
    "ResponseRow",
    ["semana", "frenos_semana_rnd", "frenos_semana_reparar", "trabajos_atrasados_semana_anterior",
     "cantidad_trabajos_realizar_semana", "trabajos_sin_terminar_semana_acutal", "cantidad_trabajo_terciarizado"])

def numero_reparaciones(mean, std):
    return np.random.uniform(mean,std)

def numero_trabajos():    
    rnd = round(np.random.rand(),2)
    intervalos = {
        (0, 0.09): 5, (0.1, 0.35): 6, (0.36, 0.75): 7, (0.76, 0.95): 8, (0.96, 0.99): 9
    }

    for itv, trab in intervalos.items():
        if itv[0] <= rnd <= itv[1]:
            return rnd, trab

def simulate(numero_corridas, media_respuesta, desv_respuesta):
    trabajos_frenos_semana_rnd, trabajos_frenos_semana, trabajos_semana_anterior, trabajos_semana_actual = 0, 0, 0, 0    
    capacidad_trabajo, sobrante_semana, trabajo_terciarizado = 0, 0, 0
    respuestas = []
    #import ipdb;ipdb.set_trace()
    for iterations in xrange(numero_corridas):
        numero_trabajos_semana = numero_trabajos();
        if iterations == 0:            
            trabajos_semana_anterior = 0
            trabajos_frenos_semana_rnd, trabajos_frenos_semana = numero_trabajos_semana
            print(media_respuesta,desv_respuesta);
            capacidad_trabajo = numero_reparaciones(media_respuesta,desv_respuesta)

            sobrante = trabajos_frenos_semana - capacidad_trabajo
            if sobrante < 0:
                sobrante_semana = 0
            else:
                sobrante_semana = sobrante
            trabajo_terciarizado = 0        



        respuesta = ResponseRow(
                semana=iterations + 1, frenos_semana_rnd=trabajos_frenos_semana_rnd, frenos_semana_reparar=trabajos_frenos_semana,
                trabajos_atrasados_semana_anterior=trabajos_semana_anterior, cantidad_trabajos_realizar_semana=capacidad_trabajo,
                trabajos_sin_terminar_semana_acutal=sobrante_semana, cantidad_trabajo_terciarizado=trabajo_terciarizado)

        respuestas.append(respuesta)

    return respuestas

def to_ndarray(respuestas, key):
    return  np.array([getattr(r, key) for r in respuestas])

