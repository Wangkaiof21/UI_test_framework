import os
import json

WAIT_TIME = "time_scale"
TYPE = "type"
DIALOG_TYPE = "dialog_type"
action_line = [{'dialog_type': '', 'type': 'add_scene', 'time_scale': ''},
               {'dialog_type': '', 'type': 'object_scene_move', 'time_scale': ''},
               {'dialog_type': '', 'type': 'play_sound', 'time_scale': ''},
               {'dialog_type': 'ccccccccccccccc', 'type': 'role_set_position', 'time_scale': 1000},
               {'dialog_type': '', 'type': 'lens_move', 'time_scale': ''},
               {'dialog_type': '', 'type': 'animation_role', 'time_scale': 1000},
               {'dialog_type': '', 'type': 'role_set_position', 'time_scale': 1500},
               {'dialog_type': '+++++++', 'type': 'animation_role', 'time_scale': 1000},
               {'dialog_type': '', 'type': 'play_sound', 'time_scale': 87568}]

dd = dict()
wtm = 0
ty = ""
dty = ""
new_action_line = dict()
for line in action_line:
    if not line.get(TYPE):
        ty = ty
    else:
        ty += line.get(TYPE) + ","
    if not line.get(WAIT_TIME):
        dty = dty
    else:
        wtm += line.get(WAIT_TIME)
    if not line.get(DIALOG_TYPE):
        wtm = wtm
    else:
        dty += line.get(DIALOG_TYPE) + ","

print(ty)
print(dty)
print(wtm)
