
# Standard libraries.
import math
import matplotlib.pyplot as plt
import numpy as np

# ACS Toolbox.
from acs_toolbox.foundation import rotation as C


def theta_tick(theta, dtheta):
    # 0 indexed
    return theta/dtheta + 1

def phi_tick(phi, dphi):
    # 0 indexed
    return phi/dphi + 1

def CartesianToSpherical(x):
    x = x/np.linalg.norm(x)
    phi = math.acos(x[2])
    if (x[0] == 0.0 and x[1] == 0.0 ):
        theta = None
    elif (x[0] == 0.0):
        if (x[1] > 0.0):
            theta = np.pi/2
        elif (x[1] < 0.0):
            theta = -np.pi/2
    else:
        theta = math.atan2(x[1], x[0])

    return theta, phi

class CelestialSphere:
    """Celestial Sphere
    # TODO: Make all 4 step sizes in the wire frames class parameters.
    """

    def __init__(self, sphere_radius, wire_colour="k", grid_dtheta=200, grid_dphi=100):
        """Constructor.
        """

        # Celestial sphere.
        self._wire_colour = wire_colour
        self._sphere_radius = sphere_radius
        self._meshgrid = []
        self._z = np.array([0, 0, 1])
        self._grid_dtheta = complex(0,grid_dtheta)
        self._grid_dphi = complex(0,grid_dphi)

        # Draw 2D Polar Plot
        self._n = 2
        self._dtheta = 10**(-self._n)
        self._dphi = 10**(-self._n)
        self._B = np.zeros((int(np.pi/self._dphi) + 1, int(2*np.pi/self._dtheta) + 1))
        self._px = 0
        self._nx = 0

    def polarplot(self):
        fig2d = plt.figure(2, figsize=(12,6))
        ax = fig2d.gca()
        ax.imshow(self._B, cmap='RdPu', vmin=0, vmax=255)
        plt.title("Area Projections on Polar Plot")
        plt.xticks([0, theta_tick(np.pi/2, self._dtheta), theta_tick(np.pi, self._dtheta), theta_tick(1.5*np.pi, self._dtheta), theta_tick(2*np.pi, self._dtheta)],['0', '$\\frac{\pi}{2}$', '$\pi$', '$\\frac{3\pi}{2}$', '$2\pi$'])
        plt.yticks([0, phi_tick(np.pi/4, self._dphi), phi_tick(np.pi/2, self._dphi), phi_tick(0.75*np.pi, self._dphi), phi_tick(np.pi, self._dphi)],['0', '$\\frac{\pi}{4}$', '$\\frac{\pi}{2}$', '$\\frac{3\pi}{4}$', '$\pi$'])

        plt.show()

    def celestialplot(self):
        fig = plt.figure(1)
        ax = fig.gca(projection='3d')
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = np.cos(u)*np.sin(v)*self._sphere_radius
        y = np.sin(u)*np.sin(v)*self._sphere_radius
        z = np.cos(v)*self._sphere_radius
        ax.plot_surface(x, y, z, color="w", edgecolor=self._wire_colour)

        # self._axis.arrow3D(1,0,0,1,1,1,mutation_scale=20,ec ='green',fc='red')
        # Draw body axes.
        # self._axis.quiver(0,0,0,1.5,0,0,length=1.0)
        # self._axis.quiver(0,0,0,0,1.5,0,length=1.0)
        # self._axis.quiver(0,0,0,0,0,1.5,length=1.0)

        for grid in self._meshgrid:
            x = grid[0]
            y = grid[1]
            z = grid[2]
            ax.plot_surface(x, y, z, color="w", edgecolor="b")

        # Label body axes.
        plt.figure(1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        # Set ticks.
        axis_ticks = np.arange(-1.0, 1.0, 0.5).tolist()
        ax.set_xticks(axis_ticks)
        ax.set_yticks(axis_ticks)
        ax.set_zticks(axis_ticks)
        plt.title("Projections on Celestial Sphere")

        # Show celestial sphere.
        plt.show()

    def conical_exclusion_area(self, v_b, half_angle_deg, val):
        v_b = v_b/np.linalg.norm(v_b)
        a = np.cross(self._z, v_b)
        phi = math.acos(np.dot(self._z, v_b))

        # Negate the angle to transform the points with C_sb.
        C_transform_z = C.EulerAxis(a, -phi)

        self.add_conical_sensor(half_angle_deg, C_transform_z, val)

    def add_conical_sensor(self, half_angle_deg, C, val):
        phi_max = half_angle_deg/180.0*np.pi
        theta, phi = np.mgrid[0:2*np.pi:self._grid_dtheta, 0:phi_max:100j]

        # Cartesian coordinates.
        x = np.cos(theta)*np.sin(phi)
        y = np.sin(theta)*np.sin(phi)
        z = np.cos(phi)

        # Determine the shape of the grids.
        m, n = np.shape(x)
        n_rays = m*n

        # Reshape the axes, Stack and transform through the desired rotation.
        sensor_rays = np.vstack((x.reshape(n_rays),y.reshape(n_rays),z.reshape(n_rays)))
        transformed_sensor_rays = np.dot(C, sensor_rays)

        # Retrieve the individual axes.
        x = transformed_sensor_rays[0,:].reshape(m,n)
        y = transformed_sensor_rays[1,:].reshape(m,n)
        z = transformed_sensor_rays[2,:].reshape(m,n)

        # Add to celestial plot.
        grid = list((x,y,z))
        self._meshgrid.append(grid)

        # Add to 2D plot.
        for v in np.transpose(transformed_sensor_rays):
            theta, phi = CartesianToSpherical(v)

            tphi = round(phi, self._n)
            phi_index = round(tphi/self._dphi)
            if theta != None:
                ttheta = round(theta, self._n)
                theta_index = round(ttheta/self._dtheta)
            else:
                if (v.dot(np.array([0,0,1])) == 1.0):
                    self._px = 1
                    continue
                elif (v.dot(np.array([0,0,-1])) == 1.0):
                    self._nx = 1
                    continue

            if (val.real):
                self._B[phi_index, theta_index] = val.imag + self._B[phi_index, theta_index]
            else:
                self._B[phi_index, theta_index] = val.imag

    def add_rectangular_sensor(self, focal_length_m, u, v, C):
        x, y = np.mgrid[-u:u:5j, -v:v:5j]
        
        # Determine the shape of the grids.
        m, n = np.shape(x)
        n_rays = m*n

        # Focal length of the sensor.
        z = np.ones(n_rays) * focal_length_m
        
        # Stack the axes and normalize.
        unnormalized_sensor_rays = np.vstack((x.reshape(n_rays), y.reshape(n_rays), z))
        unnormalized_magnitudes = np.sqrt(np.sum(unnormalized_sensor_rays**2, axis=0))
        normalized_sensor_rays = unnormalized_sensor_rays / unnormalized_magnitudes[np.newaxis,:]

        # Transform the boresight from [0 0 +1] by C.
        normalized_sensor_rays = np.dot(C,normalized_sensor_rays)
        
        # Reshape to the original grid shape.
        x = normalized_sensor_rays[0,:].reshape(m,n)
        y = normalized_sensor_rays[1,:].reshape(m,n)
        z = normalized_sensor_rays[2,:].reshape(m,n)

        # Add to celestial plot.
        grid = list((x,y,z))
        self._meshgrid.append(grid)

def main():    
    # Run as a script.
    print(f"File cannot be run as a script")

if __name__ == '__main__':
    main()