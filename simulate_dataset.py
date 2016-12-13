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

import ois
from properimage import propercoadd as pc
from properimage import propersubtract as ps
from properimage import utils

import stuffskywrapper as w


def main(imgs_dir):

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
               'exp_time'   : 350,
               'mag_zp'     : 25.0,
               'px_scale'   : 0.3,
               'seeing_fwhm': 0.90,
               'starcount_zp': 3e5,
               'starcount_slope': 0.2
               }

    w.write_skyconf('dataset_simulation/conf.sky', skyconf)
    ref = w.run_sky('dataset_simulation/conf.sky', cat_name,
                    img_path=os.path.join(imgs_dir, 'ref.fits'))

    # add some transients
    rows = []
    for i in xrange(40):
        code = 100
        x = np.random.randint(20, 1004)
        y = np.random.randint(20, 1004)
        app_mag = 4. * np.random.random() + 19.
        row = [code, x, y, app_mag]
        #row.extend(np.zeros(9))
        rows.append(row)

    newcat = Table(rows=rows, names=['object_code', 'x', 'y', 'app_mag'])

    newcat.write('dataset_simulation/transient.list',
                 format='ascii.fast_no_header')

    os.system('cat dataset_simulation/images/ref.list >> dataset_simulation/transient.list')

    # generate the new image
    skyconf = {'image_name' : 'test.fits',
               'image_size' : 1024,
               'exp_time'   : 300,
               'mag_zp'     : 25.0,
               'px_scale'   : 0.3,
               'seeing_fwhm': 1.2,
               'starcount_zp': 3e-4,
               'starcount_slope': 0.2
               }

    cat_name = os.path.join('dataset_simulation/transient.list')
    w.write_skyconf('dataset_simulation/conf.sky', skyconf)

    new = w.run_sky('dataset_simulation/conf.sky', cat_name,
                    img_path=os.path.join(imgs_dir, 'new.fits'))

    print 'Images to be subtracted: {} {}'.format(ref, new)

    with ps.ImageSubtractor(ref, new, align=False) as subtractor:
        D, P = subtractor.subtract()

    xc, yc = np.where(P.real==np.max(P.real))
    P = P.real[0:2*np.int(xc), 0:2*np.int(yc)]

    d_shifted = np.ones(D.shape) * np.median(D)
    d_shifted[14:, 14:] = D[7:-7, 7:-7]

    D = d_shifted

    utils.encapsule_R(D, path=os.path.join(imgs_dir, 'diff.fits'))

    utils.encapsule_R(P, path=os.path.join(imgs_dir, 'psf_d.fits'))

    #~ ois_d = ois.optimal_system(fits.getdata(ref), fits.getdata(ref))[0]
    #~ utils.encapsule_R(ois_d, path=os.path.join(imgs_dir, 'diff_ois.fits'))

    return newcat


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
