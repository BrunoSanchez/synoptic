#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  run_synoptic.py
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
from properimage import propercoadd as pc
from properimage import utils
import stuffskywrapper as w

stuffconf = {'cat_name' : 'cat.list',
             'im_w'     : 1024,
             'im_h'     : 1024,
             'px_scale' : 0.3
             }

w.write_stuffconf('conf.stuff', stuffconf)
cat_name = w.run_stuff('conf.stuff')

skyconf = {'image_name' : 'test.fits',
           'image_size' : 1024,
           'exp_time'   : 300,
           'mag_zp'     : 25.0,
           'px_scale'   : 0.3,
           'seeing_fwhm': 0.9
           }

w.write_skyconf('conf.sky', skyconf)
img = w.run_sky('conf.sky', img_path='test_image')

files = []
for i in range(40):
    files.append(w.run_sky('conf.sky',
                           img_path='./test_images/image_{}.fits'.format(
                                    str(i).zfill(3)),
                           t_exp=str(i*10 + 200))
                           )

with pc.ImageEnsemble(files) as ensemble:
    R, S = ensemble.calculate_R(n_procs=4, return_S=True)


utils.encapsule_S(S, 'S.fits')
utils.encapsule_R(R, 'R.fits')

utils.plot_S(S, 'S.png')
utils.plot_R(R, 'R.png')


import numpy as np
aux_r = np.ma.masked_outside(R.real, 0.1, 30000., copy=True)


utils.encapsule_S(aux_r.filled(0.1), 'R_aux.fits')
utils.plot_S(aux_r, 'R_aux.png')
