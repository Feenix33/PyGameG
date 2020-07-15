"""
Initialization routines
        #'elev_clrs': {'shell':"#a8a7a7", 'outline':"#cc527a", 'carpet':"#e8175d ", 'c4':'#474747', 'c5':'#363636' }, 
"""

def get_constants():
    screen_width = 400
    screen_height = 250
    display_width = screen_width*2
    display_height = screen_height*2
    fps = 30


    constants = {
        'caption': "Shuttle Experiment",
        'screen_width': screen_width,
        'screen_height': screen_height,
        'display_width': display_width,
        'display_height': display_height,
        'fps': fps,

        'background_color': "skyblue",

    }
    return constants



