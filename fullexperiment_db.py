#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  fullexperiment_db.py
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

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy import Float, Text
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///home/bruno/Devel/synoptic/dataset_simulation/fullexperiment.db', echo=True)
Base = declarative_base()


class Simulated(Base):

    __tablename__ = "simulated"

    id = Column(Integer, primary_key=True)
    code = Column(Integer, nullable=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    app_mag = Column(Float, nullable=False)
    image = Column(String(100), nullable=False)

    def __init__(self, name):
        self.name = name


class Detected(Base):

    __tablename__ = "detected"

    id = Column(Integer, primary_key=True)
    NUMBER = Column(Integer, nullable=False)
    FLUX_ISO = Column(Float, nullable=False)
    FLUXERR_ISO = Column(Float, nullable=False)           # RMS error for isophotal flux                               [count]
    MAG_ISO = Column(Float, nullable=False)               # Isophotal magnitude                                        [mag]
    MAGERR_ISO = Column(Float, nullable=False)            # RMS error for isophotal magnitude                          [mag]
    FLUX_APER = Column(Float, nullable=False)             # Flux vector within fixed circular aperture(s)              [count]
    FLUXERR_APER = Column(Float, nullable=False)          # RMS error vector for aperture flux(es)                     [count]
    MAG_APER = Column(Float, nullable=False)              # Fixed aperture magnitude vector                            [mag]
    MAGERR_APER = Column(Float, nullable=False)           # RMS error vector for fixed aperture mag.                   [mag]
    FLUX_AUTO = Column(Float, nullable=False)             # Flux within a Kron-like elliptical aperture                [count]
    FLUXERR_AUTO = Column(Float, nullable=False)          # RMS error for AUTO flux                                    [count]
    MAG_AUTO = Column(Float, nullable=False)              # Kron-like elliptical aperture magnitude                    [mag]
    MAGERR_AUTO = Column(Float, nullable=False)           # RMS error for AUTO magnitude                               [mag]
    BACKGROUND = Column(Float, nullable=False)            # Background at centroid position                            [count]
    THRESHOLD = Column(Float, nullable=False)             # Detection threshold above background                       [count]
    FLUX_MAX = Column(Float, nullable=False)              # Peak flux above background                                 [count]
    XMIN_IMAGE = Column(Float, nullable=False)            # Minimum x-coordinate among detected pixels                 [pixel]
    YMIN_IMAGE = Column(Float, nullable=False)            # Minimum y-coordinate among detected pixels                 [pixel]
    XMAX_IMAGE = Column(Float, nullable=False)            # Maximum x-coordinate among detected pixels                 [pixel]
    YMAX_IMAGE = Column(Float, nullable=False)            # Maximum y-coordinate among detected pixels                 [pixel]
    X_IMAGE = Column(Float, nullable=False)               # Object position along x                                    [pixel]
    Y_IMAGE = Column(Float, nullable=False)               # Object position along y                                    [pixel]
    X2_IMAGE = Column(Float, nullable=False)              # Variance along x                                           [pixel**2]
    Y2_IMAGE = Column(Float, nullable=False)              # Variance along y                                           [pixel**2]
    XY_IMAGE = Column(Float, nullable=False)              # Covariance between x and y                                 [pixel**2]
    CXX_IMAGE = Column(Float, nullable=False)             # Cxx object ellipse parameter                               [pixel**(-2)]
    CYY_IMAGE = Column(Float, nullable=False)             # Cyy object ellipse parameter                               [pixel**(-2)]
    CXY_IMAGE = Column(Float, nullable=False)             # Cxy object ellipse parameter                               [pixel**(-2)]
    A_IMAGE = Column(Float, nullable=False)               # Profile RMS along major axis                               [pixel]
    B_IMAGE = Column(Float, nullable=False)               # Profile RMS along minor axis                               [pixel]
    THETA_IMAGE = Column(Float, nullable=False)           # Position angle (CCW/x)                                     [deg]
    MU_MAX = Column(Float, nullable=False)                # Peak surface brightness above background                   [mag * arcsec**(-2)]
    FLAGS = Column(Float, nullable=False)                 # Extraction flags
    FWHM_IMAGE = Column(Float, nullable=False)            # FWHM assuming a gaussian core                              [pixel]
    ELONGATION = Column(Float, nullable=False)            # A_IMAGE/B_IMAGE
    ELLIPTICITY = Column(Float, nullable=False)           # 1 - B_IMAGE/A_IMAGE
    CLASS_STAR = Column(Float, nullable=False)            # S/G classifier output
    IMAGE = Column(String(100), nullable=False)

Base.metadata.create_all(engine)

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
