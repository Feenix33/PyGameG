"""
Initialization routines

TODO:

        elevator a8a7a7 cc527a e8175d 474747 363636
        #A7226E   #EC2049   #F26B38   #F7DB4F   #2F9599
        #E1F5C4   #EDE574   #F9D423   #FC913A   #FF4E50
        #E5FCC2   #9DE0AD   #45ADA8   #547980   #594F4F
        #FE4365   #FC9D9A   #F9CDAD   #C8C8A9   #83AF9B
"""

def get_constants():
    screen_width = 200
    screen_height = 400
    display_width = screen_width*2
    display_height = screen_height*2
    fps = 30


    constants = {
        'caption': "Tower 03",
        'screen_width': screen_width,
        'screen_height': screen_height,
        'display_width': display_width,
        'display_height': display_height,
        'fps': fps,

        'background_color': "skyblue",

        'bldg_xy': (10, 330),
        'bldg_wh': (180, 50),
        'bldg_clrs': ["darkgrey", "grey", "black"],
        'bldg2_clrs': {'a':"darkgrey", 'b':"grey", 'c':"black"},

        'floor_w': 140,
        'floor_h': 40,
        'floor_wh': (140, 40),
        'floor_x': 45,
        'floor2_clrs': {'wall':'lightyellow',
            'carpet':'lightgoldenrod',
            'outline': 'black',
            },
        'floor_clrs': {'res': {'wall':'#a8e6ce', 'carpet':'#dcedc2', 'obj1':'#ffd3B5', 'obj2':'#ffaaa6', 'obj3':'#ff8c94'},
                       'com': {'wall':'#cc3300', 'carpet':'#ff9966', 'obj1':'#ffcc00', 'obj2':'#99cc33', 'obj3':'#339900'},
                       },
        'carpet_h': 4, # carpet height
        'floor_carpet_off': 8, # offset for top of meeple

        'elev_x': 15,
        'elev_xy': (15, 330-40),
        'elev_wh': (30, 40),
        'elev_carpet': 4,
        'elev_clrs': {'shell':"#0081A7", 'outline':"#00AFB9", 'carpet':"#FDFCDC", 'c4':'#FED9B7', 'c5':'#F07167' },
        'elev_tclose': 20,
        'elev_topen': 40,
        'elev_tload': 33,

        'door_x': 15,
        'door_xy': (15, 330-40),
        'door_wh': (30, 40),
        'door_carpet': 4,
        'door_clrs': {'shell':"#0081A7", 'outline':"#00AFB9", 'carpet':"#FDFCDC", 'c4':'#FED9B7', 'c5':'#F07167' },

        'meep_hair':  ["#03071e","#370617","#6a040f","#9d0208","#d00000","#dc2f02","#e85d04","#f48c06","#faa307","#ffba08", "#ffd9da","#ea638c","#89023e","#30343f","#1b2021"],
        'meep_face':  ['#ffcdb2','#ffb4a2','#e5989b','#b5838d','#6d6875'],
        'meep_shirt': ["#14281d","#355834","#6e633d","#c2a878","#f1f5f2"],
        'meep_jeans': ["#d9f0ff","#a3d5ff","#83c9f4","#6f73d2","#7681b3"],
        'meep_h':24,
        'meep_hhair': 4,
        'meep_hface': 5,
        'meep_hshirt': 8,
        'meep_w':10,


    }
    return constants

        #'elev_clrs': {'shell':"#a8a7a7", 'outline':"#cc527a", 'carpet':"#e8175d ", 'c4':'#474747', 'c5':'#363636' }, 


