"""
Initialization routines
        #'elev_clrs': {'shell':"#a8a7a7", 'outline':"#cc527a", 'carpet':"#e8175d ", 'c4':'#474747', 'c5':'#363636' }, 
"""

def get_constants():
    dim = 40 #tile dim
    world_width = 20
    world_height = 10
    screen_width = world_width * dim
    screen_height = world_height * dim
    use_double = False
    mult = 2 if use_double else 1
    display_width = screen_width*mult
    display_height = screen_height*mult
    fps = 20 # 30


    constants = {
        'caption': "Flow Field Demo",
        'dim': dim,
        'world_width': world_width,
        'world_height': world_height,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'display_width': display_width,
        'display_height': display_height,
        'use_double': use_double,
        'fps': fps,

        'background_color': "#ff0000",
        'clr_background': "navyblue",
        'clr_world': {},
        'clr_world_background': "navyblue",
        'clr_world_grid': "#aaaaaa",
        'clr_world_goal': "pink",
        'clr_world_source': "plum",
    }
    #constants['clr_world'] = ["#ffadad","#ffd6a5","#fdffb6","#caffbf","#9bf6ff","#a0c4ff","#bdb2ff","#ffc6ff","#fffffc"]
    constants['clr_world'] = [ "#000000", "#493c2b", "#be2633", "#e06f8b", "#9d9d9d", "#a46422", "#eb8931", "#f7e26b",
                                "#ffffff", "#1b2632", "#2f484e", "#44891a", "#a3ce27", "#005784", "#31a2f2", "#b2dcef"]
    #print (len( constants['clr_world']))
    return constants



