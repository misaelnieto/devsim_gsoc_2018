import os.path
import csv


DATADIR = os.path.join(os.path.dirname(__file__), 'data')


class AM0(object):
    """docstring for GenericLightSource"""
    def __init__(self, lambda_min=280, lambda_max=4000, samples=None):
        self.lambda_min = lambda_min
        self.lambda_max = lambda_max
        self._wavelength = []
        self._irradiance = []
        # open the file
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

    def irradiance(self, wavelength):
        """
            Returns spectral irradiance for the given wavelength
            Units: W/(m–2⋅nm–1)
        """
        return 1

