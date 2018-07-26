# Data for devsim

## AM0.csv

Downloaded from [PV Lighthouse](https://www2.pvlighthouse.com.au/resources/optics/spectrum%20library/spectrum%20library.aspx) on July 21st 2018

**Description**: This is the Air Mass 0 spectrum, generated with SMARTS v 2.9.2 (with the SMARTS/Gueymard model chosen for the extraterrestrial spectrum).

**Outputs** Integrated over the range  280–4000 nm:

- **Intensity**: 1348,0434  W/m2
- **Photon flux** : 6,1445397E+17   cm–2⋅s–1
- **Photon current** : 98,447815    mA/cm2

Columns:
- Column 1: Wavelength (nm)
- Colimn 2: Spectral irradiance (W⋅m–2⋅nm–1)
- Column 3: Cumulative photon flux (cm–2⋅s–1)

## AM1.5d.csv

Downloaded from [PV Lighthouse](https://www2.pvlighthouse.com.au/resources/optics/spectrum%20library/spectrum%20library.aspx) on July 21st 2018

**Description**: This is the Air Mass 1.5 direct normal irradiance, calculated with SMARTS v 2.9.2 with inputs chosen per international standard IEC 60904-3-Ed2.

**Outputs** Integrated over the range  280–4000 nm:

- **Intensity**: 900,18710   W/m2
- **Photon flux**: 3,9855336E+17   cm–2⋅s–1
- **Photon current**: 63,856220   mA/cm2

## AM1.5g.csv

Downloaded from [PV Lighthouse](https://www2.pvlighthouse.com.au/resources/optics/spectrum%20library/spectrum%20library.aspx)_ on July 21st 2018

**Description**: This is the Air mass 1.5 global tilted irradiance, calculated with SMARTS v 2.9.2 with inputs chosen per international standard IEC 60904-3-Ed2. Note that this standard calls for the SMARTS output values for the spectral irradiance to be multiplied by a normalisation factor (0.9971) "in order to get an integrated irradiance of 1000 W/m2 in the wavelength range 0 to infinity."

**Outputs** Integrated over the range 280–4000 nm:

- **Intensity**: 997,54153   W/m2
- **Photon flux**: 4,2907423E+17   cm–2⋅s–1
- **Photon current**: 68,746273   mA/cm2

## QFlash.csv

Downloaded from [PV Lighthouse](https://www2.pvlighthouse.com.au/resources/optics/spectrum%20library/spectrum%20library.aspx)_ on July 21st 2018

**Description**: This is the Spectral irradiance of the Xenon flash (unfiltered) typically used to illuminate samples during photoconductance lifetime measurement (eg. with a Sinton WCT tool).

**Outputs**: Integrated over the range 251–1200 nm:

- **Intensity**: 751,27626  W/m2
- **Photon flux**: 2,8978947E+17    cm–2⋅s–1
- **Photon current**: 46,430068     mA/cm2

## QFlash-IR.csv

Downloaded from [PV Lighthouse](https://www2.pvlighthouse.com.au/resources/optics/spectrum%20library/spectrum%20library.aspx)_ on July 21st 2018

**Description**: This is the    Spectral irradiance (through a high pass filter) of the Xenon flash typically used to illuminate samples during photoconductance lifetime measurement (eg. with a Sinton WCT tool).

**Outputs**: Integrated over the range 251–1200 nm:

- **Intensity**: 632,63091  W/m2
- **Photon flux**: 2,8977775E+17    cm–2⋅s–1
- **Photon current**: 46,428190     mA/cm2


## Refractive indexes

Files contained in data folder: `data/refractive_indexes`

### Si.csv

Refractive index data of Silicon downloaded from [PV Lighthouse](https://www2.pvlighthouse.com.au/resources/photovoltaic%20materials/refractive%20index/refractive%20index.aspx)

**Description**: This is a list of the complex refractive index for Si in function of the
of the wave length.

Reference

[Gre08] M. Green, 'Self-consistent optical parameters of intrinsic silicon at 300K including temperature coefficients', Solar Energy Materials & Solar Cells 92, pp. 1305–1310, 2008. 

- Row 1: Wavelength
- Row 2: n (real part of refractive index)
- Row 3: k (imaginary part of refractive index: Exctinction coefficient)
- Row 4: alpha (cm-1) absorption coefficient

### Air.csv

**Description**: This is the complex refractive index for Air in function of
the wave length.

**Downloaded from** [PV Lighthouse](https://www2.pvlighthouse.com.au/resources/photovoltaic%20materials/refractive%20index/refractive%20index.aspx)

Reference:

[Pal85d]    E. Palik, Handbook of Optical Constants of Solids Vol I, Academic Press, Orlando, pp. 577–580, 1985. 

- Row 1: Wavelength
- Row 2: n (real part of refractive index)
- Row 3: k (imaginary part of refractive index: Exctinction coefficient)
- Row 4: alpha (cm-1) absorption coefficient
