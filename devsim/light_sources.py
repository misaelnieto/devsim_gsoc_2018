import os.path
import csv
from numpy import interp as interpolate

DATADIR = os.path.join(os.path.dirname(__file__), 'data')


class AM0(object):
    """docstring for GenericLightSource"""
    def __init__(self, lambda_min=280, lambda_max=4000, samples=None):
        self.lambda_min = lambda_min
        self.lambda_max = lambda_max
        self._wavelength = []
        self._irradiance = []

        data_file = os.path.join(DATADIR, 'AM0.csv')
        with open(data_file, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, fieldnames=('wavelength', 'irradiance', 'photon_flux')
            )
            for row in reader:
                wl = float(row['wavelength'])
                if lambda_min <= wl <= lambda_max:
                    self._wavelength.append(wl)
                    self._irradiance.append(float(row['irradiance']))

        if samples is not None:
            # Probably not the best way? We'll see
            interval = len(self._wavelength) // samples
            self._wavelength = self._wavelength[::interval]
            self._irradiance = self._irradiance[::interval]
            if len(self._wavelength) == samples + 1:
                self._wavelength.pop()
                self._irradiance.pop()

    def __len__(self):
        return len(self._wavelength)

    def irradiance(self, wavelength):
        """
            Returns spectral irradiance for the given wavelength
            Units: W/(m–2⋅nm–1)
        """
        if wavelength < self.lambda_min or wavelength > self.lambda_max:
            return 0.0
        if wavelength in self._wavelength:
            ix = self._wavelength.index(wavelength)
            return self._irradiance[ix]
        return interpolate(
            wavelength,
            self._wavelength,
            self._irradiance
        )
