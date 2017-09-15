import numpy as np
import PyFVCOM as pf
from shapely.geometry import Polygon, Point

import pylag_startlocs as ps

fvcom_grid_file = '/data/euryale4/backup/mbe/Code/fvcom-projects/locate/run/input/tamar_v2_grd.dat'
triangle, nodes, X, Y, Z = pf.grid_tools.read_fvcom_mesh(fvcom_grid_file)
poly_list = pf.grid_tools.get_boundary_polygons(triangle)
poly_xy = np.asarray([X[poly_list[0]], Y[poly_list[0]]]).T

tamar_subset = np.asarray([[420437.66909469309, 5578342.1487603299],
						[422051.53485952143, 5578877.6859504124],
						[423096.57908428728, 5581793.3884297507],
						[423123.03590010415, 5584917.3553718999],
						[418056.55567117594, 5598395.0413223132],
						[411574.63579604583, 5599049.5867768582],
						[407698.71227887622, 5591462.809917354],
						[407196.03277835593, 5582507.4380165283],
						[408796.67013527581, 5580038.0165289249],
						[414431.97190426645, 5577211.5702479333],
						[415662.21383975033, 5578074.3801652882],
						[416746.94328824151, 5578312.3966942141]])

rough_subset_area = ps.grid_area(tamar_subset)
is_in = rough_subset_area.points_in_area(poly_xy)

tamar_subset_area = ps.grid_area(poly_xy[is_in,:])

test_start_locs = ps.start_locs_set(tamar_subset_area)
test_start_locs.get_n_particles(10000)
test_start_locs.write_particle_file('test_out.dat')
