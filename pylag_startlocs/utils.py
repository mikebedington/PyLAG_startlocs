import numpy as np
import random as r
from shapely.geometry import Polygon, Point

import PyFVCOM as pf

# TODO Parrerererelalise

MAX_PARTS_AT_ONCE = 2000

class start_locs_set():
	def __init__(self, choose_area):
		self.choose_area = choose_area
		self.bounding_box = choose_area.area_bound_box

	def get_n_particles(self, n):
		parts_per_it = min(MAX_PARTS_AT_ONCE, n)

		chosen_parts = np.asarray([[],[]]).T
	
		while len(chosen_parts) < n:
			print("%d of %d particles chosen" % (len(chosen_parts), n))
			x_parts = [r.uniform(self.bounding_box[0,0], self.bounding_box[0,1]) for x in range(0, parts_per_it)]
			y_parts = [r.uniform(self.bounding_box[1,0], self.bounding_box[1,1]) for x in range(0, parts_per_it)]
			parts_xy = np.asarray([x_parts, y_parts]).T
			parts_in = self.choose_area.points_in_area(parts_xy)
			chosen_parts = np.append(chosen_parts, parts_xy[parts_in], axis=0)
		
		self.chosen_parts = chosen_parts[0:n]
		return self.chosen_parts

	def write_particle_file(self, filename, depth=0):			
		with open(filename, 'w') as out_file:
			out_file.write('%d\n' % len(self.chosen_parts))
			
			for this_part in self.chosen_parts:
				out_file.write('1 %f %f %f\n' % (this_part[0], this_part[1], depth))


class grid_area():
	def __init__(self, outline_points):
		self.area_poly = Polygon(tuple(map(tuple, outline_points)))
		pb_temp = self.area_poly.bounds
		self.area_bound_box = np.asarray([[pb_temp[0], pb_temp[2]],[pb_temp[1], pb_temp[3]]])

	def points_in_area(self, points_list):
		particles_in = []
		for this_point in points_list:
			particles_in.append(Point(this_point).within(self.area_poly))
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



