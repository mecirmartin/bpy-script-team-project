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


def select_object(object_ref):
    bpy.ops.object.select_all(action='DESELECT')
    object_ref.select_set(True)


def generate_wall_coordinates(big_cube_size, small_cube_size, padding):
    wall_start = big_cube_size/2 - small_cube_size/2
    wall_start_with_padding = wall_start - padding

    z_current = wall_start_with_padding
    x1_start = (wall_start, -wall_start_with_padding)
    x2_start = (-wall_start, wall_start_with_padding)
    y1_start = (wall_start_with_padding, wall_start)
    y2_start = (-wall_start_with_padding, -wall_start)

    x1_array = []
    x2_array = []
    y1_array = []
    y2_array = []

    for _ in range(10):
        for j in range(10):
            x1_array.append(
                (x1_start[0], round(x1_start[1] + j*small_cube_size, 3), z_current))
            x2_array.append(
                (x2_start[0], round(x2_start[1] - j*small_cube_size, 3), z_current))
            y1_array.append(
                (round(y1_start[0] - j*small_cube_size, 3), y1_start[1], z_current))
            y2_array.append(
                (round(y2_start[0] + j*small_cube_size, 3), y2_start[1], z_current))

        z_current = round(z_current - small_cube_size, 3)

    return [x1_array, x2_array, y1_array, y2_array]


def generate_ceil_coordinates(big_cube_size, small_cube_size, padding):
    wall_start = big_cube_size/2 - small_cube_size/2
    wall_start_with_padding = wall_start - padding

    z_current = wall_start
    z1_start = (-wall_start_with_padding, wall_start_with_padding)
    z1_array = []

    for i in range(10):
        for j in range(10):
            z1_array.append((round(z1_start[0] + j*small_cube_size, 3),
                            round(z1_start[1] - i*small_cube_size, 3), z_current))

    return z1_array


def generate_cube(wall_size_m, number):
    if (number > 2**100):
        raise ValueError("Number to encode can't be higher than 2^100.")

    bpy.ops.mesh.primitive_cube_add(
        size=12, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    bpy.context.active_object.name = 'big_cube'
    bpy.ops.mesh.primitive_cube_add(
        size=1, enter_editmode=False, align='WORLD', location=(0.055, 0.055, 0.055))
    bpy.context.active_object.name = 'small_cube'

    big_cube = bpy.data.objects['big_cube']
    small_cube = bpy.data.objects['small_cube']

    walls = generate_wall_coordinates(12, 1, 1)
    ceil = generate_ceil_coordinates(12, 1, 1)
    walls.append(ceil)

    binary_list = decimal_to_reversed_binary_list(number)

    for wall in walls:
        for index, coordinate in enumerate(wall):
            if index > len(binary_list)-1 or binary_list[index] == 0:
                small_cube.location = coordinate
                carve_out_with_object(big_cube, small_cube)

    # Delete small cube
    select_object(small_cube)
    bpy.ops.object.delete()

    select_object(big_cube)
    big_cube.dimensions = [wall_size_m, wall_size_m, wall_size_m]


generate_cube(0.12, 2593233243242343213645447993)
