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
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits

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
                           t_exp=200#str(i*10 + 200)
                           ))

with pc.ImageEnsemble(files) as ensemble:
    S_hat_stack, S_stack, S_hat, S, R_hat = ensemble.calculate_R(n_procs=6,
                                                                 debug=True)

plt.subplot(121)
plt.imshow(np.log10(np.absolute(R_hat.real)), cmap='viridis')
plt.subplot(122)
plt.imshow(np.log10(np.absolute(R_hat.imag)), cmap='viridis')
plt.savefig('R_hat.png')

plt.subplot(121)
plt.imshow(np.log10(np.absolute(S_hat.real)), cmap='viridis')
plt.subplot(122)
plt.imshow(np.log10(np.absolute(S_hat.imag)), cmap='viridis')
plt.savefig('S_hat.png')

R_std = np.std(S_hat_stack, axis=2)

plt.imshow(np.log10(np.absolute(R_std)), cmap='viridis')
plt.savefig('R_std.png')


R = pc._ifftwn(R_hat)

utils.encapsule_R(R, path='R.fits')
