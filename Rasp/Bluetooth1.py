#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:Bluetooth1.py
#Descripción		:Comunicación Bluetooth.
#Autor          	:Javier Campos Rojas
#Fecha            	:Setiembre-2017
#Versión         	:1.0
#Notas          	:
#==============================================================================

import os
import glob
import time
import RPi.GPIO as GPIO
from bluetooth import *

os.system('modprobe w1-gpio')
os.system('modprobe w1-term')

GPIO.setmode(GPIO.BCM)
GPIO.setuo(14, GPIO.OUT)

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(
