#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  simulate_dataset.py
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
import shutil
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from astropy.io import ascii
from astropy.table import Table

from properimage import propercoadd as pc
from properimage import propersubtract as ps
from properimage import utils

import stuffskywrapper as w

imgs_dir = os.path.abspath('./dataset_simulation/images')
if not os.path.isdir(imgs_dir):
    os.makedirs(imgs_dir)

# generate stuff cat
stuffconf = {'cat_name' : 'dataset_simulation/gxcat.list',
             'im_w'     : 1024,
             'im_h'     : 1024,
             'px_scale' : 0.3
             }

w.write_stuffconf('dataset_simulation/conf.stuff', stuffconf)
cat_name = stuffconf['cat_name']
w.run_stuff('dataset_simulation/conf.stuff')

# generate the Reference image
skyconf = {'image_name' : 'test.fits',
           'image_size' : 1024,
           'exp_time'   : 300,
           'mag_zp'     : 25.0,
           'px_scale'   : 0.3,
           'seeing_fwhm': 0.9,
           'starcount_zp': 3e4,
           'starcount_slope': 0.2
           }

w.write_skyconf('dataset_simulation/conf.sky', skyconf)
ref = w.run_sky('dataset_simulation/conf.sky', cat_name,
                img_path=os.path.join(imgs_dir, 'ref.fits'))

# now read the output source list and add some transients
#~ colnames = ['object_code', 'x', 'y', 'app_mag', 'bulge_to_total', 'bulge_rad',
            #~ 'bulge_aspect', 'bulge_PA','disk_scale_l', 'disk_aspect',
            #~ 'disk_PA', 'z', 'hubble_stage']

#~ refcat = ascii.read(os.path.join(imgs_dir, 'ref.list'),
                    #~ format='fast_no_header',
                    #~ names=colnames)

rows = []
for i in xrange(15):
    code = 100
    x = np.random.randint(10, 1014)
    y = np.random.randint(10, 1014)
    app_mag = 4. * np.random.random() + 18.
    row = [code, x, y, app_mag]
    #row.extend(np.zeros(9))
    rows.append(row)

newcat = Table(rows=rows, names=['object_code', 'x', 'y', 'app_mag'])

newcat.write('dataset_simulation/transient.list',
             format='ascii.fast_no_header')

#os.system('cat dataset_simulation/transient.list dataset_simulation/images/ref.list > dataset_simulation/transient.list')

# generate the Reference image
skyconf = {'image_name' : 'test.fits',
           'image_size' : 1024,
           'exp_time'   : 300,
           'mag_zp'     : 25.0,
           'px_scale'   : 0.3,
           'seeing_fwhm': 1.1,
           'starcount_zp': 3e-4,
           'starcount_slope': 0.2
           }

cat_name = os.path.join('dataset_simulation/transient.list')
w.write_skyconf('dataset_simulation/conf.sky', skyconf)

new = w.run_sky('dataset_simulation/conf.sky', cat_name,
                img_path=os.path.join(imgs_dir, 'new.fits'))

