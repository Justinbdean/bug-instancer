import random
import maya.cmds as cmds
import maya.OpenMaya as om
from functools import partial 

def selection_true():
    bug = cmds.ls(sl=True)[0]
    if bug:
        return bug 
    else:
        om.MGlobal.displayWarning("No object was selected. ")
              
def copy_animation(bug, copy):
    cmds.copyKey(bug, animation = "objects", option = "keys")
    bug_with_animation = cmds.pasteKey(copy, animation = "objects", option = "replaceCompletely")
    return bug_with_animation

x= 0
y= 0
z = 0

randomx = []
randomy = []
randomz = []

x_flag = False
def getX(zone_x, zone_y):
    x_flag = False
    while x_flag == False:
        print("in x loop")
        print(randomx)
        x = random.randint(zone_x, zone_y)
        fx = x + 5
        bx = x - 6
        distance = [bx, fx]
        if len(randomx) == 0:
            randomx.append(distance)
            x_flag = True
            return x
        else:
            for i in randomx:
                a = i[0]
                b = i[1]
                if x in range(a,b):
                    break 
                else:
                    randomx.append(distance)
                    x_flag = True
                    return x
                break

y_flag = False
def getY(zone_x, zone_y):
    y_flag = False
    while y_flag == False:
        y = random.randint(zone_x, zone_y)
        fx = y + 5
        bx = y - 5
        distance = [bx, fx]
        if len(randomy) == 0:
            randomy.append(distance)
            y_flag = True
            return y
        else:
            for i in randomy:
                a = i[0]
                b = i[1]
                if x in range(a,b):
                    break 
                else:
                    randomx.append(distance)
                    y_flag = True
                    return y
                break

z_flag = False
def getZ(zone_x, zone_y):
    z_flag = False
    while z_flag == False:
        print("In Z Loop")
        print(randomz)
        z = random.randint(zone_x, zone_y)
        rz = z + 8
        lz = z - 8
        distance = [lz, rz]
        if len(randomz) == 0:
            randomz.append(distance)
            z_flag = True
            return z
        else:
            for i in randomz:
                a = i[0]
                b = i[1]
                if x in range(a,b):
                    break 
                else:
                    randomz.append(distance)
                    z_flag = True
                    return z
                break           

def bug_multiplier(shape, rows, columns, num_bugs, x, y, *args):
    
    shape = cmds.optionMenu(shape, q = True, value=True)
    rows = cmds.intField(rows, q = True, value=True)
    columns = cmds.intField(columns, q = True, value=True)
    num_bugs = cmds.intField(num_bugs, q = True, value=True)
    regionx = cmds.intField(x, q= True, value=True)
    regiony = cmds.intField(y, q= True, value=True)
    
    x = 0
    y = 0
    z = 0
     
    bug = selection_true()
    
    if bug:
        if shape == "Square":
            group = cmds.group(empty = True, name = "Bug_Square_Instances" + '_grp#')
            for i in range(rows):
                for i in range(columns):
                    x += 7
                    instance = cmds.instance(bug, name = bug + '_instnace#')
                    cmds.parent(instance, group)
                    cmds.move(x,y,z, instance)                        
                z += 10
                x =0

        elif shape == "Line":
            group = cmds.group(empty = True, name = "Bug_Line_Instances" + '_grp#')
            for i in range(num_bugs):
                x += 7
                instance = cmds.instance(bug, name = bug + '_instance#')
                cmds.parent(instance, group)
                cmds.move(x,y,z, instance)
                
        elif shape == "Random":
            group = cmds.group(empty = True, name = "Bug_Random_Instances" + '_grp#')
            for i in range(num_bugs):
                x = getX(regionx, regiony)
                print(x)
                #y= getY(0, 50)
                z = getZ(regionx, regiony)
                print(z)
                instance = cmds.instance(bug, name = bug + '_instance#')
                cmds.parent(instance, group)
                cmds.move(x,y,z, instance)

        elif shape == "Test":
            x = random.randint(-10, 10)
            z = random.randint(-10, 10)
            bug2 = cmds.duplicate(bug, rr = True, un = True, name = "Bug" + '_duplicate#')
            bug2superMoverName = bug2[0] 
            print(bug2superMoverName)
            bug2_superMover = cmds.select(bug2superMoverName + "|Invader_Skeleton_Rig|SuperMover_cc")
            cmds.move(x,y,z, bug2_superMover)
            
            list_items = cmds.listRelatives(bug2, ad = True, f = True)
            print(list_items)
            
            for i in list_items:
                if cmds.keyframe(i, q= True, keyframeCount = True) > 1:
                    print(i + " Has Frame")
                    startTime = cmds.playbackOptions(query = True, minTime = True)
                    endTime = cmds.playbackOptions(query = True, maxTime = True)
                    obj = i
                    cmds.cutKey(obj, time = (startTime, endTime), attribute = "translate X")
                    #cmds.setKeyframe(obj, time = (10), attribute = "translate X", value = 0)
                else:
                    pass
            
            group = cmds.group(empty = True, name = "Bug_Individual_Instances" + '_grp#')
            #cmds.selectKey(bug2)
            instance = cmds.instance(bug2, name = bug + '_instance#')
            cmds.parent(instance, group)
            cmds.move(x,y,z, instance)
                
def create_ui():
    window = cmds.window(title= "THE BUG MULTIPLIER", width = 500)
    layout = cmds.formLayout()
    
    shape_type = cmds.optionMenu(label = "Shape Type:", parent = layout)
    cmds.menuItem(label = "Square")
    cmds.menuItem(label = "Line")
    cmds.menuItem(label = "Random")
    cmds.menuItem(label = "Test")
    
    row_count_label = cmds.text(label = "If Sqaure- Rows:", parent = layout)
    row_count_field = cmds.intField(value = 0, minValue = 0, parent = layout)
    
    columns_count_label = cmds.text(label = "If Sqaure- Columns:", parent = layout)
    columns_count_field = cmds.intField(value = 0, minValue = 0, parent = layout)
    
    num_of_bugs_label = cmds.text(label = "If Line or Random- Number of Bugs:", parent = layout)
    num_of_bugs_field = cmds.intField(value = 0, minValue = 0, parent = layout)
    
    randomx_zone_label = cmds.text(label = "If Random- Minimum random value:", parent = layout)
    randomx_zone_field = cmds.intField(value = 0, parent = layout)
    
    randomy_zone_label = cmds.text(label = "If Random- Maximum random value:", parent = layout)
    randomy_zone_field = cmds.intField(value = 0, parent = layout)
    

    create_button = cmds.button(label = "CREATE BUGS!!", 
                                parent = layout, command = partial(bug_multiplier, 
                                shape_type, row_count_field, columns_count_field, 
                                num_of_bugs_field, randomx_zone_field, randomy_zone_field))
                                                    
    cmds.formLayout(layout,
                    e=True,
                    af=[(shape_type, "left", 4), (shape_type, "top", 4)])
    cmds.formLayout(layout,
                    e=True,
                    af=[(row_count_label, "left", 4)],
                    ac=[(row_count_label, "top", 14, shape_type), (row_count_field, "top", 14, shape_type), (row_count_field, "left", 4, row_count_label)])
    cmds.formLayout(layout,
                    e=True,
                    af=[(columns_count_label, "left", 4)],
                    ac=[(columns_count_label, "top", 35, shape_type), (columns_count_field, "top", 35, shape_type), (columns_count_field, "left", 4, columns_count_label)])
    cmds.formLayout(layout,
                    e=True,
                    af=[(num_of_bugs_label, "left", 4)],
                    ac=[(num_of_bugs_label, "top", 55, shape_type), (num_of_bugs_field, "top", 55, shape_type), (num_of_bugs_field, "left", 4, num_of_bugs_label)])
    
    cmds.formLayout(layout,
                    e=True,
                    af=[(randomx_zone_label, "left", 4)],
                    ac=[(randomx_zone_label, "top", 75, shape_type), (randomx_zone_field, "top", 75, shape_type), (randomx_zone_field, "left", 4, randomx_zone_label)])

    cmds.formLayout(layout,
                    e=True,
                    af=[(randomy_zone_label, "left", 4)],
                    ac=[(randomy_zone_label, "top", 95, shape_type), (randomy_zone_field, "top", 95, shape_type), (randomy_zone_field, "left", 4, randomy_zone_label)])       
                              
    cmds.formLayout(layout,
                    e=True,
                    af=[(create_button, "left", 4), (create_button, "right", 0), (create_button, "bottom", 10)],
                    ac=[(create_button, "top", 110, row_count_label)])
    
    cmds.showWindow(window)
                                                    
if __name__ == "__main__":
    create_ui()