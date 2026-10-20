# ch10_cc data table (what the problems use)

Source: `archetypes/data/substances.json` (the universal substance table) for the physical data; `archetypes/ch10_cc.py`, `LIQUIDS`, for the
coldest-temperature range. **Every value is the instructor's (NIST unless the record's source says otherwise). Convention: ΔHvap at the
normal boiling point.** A simulation must use the same convention and these values. "Coldest °C" is the lowest temperature a problem may
use, always above the melting point (tested). Density is given with the temperature it was measured at; blank = not yet supplied.

| liquid | ΔHvap at Tb, kJ/mol | normal boiling point, °C | normal melting point, °C | coldest °C a problem uses | density, g/mL | at °C | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| water | 40.66 | 100.0 | 0.0 | 5.0 | 0.998 | 20.0 | water |
| methanol | 35.2 | 64.6 | -97.2 | -10.0 |  |  | alcohol |
| ethanol | 38.6 | 78.4 | -114.2 | -10.0 | 0.789 | 20.0 | alcohol |
| 1-propanol | 41.4 | 97.2 | -126.2 | -10.0 |  |  | alcohol |
| 2-propanol | 40.0 | 82.4 | -89.5 | -10.0 |  |  | alcohol |
| 1-butanol | 43.3 | 117.5 | -89.6 | -10.0 |  |  | alcohol |
| acetone | 29.1 | 56.2 | -95.4 | -20.0 | 0.791 | 20.0 | ketone |
| diethyl ether | 26.5 | 34.6 | -116.3 | -30.0 | 0.713 | 20.0 | ether |
| pentane | 25.8 | 36.1 | -129.8 | -30.0 | 0.626 | 20.0 | alkane |
| hexane | 28.9 | 68.8 | -95.4 | -10.0 |  |  | alkane |
| heptane | 32.0 | 98.4 | -90.6 | 10.0 |  |  | alkane |
| cyclohexane | 29.6 | 80.8 | 6.6 | 10.0 |  |  | cycloalkane |
| benzene | 30.8 | 80.1 | 5.5 | 10.0 |  |  | aromatic hydrocarbon |
| toluene | 33.2 | 110.7 | -95.0 | 20.0 |  |  | aromatic hydrocarbon |
| chloroform | 29.2 | 61.2 | -63.6 | -10.0 |  |  | haloalkane |
| carbon tetrachloride | 30.0 | 76.7 | -22.9 | 0.0 |  |  | haloalkane |
| ethyl acetate | 31.0 | 77.1 | -83.6 | 0.0 |  |  | ester |
| 2-butanol | 40.8 | 98.9 | -114.7 | -10.0 |  |  | alcohol |
| isobutyl alcohol | 41.8 | 107.7 | -108.0 | -10.0 |  |  | alcohol |
| tert-butyl alcohol | 39.1 | 82.4 | 25.1 | 26.0 |  |  | alcohol |
| dichloromethane | 28.06 | 39.9 | -96.5 | -30.0 | 1.326 | 20.0 | haloalkane |
| CFC-11 | 25.2 | 23.8 | -111.0 | -30.0 | 1.488 | 20.0 | chlorofluorocarbon |
| HFE-7000 | 28.4 | 34.2 | -122.5 | -30.0 | 1.4 | 25.0 | hydrofluoroether |

Pressure units the problems use: atm and torr (mmHg accepted when typed); never kPa (instructor, 9 Oct 2026). R = 8.314 J/(mol·K).
A simulation may show a liquid's curve only between its melting point and its boiling point plus a margin; below the melting point there is no liquid.

Problems for the Rubbing Alcohol Chill opener draw methanol, ethanol and 2-propanol (instructor, 10 Oct: the alcohols clearly more volatile than water).
