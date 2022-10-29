import bpy

def decimal_to_reversed_binary_list(number):
    reversed_binary_list = [int(x) for x in bin(number)[2:]]
    reversed_binary_list.reverse()
    return reversed_binary_list

def carve_out_with_object(main_object, carve_object):
    # Deselect all and select only main_object
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = main_object
    main_object.select_set(True)
    
    # Carve out with boolean modifier
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].object = carve_object
    bpy.ops.object.modifier_apply(modifier="Boolean")



bpy.ops.mesh.primitive_cube_add(size=0.12, enter_editmode=False, align='WORLD', location=(0, 0, 0))
bpy.context.active_object.name = 'big_cube'
bpy.ops.mesh.primitive_cube_add(size=0.01, enter_editmode=False, align='WORLD', location=(0.045, 0.055, 0.045))
bpy.context.active_object.name = 'small_cube'

big_cube = bpy.data.objects['big_cube']
small_cube = bpy.data.objects['small_cube']

carve_out_with_object(big_cube, small_cube)


#bpy.context.view_layer.objects.active = big_cube
#bpy.context.object.modifiers["Boolean"].object = None
#bpy.ops.object.modifier_apply(modifier="Boolean")


