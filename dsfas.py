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
wtm = 0
ty = ""
dty = ""
new_action_line = dict()
# for line in action_line:
# ty += "" if not line.get("type") else ty += line.get("type") + ","
# ty = ty + '' if not line.get("type") else ty + ","

# if not line.get("type"):
#     ty += ""
# else:
#     ty += line.get("type") + ","
#
# if not line.get("time_scale"):
#     wtm += 0
# else:
#     wtm += line.get("time_scale")
# if not line.get("dialog_type"):
#     dty += ""
# else:
#     dty += line.get("dialog_type") + ","


a = [i["dialog_type"] for i in action_line if i["dialog_type"]]
new_action_line["dialog_type"] = ','.join(a)

a = [i["type"] for i in action_line if i["type"]]
new_action_line["type"] = ','.join(a)

a = [i["time_scale"] for i in action_line if i["time_scale"]]
new_action_line["time_scale"] = sum(a)

# print(new_action_line)
index = 0
while index < 5:
    print(1111)
    index += 1
