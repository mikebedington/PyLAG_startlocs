import numpy as np
import random as r
import multiprocessing as mp
from shapely.geometry import Polygon, Point, MultiPolygon
import PyFVCOM as pf

# TODO Parrerererelalise

MAX_PARTS_AT_ONCE = 2000
PARTS_PER_PLL_TASK = 4000

class start_locs_set():
    def __init__(self, choose_area):
        self.choose_area = choose_area
        self.bounding_box = choose_area.area_bound_box

    def get_n_particles(self, n, serial=True, poolsize=4):
        if serial:
            parts_per_it = min(MAX_PARTS_AT_ONCE, n)
        else:
            parts_per_it = list(np.asarray(np.ones(poolsize)*np.floor(min(PARTS_PER_PLL_TASK,n)/poolsize), dtype=int))

        chosen_parts = np.asarray([[],[]]).T
        if not serial:
            pool = mp.Pool(poolsize)
    
        while len(chosen_parts) < n:
            if serial:
                chosen_parts = np.append(chosen_parts, self._try_n_parts(parts_per_it), axis=0)
            else:
                # Launch the parallel plotting and then close the pool ready for the
                # next variable.
                chosen_parts_raw = pool.map(self._try_n_parts, parts_per_it)
                chosen_parts_raw = np.asarray([item for sublist in chosen_parts_raw for item in sublist])
                chosen_parts = np.append(chosen_parts, chosen_parts_raw, axis=0)
            print("%d of %d particles chosen" % (len(chosen_parts), n))
    
        if not serial:
            pool.close()
        self.chosen_parts = chosen_parts[0:n,:]
        return self.chosen_parts

    def _try_n_parts(self, n):
        x_parts = [r.uniform(self.bounding_box[0,0], self.bounding_box[0,1]) for x in range(0, n)]
        y_parts = [r.uniform(self.bounding_box[1,0], self.bounding_box[1,1]) for x in range(0, n)]
        parts_xy = np.asarray([x_parts, y_parts]).T
        parts_in = self.choose_area.points_in_area(parts_xy)
        return parts_xy[parts_in,:]

    def write_particle_file(self, filename, depth=0):            
        with open(filename, 'w') as out_file:
            out_file.write('%d\n' % len(self.chosen_parts))
            
            for this_part in self.chosen_parts:
                out_file.write('1 %f %f %f\n' % (this_part[0], this_part[1], depth))


class grid_area():
    def __init__(self, outline_points):
        if type(outline_points) == Polygon or type(outline_points) == MultiPolygon:
            self.area_poly = outline_points
        else:
            self.area_poly = Polygon(tuple(map(tuple, outline_points)))
        pb_temp = self.area_poly.bounds
        self.area_bound_box = np.asarray([[pb_temp[0], pb_temp[2]],[pb_temp[1], pb_temp[3]]])
        self.has_fvcom = False

    def add_fvcom_freader(self, fvcom_fr_str):
        self.fvcom_fr_str = fvcom_fr_str
        self.has_fvcom = True

    def points_in_area(self, points_list):
        particles_in = []

        for this_point in points_list:
            particles_in.append(Point(this_point).within(self.area_poly))
        
        if self.has_fvcom:
            self.fvcom_fr = pf.read.FileReader(self.fvcom_fr_str)
            points_list = np.asarray(points_list)
            particles_in = np.asarray(particles_in)
            test_pts = points_list[particles_in,:] 
            in_fvcom = self.fvcom_fr.in_domain(test_pts[:,0], test_pts[:,1], cartesian=True)
            particles_in[particles_in == True] = in_fvcom

        return np.asarray(particles_in)


class poly_area(grid_area):
    def __init__(self, poly):
        self.area_poly = poly
        pb_temp = self.area_poly.bounds
        self.area_bound_box = np.asarray([[pb_temp[0], pb_temp[2]],[pb_temp[1], pb_temp[3]]])


class multi_poly_area(grid_area):
    def __init__(self, poly_list):
        self.area_poly
        

    def points_in_area(self, points_list):
        grid_area.points_in_area(this_area, points_list)



