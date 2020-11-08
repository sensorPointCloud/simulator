import bpy
import numpy as np
from math import radians
import time

def program():
    output_directory = 'D:\\test\\result'
    absolute_angle_camera_and_laser_angle_and_offset(70, 20, -0.2)
    laser_start = -20.0
    laser_end = 20.0
    deg_incr = 0.1
    cam_start = 37.1
    cam_end = 70.0
    create_series(cam_start, cam_end, deg_incr, laser_start, laser_end, deg_incr, output_directory)


def create_series(from_deg_cam, to_deg_cam, deg_incr_cam, from_deg_laser, to_deg_laser, deg_incr_laser, output_directory):
    cam_z_angles = np.arange(from_deg_cam, to_deg_cam, deg_incr_cam)
    laser_x_angles = np.arange(from_deg_laser, to_deg_laser, deg_incr_laser)
    
    print('Creating series from_deg_cam: %f, to_deg_cam: %f, deg_incr_cam: %f, from_deg_laser: %f, to_deg_laser: %f, deg_incr_laser: %f' % (from_deg_cam, to_deg_cam, deg_incr_cam, from_deg_laser, to_deg_laser, deg_incr_laser) )
    for z in cam_z_angles:
        for x in laser_x_angles:
            dir = output_directory
            filename = 'z_%f_x_%f' % (z,x)
            path = '%s/%s' % (dir,filename)
            print(path)
            
            absolute_angle_camera_and_laser_angle_and_offset(z, x, -0.2)
            save_environment_points_matrixes_and_depth_to_file(path)
            bpy.data.scenes["Scene"].render.image_settings.compression = 0
            bpy.data.scenes["Scene"].render.image_settings.file_format = 'PNG'
            bpy.data.images['Render Result'].save_render(path + '.png')
            print('Current camera z: %f, current laser x: %f' % (z,x) )
    

# Generates world coordinates, x,y,z
def environment_points_xyz(filename='environmet_points.xyz'):
    print('Test')


def absolute_angle_camera_and_laser_angle_and_offset(cam_z_deg, laser_x_deg, laser_z_offset):
    # Set rotations
    obj_camera = bpy.context.scene.camera
    obj_camera.rotation_euler.z = radians(cam_z_deg)
    bpy.data.objects['Laser'].data.node_tree.nodes["Mapping"].rotation[0] = bpy.context.scene.camera.rotation_euler.x + radians(90+laser_x_deg)
    bpy.data.objects['Laser'].data.node_tree.nodes["Mapping"].rotation[2] = bpy.context.scene.camera.rotation_euler.z
    # Set offset
    bpy.data.objects['Laser'].location.x=bpy.context.scene.camera.location.x
    bpy.data.objects['Laser'].location.y=bpy.context.scene.camera.location.y
    bpy.data.objects['Laser'].location.z=bpy.context.scene.camera.location.z+laser_z_offset


# x=image[:,:,0], y=image[:,:,1], z=image[:,:,2], depth=image[:,:,3]
def get_environment_points_xyz_and_depth(image_as_matrix=False):
    print('Rendering environment points and pixel depth')
    
    bpy.ops.render.render()
    
    # get viewer pixels
    pixels = np.array(bpy.data.images['Viewer Node'].pixels)
    print(len(pixels)) # size is always width * height * 4 (rgba)
    
    width = bpy.context.scene.render.resolution_x 
    height = bpy.context.scene.render.resolution_y
    
    
    # reshaping into image array 4 channel (rgbz)
    if image_as_matrix:
        image = pixels.reshape(height,width,4)
        return image
    else:
        image = pixels.reshape(height*width,4)
        return image

# Save environment points to one file that can be directly loaded into meshlab
def save_environment_points_and_depth_to_file():
    image = get_environment_points_xyz_and_depth()
    np.savetxt('C:/Users/knutbk/Dropbox/UNDERVISNING/SFI/Sensor 3d devel/Simulation/blender/readme/environment.xyz',image[:,0:3],fmt='%f')

# Save to four files, where x, y, and z are separate files and corresponds to their pixel idices, like a '3d image'
# columns = 'image width' and rows = 'image height'
def save_environment_points_matrixes_and_depth_to_file(filename):
    image = get_environment_points_xyz_and_depth(True)
    x_name = '%s%s' % (filename,'x.txt')
    y_name = '%s%s' % (filename,'y.txt')
    z_name = '%s%s' % (filename,'z.txt')
    depth_name = '%s%s' % (filename,'depth.txt')
    #np.savetxt(x_name,image[:,:,0],fmt='%f')
    #np.savetxt(y_name,image[:,:,1],fmt='%f')
    #np.savetxt(z_name,image[:,:,2],fmt='%f')
    np.savetxt(depth_name,image[:,:,3],fmt='%f')

# Runs the program
program()