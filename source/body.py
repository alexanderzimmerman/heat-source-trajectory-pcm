import numpy as np
import math

import input

def move(old_points, x):
    assert(x.size == 3)  # 2D
    theta = x[2]
    rotation_matrix = np.matrix([[math.cos(theta), math.sin(theta)], [-math.sin(theta), math.cos(theta)]])
    # @todo: Is the rotation direction consistent with the deal.II parameter?
    points = np.matrix(old_points)*rotation_matrix
    points = points + x[:2]
    return np.array(points)


def centroid(points):
    length = points.shape[0]
    sum_x = np.sum(points[:, 0])
    sum_y = np.sum(points[:, 1])
    return np.array((sum_x/length, sum_y/length))


def get_hull_points(state=np.array((0., 0., 0.))):
    return get_sphere_cylinder_points(state)


def get_sphere_cylinder_points(state):
    sizes = input.body['sizes']
    # Construct spherical curve parametrically
    arc_point_count = input.body['arc_point_count']
    sample_angles = np.linspace(np.pi, 2*np.pi, arc_point_count)
    sphere_radius = sizes[0]
    nose_x = sphere_radius*np.cos(sample_angles)
    nose_y = sphere_radius*np.sin(sample_angles)
    nose_points = np.vstack((nose_x, nose_y))
    nose_points = np.transpose(nose_points)
    # Construct aft-body
    cylinder_length = sizes[2]
    line_point_count = input.body['line_point_count']
    aft_body_points = points_on_line([sphere_radius, 0], [sphere_radius, cylinder_length], line_point_count)
    aft_body_points = np.append(aft_body_points, points_on_line([-sphere_radius, cylinder_length], [-sphere_radius, 0], line_point_count), axis=0)
    #
    body_points = np.concatenate((nose_points, aft_body_points))
    body_points = move(body_points, state)
    return body_points


def points_on_line(start_point, end_point, count):
    return np.transpose(np.vstack((np.linspace(start_point[0], end_point[0], count),
                                   np.linspace(start_point[1], end_point[1], count))))


def get_center_of_gravity(state=np.array(0.)):
    return centroid(get_hull_points(state))  # Assume uniform density within the body


def close_curve(points):
    return np.row_stack((points, points[0, :]))
