"""
Initialization routines
        #'elev_clrs': {'shell':"#a8a7a7", 'outline':"#cc527a", 'carpet':"#e8175d ", 'c4':'#474747', 'c5':'#363636' }, 
"""

def get_constants():
    dim = 50 #tile dim
    world_width = 25
    world_height = 10
    screen_width = world_width * dim
    screen_height = world_height * dim
    use_double = False
    mult = 2 if use_double else 1
    display_width = screen_width*mult
    display_height = screen_height*mult
    fps = 20 # 30

               #1...5....01...5....01...5....01...5....01...5....0
    world_str= '....#....................' \
               '....#..........#.........' \
               '....#..........#.........' \
               '....#..........#.........' \
               '....#..........#.........' \
               '...............#.........' \
               '...............#.........' \
               '...............#.........' \
               '......#........#.........' \
               '.........................' \


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

        'world_str': world_str,

        'clr_world': {'background': "#3d348b", 'wall':"#7678ed", \
                'grid':"#f7b801","goal":"#f18701",'emit':"#f35b04"},

        'clr_bugs': ["#007f5f","#2b9348","#55a630","#80b918","#aacc00","#bfd200","#d4d700","#dddf00","#eeef20","#ffff3f"],
    }
    return constants
