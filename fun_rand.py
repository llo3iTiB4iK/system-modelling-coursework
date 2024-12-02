import math
import random


def exp(time_mean):
    a = 0
    while a == 0:
        a = random.random()
    a = -time_mean * math.log(a)
    return a


def unif(time_min, time_max):
    a = random.random()
    a = time_min + a * (time_max - time_min)
    return a


def norm(time_mean, time_deviation):
    a = random.gauss(time_mean, time_deviation)
    return a
