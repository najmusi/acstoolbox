import sys
sys.path.append('/Volumes/Kingston128/Sandbox/exastris/')
import numpy as np
from acstoolbox.sensors import placement

# Set up celestial sphere with points drawn with boresight [0, 0, 1]
sphere = placement.CelestialSphere(0.9, "k")

# Rotate points -90 deg about [1, 0, 0]
C_x_90 = np.array([[1,0,0], [0, np.cos(np.pi/2), np.sin(np.pi/2)], [0, -np.sin(np.pi/2), np.cos(np.pi/2)]])

# sphere.add_conical_sensor(55, C_x_90)
# sphere.add_conical_sensor(45, C_x_90)

# Rotate points +90 deg about [1, 0, 0]
C_x_n90 = np.array([[1,0,0], [0, np.cos(-np.pi/2), np.sin(-np.pi/2)], [0, -np.sin(-np.pi/2), np.cos(-np.pi/2)]])
# sphere.add_rectangular_sensor(2.5,1,1,C_x_n90)


panel_normal_list = [np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1]),
                     np.array([-1,0,0]), np.array([0,-1,0]), np.array([0,0,-1])]

half_angle_fov_deg = 42.2

for normal in panel_normal_list:
    sphere.conical_exclusion_area(normal, half_angle_fov_deg, 200j)
# sphere.conical_exclusion_area(np.array([0,1,0]), 30.0, 200j)
sphere.polarplot()
# sphere.celestialplot()
