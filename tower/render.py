'''
render.py
'''

#import os
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
#import pygame as pg
from enum import Enum
from entity import Entity

class RenderOrder(Enum):
    BACKGROUND=1
    BUILDING=2
    FLOOR=3
    DOOR=5
    ELEVATOR=4


def render_system(screen, entities, background_color):
    screen.fill(background_color)
    entities_in_render_order = sorted(entities, key=lambda x: x.zorder.value)
    for entity in entities_in_render_order: 
        entity.draw(screen)

