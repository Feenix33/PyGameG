"""
Initialization routines
        #'elev_clrs': {'shell':"#a8a7a7", 'outline':"#cc527a", 'carpet':"#e8175d ", 'c4':'#474747', 'c5':'#363636' }, 
"""

def get_constants():
    dim = 8 #tile dim
    world_width = 50
    world_height = 30
    screen_width = world_width * dim
    screen_height = world_height * dim
    display_width = screen_width*2
    display_height = screen_height*2
    fps = 30


    constants = {
        'caption': "Road ECS Experiment 04",
        'dim': dim,
        'world_width': world_width,
        'world_height': world_height,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'display_width': display_width,
        'display_height': display_height,
        'fps': fps,

        'background_color': "#c4d86f",
        'clr_background': "#c4d86f",
        'clr_truck': {'fill':"brown", 'outline':'white'},

    }
    return constants



