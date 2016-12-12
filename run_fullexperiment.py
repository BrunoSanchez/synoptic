#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  run_fullexperiment.py
#
#  Copyright 2016 Bruno S <bruno@oac.unc.edu.ar>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import os
from astropy.io import ascii
import simulate_dataset as sd
import stuffskywrapper as w

imgs_dir = os.path.abspath('./dataset_simulation/images/')

for i in range(3):
    suffix = 'img{}'.format(str(i).zfill(5))

    curr_dir = os.path.join(imgs_dir, suffix)

    transients = sd.main(curr_dir)

    diff_path = os.path.join(curr_dir, 'diff.fits')
    cat_out = os.path.join(curr_dir, 'outcat.cat')

    w.run_sex('./conf.sex', diff_path, cat_output='outcat.dat')

    detections = ascii.read('outcat.dat', format='sextractor')

    deltax = list(detections["XMAX_IMAGE"] - detections["XMIN_IMAGE"])
    deltay = list(detections["YMAX_IMAGE"] - detections["YMIN_IMAGE"])
    ratio = [float(min(dx,dy))/float(max(dx,dy,1))
             for dx, dy in zip(deltax, deltay)]

    roundness = list(detections["A_IMAGE"] / detections["B_IMAGE"])

    peak_centroid = list(np.sqrt((detections['XPEAK_IMAGE'] - detections['X_IMAGE'])**2
                     + (detections['YPEAK_IMAGE'] - detections['Y_IMAGE'])**2))



