from os.path import join as joinpath
import csv
from numpy import interp as interpolate
from devsim import DS_DATADIR


class AM0(object):
    """docstring for GenericLightSource"""
    def __init__(self, lambda_min=280, lambda_max=4000, samples=None):
        self.lambda_min = lambda_min
        self.lambda_max = lambda_max
        self._wavelength = []
        self._irradiance = []
        self._photon_flux = []

        data_file = joinpath(DS_DATADIR, 'AM0.csv')
        with open(data_file, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, fieldnames=('wavelength', 'irradiance', 'photon_flux')
            )
            for row in reader:
                wl = float(row['wavelength'])
                if lambda_min <= wl <= lambda_max:
                    self._wavelength.append(wl)
                    self._irradiance.append(float(row['irradiance']))
                    self._photon_flux.append(float(row['photon_flux']))

        if samples is not None:
            # Probably not the best way? We'll see
            interval = len(self._wavelength) // samples
            self._wavelength = self._wavelength[::interval]
            self._irradiance = self._irradiance[::interval]
            self._photon_flux = self._photon_flux[::interval]
            if len(self._wavelength) == samples + 1:
                self._wavelength.pop()
                self._irradiance.pop()
                self._photon_flux.pop()

    def __len__(self):
        return len(self._wavelength)

    def __iter__(self):
        return self._wavelength.__iter__()

    def __next__(self):
        return self._wavelength.__next__()

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

    def photon_flux(self, wavelength):
        """
            Returns photon_flux for the given wavelength
            Units: cm-2 * s-1
        """
        if wavelength < self.lambda_min or wavelength > self.lambda_max:
            return 0.0
        if wavelength in self._wavelength:
            ix = self._wavelength.index(wavelength)
            return self._photon_flux[ix]
        return interpolate(
            wavelength,
            self._wavelength,
            self._photon_flux
        )
