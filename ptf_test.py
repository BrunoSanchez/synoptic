#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ptf_test.py
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
from astropy.io import fits
import ois
from properimage import propersubtract as ps
from properimage import utils


ref = '/home/bruno/Data/ptf/proc/2009/03/21/f1/c2/p5/v3/PTF_200903212791_i_p_scie_t064154_u016700438_f01_p100037_c02_ra148.8882_dec69.0653_asec7200.fits'
new = '/home/bruno/Data/ptf/proc/2009/03/21/f1/c2/p5/v3/PTF_200903213762_i_p_scie_t090144_u016700460_f01_p100037_c02_ra148.8882_dec69.0653_asec7200.fits'


with ps.ImageSubtractor(ref, new) as subtractor:
    D, _ = subtractor.subtract()
    utils.encapsule_R(D, path='dataset_simulation/ptf_images/diff.fits')

#~ ois_d = ois.optimal_system(fits.getdata(ref), fits.getdata(ref))[0]
#~ utils.encapsule_R(ois_d, path='dataset_simulation/ptf_images/diff_ois.fits')

