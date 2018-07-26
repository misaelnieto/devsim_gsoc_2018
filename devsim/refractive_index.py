import os.path
import csv
from numpy import interp as interpolate


DATADIR = os.path.join(os.path.dirname(__file__), 'data', 'refractive_indexes')


class RefractiveIndex(object):
    """docstring for RefractiveIndex"""
    lambda_min = 0
    lambda_max = 0
    _lambda = None
    _n = None
    _k = None
    _alpha = None

    def __init__(self, datafile):
        self._lambda = []
        self._n = []
        self._k = []
        self._alpha = []

        with open(os.path.join(DATADIR, datafile)) as csvfile:
            reader = csv.DictReader(
                csvfile, fieldnames=('wavelength', 'real', 'imaginary', 'absorption')
            )
            for row in reader:
                self._lambda.append(float(row['wavelength']))
                self._n.append(float(row['real']))
                self._k.append(float(row['imaginary']))
                self._alpha.append(float(row['absorption']))

        self.lambda_min = min(self._lambda)
        self.lambda_max = max(self._lambda)

    def __len__(self):
        return len(self._lambda)

    def __iter__(self):
        return self._lambda.__iter__()

    def __next__(self):
        return self._lambda.__next__()

    def refraction(self, wavelength):
        if wavelength in self._lambda:
            ix = self._lambda.index(wavelength)
            return self._n[ix]
        return interpolate(
            wavelength,
            self._lambda,
            self._n
        )

    n = real = refraction

    def extinction(self, wavelength):
        if wavelength in self._lambda:
            ix = self._lambda.index(wavelength)
            return self._k[ix]
        return interpolate(
            wavelength,
            self._lambda,
            self._k
        )

    k = imag = extinction

    def absorption(self, wavelength):
        if wavelength in self._lambda:
            ix = self._alpha.index(wavelength)
            return self._alpha[ix]
        return interpolate(
            wavelength,
            self._lambda,
            self._alpha
        )

    alpha = absorption
