import pandas as pd
import numpy as np


class Material:
    def __init__(self, name, alpha, E, nu, Kic):
        """

        :param name: name of material
        :param alpha: thermal expansion [10^(-6) / K]
        :param E: Young modulus [GPa]
        :param nu: Poisson number [-]
        :param Kic: Fracture toughness [MPa sqrt(m)]
        """
        self.name = name
        self.alpha = alpha * 10 ** (-6)     # 1 / K
        self.E = E * 10 ** 9                # Pa
        self.nu = nu                        # -
        self.Kic = Kic * 10 ** 6            # Pa sqrt(m)
        self.delta_T = self.shock(1)        # [K] maximal temp change in material with half circular crack 1 mm diameter

    def shock(self, crack_size):
        """

        :param crack_size: [mm] size of half circular crack
        :return: delta_T [K] maximal permisible temperature change in material with half circular crack
        """

        delta_T = np.abs(self.Kic / self.K(crack_size))     # [K]

        return delta_T

    def K(self, crack_size):
        """

        :param crack_size: radius of half circular crack [mm]
        :return: K [Pa * sqrt(m) / K] stress intensity factor caused by 1 K decrease of temperature
        """
        crack_size = crack_size * 10 ** (-3)                   # m
        F = 0.728                                              # shape coefficient fig. 8.17 Dowling

        K = F * self.sigma() * np.sqrt(np.pi * crack_size)     # fig. 8.17 Dowlnig

        return K

    def sigma(self):
        """

        :return: sigma - stress caused by 1 K decrease of temperature [Pa / K]
        """
        sigma = -(self.E * self.alpha * (-1)) / (1 - self.nu)      # eq. 5.41 Dowling
        return sigma


materials = [
    Material('soda-lime glass', 9.1, 69, 0.2, 0.76),
    Material('MgO', 13.5, 300, 0.18, 2.9),
    Material('Al2O3', 8, 400, 0.22, 4),
    Material('SiC', 4.5, 396, 0.22, 3.7),
    Material('Si3N4', 2.9, 310, 0.27, 5.6)
          ]                                                 # tables 8.21 and 8.2 Dowling

df = pd.DataFrame(columns=['name', 'Kic [Pa sqrt(m)]', 'K [Pa sqrt(m) / K]', 'delta_T [K]'])

for mat in materials:
    df.loc[len(df.index)] = [mat.name, mat.Kic, mat.K(1), mat.delta_T]

df = df.sort_values(by=['delta_T [K]'])

print('\n')

with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 2,
                       ):
    print(df)

print('\n')
