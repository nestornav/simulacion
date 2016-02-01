#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict, namedtuple

import numpy as np


ResponseRow = namedtuple(
    "ResponseRow",
    ["semana", "frenos_semana_rnd", "frenos_semana_reparar", "trabajos_atrasados_semana_anterior",
     "cantidad_trabajos_realizar_semana", "trabajos_sin_terminar_semana_acutal", "cantidad_trabajo_terciarizado",
        "tipo_politica", "cantidad_pactado_politica", "costo_politica", "costo_excedente"])

def numero_reparaciones(mean, std):
    return int(np.random.uniform(mean,std))

def numero_trabajos():    
    rnd = round(np.random.rand(),2)
    intervalos = {
        (0, 0.09): 5, (0.1, 0.35): 6, (0.36, 0.75): 7, (0.76, 0.95): 8, (0.96, 0.99): 9
    }

    rnd = rnd - 0.01 if rnd == 1 else rnd    
    for itv, trab in intervalos.items():
        if itv[0] <= rnd <= itv[1]:            
            return rnd, trab

def trabajos_politica_aleatoria():
    politica = [1, 2, 3, 4, 5]
    return np.random.choice(politica)

def get_trabajos_sin_cumplir(capacidad_trabajo, trabajos_semana_anterior, trabajos_frenos_semana):
    trabajo_a_terciarizar, trabajos_actual_pendientes = 0, 0    
    sobrante = trabajos_semana_anterior - capacidad_trabajo

    if sobrante > 0:
        trabajo_a_terciarizar = sobrante
        trabajos_actual_pendientes = trabajos_frenos_semana
    else:
        actuales = trabajos_frenos_semana + sobrante
        trabajos_actual_pendientes = 0 if actuales < 0 else actuales

    trabajos_semana = [trabajo_a_terciarizar,trabajos_actual_pendientes]
    return trabajos_semana

def get_costos(tipo_politica,trabajos_terciarizado, costo_fuera_pactado):    
    presupuesto_taller = {
        (0, 0): 1, (2, 500): 2, (4, 950): 3, (6, 1300): 4, (8, 1600): 5 
    }    
    #import ipdb;ipdb.set_trace()
    for ite, pol in presupuesto_taller.items():
        if pol == tipo_politica:            
            trabajo_excedente = ite[0] - trabajos_terciarizado
            costo_excedente = 0 if trabajo_excedente >= 0 else costo_fuera_pactado * (trabajo_excedente * -1)
            return ite[0], ite[1], costo_excedente

def simulate(numero_corridas, media_respuesta, desv_respuesta, tipo_politica):
    trabajos_frenos_semana_rnd, trabajos_frenos_semana, trabajos_semana_actual, capacidad_trabajo  = 0, 0, 0, 0    
    trabajos_semana_anterior, sobrante_semana, trabajo_terciarizado = 0, 0, 0
    politica_seleccionada, costo_pactado, costo_fuera_pactado, costo_total_fuera_pactado = tipo_politica, 0, 400, 0
    cantidad_reparar_taller_pactado = 0
    respuestas = []
   # import ipdb;ipdb.set_trace()
    for iterations in xrange(numero_corridas):      
        numero_trabajos_semana = numero_trabajos()
        
        if iterations == 0:            
            trabajos_semana_anterior = 0
            trabajos_frenos_semana_rnd, trabajos_frenos_semana = numero_trabajos_semana            
            capacidad_trabajo = numero_reparaciones(media_respuesta,desv_respuesta)

            sobrante = trabajos_frenos_semana - capacidad_trabajo
            if sobrante <= 0:
                sobrante_semana = 0
            else:
                sobrante_semana = sobrante
            trabajo_terciarizado = 0
        
        else:
            trabajos_semana_anterior = sobrante_semana
            trabajos_frenos_semana_rnd, trabajos_frenos_semana = numero_trabajos_semana
            capacidad_trabajo = numero_reparaciones(media_respuesta,desv_respuesta)

                        
            trabajo_terciarizado, sobrante_semana = get_trabajos_sin_cumplir(capacidad_trabajo,trabajos_semana_anterior,trabajos_frenos_semana)
            
            if tipo_politica == 6:  
                cantidad_reparar_taller_pactado = trabajos_semana_anterior
                trabajo_excedente = trabajos_semana_anterior - trabajo_terciarizado
                costo_total_fuera_pactado = 0 if trabajo_excedente >= 0 else costo_fuera_pactado * (trabajo_excedente * -1)                                
            
            elif tipo_politica == 7:            
                politica_rnd = trabajos_politica_aleatoria()
                tipo_politica = politica_rnd
                cantidad_reparar_taller_pactado, costo_pactado, costo_total_fuera_pactado = get_costos(politica_rnd, trabajo_terciarizado, costo_fuera_pactado)
            
            else:
                cantidad_reparar_taller_pactado, costo_pactado, costo_total_fuera_pactado = get_costos(tipo_politica, trabajo_terciarizado, costo_fuera_pactado)
            
        respuesta = ResponseRow(
                semana=iterations + 1, frenos_semana_rnd=trabajos_frenos_semana_rnd, frenos_semana_reparar=trabajos_frenos_semana,
                trabajos_atrasados_semana_anterior=trabajos_semana_anterior, cantidad_trabajos_realizar_semana=capacidad_trabajo,
                trabajos_sin_terminar_semana_acutal=sobrante_semana, cantidad_trabajo_terciarizado=trabajo_terciarizado, 
                tipo_politica=politica_seleccionada, cantidad_pactado_politica=cantidad_reparar_taller_pactado, 
                costo_politica=costo_pactado, costo_excedente=costo_total_fuera_pactado)

        respuestas.append(respuesta)

    return respuestas

def to_ndarray(respuestas, key):
    return  np.array([getattr(r, key) for r in respuestas])

