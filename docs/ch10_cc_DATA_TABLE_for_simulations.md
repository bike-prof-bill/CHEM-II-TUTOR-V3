# ch10_cc data table (what the problems use)

Source: `archetypes/data/substances.json` (the universal substance table) for the physical data; `archetypes/ch10_cc.py`, `LIQUIDS`, for the coldest-temperature range. **Every value is the instructor's, from the NIST Chemistry WebBook, 9 Oct 2026.
Convention: ΔHvap at the normal boiling point.** A simulation must use the same convention and these values. The tutor models each
liquid's vapour pressure as a Clausius-Clapeyron line hung from its normal boiling point (1 atm) with the constant ΔHvap below.
"Coldest °C" is the lowest temperature a problem may use: the instructor's choice of range, always above the melting point (tested).

| liquid | ΔHvap at Tb, kJ/mol | normal boiling point, °C | normal melting point, °C | coldest °C a problem uses |
| --- | --- | --- | --- | --- |
| water | 40.66 | 100.0 | 0.0 | 5.0 |
| methanol | 35.2 | 64.6 | -97.2 | -10.0 |
| ethanol | 38.6 | 78.4 | -114.2 | -10.0 |
| 1-propanol | 41.4 | 97.2 | -126.2 | -10.0 |
| 2-propanol | 40.0 | 82.4 | -89.5 | -10.0 |
| 1-butanol | 43.3 | 117.5 | -89.6 | -10.0 |
| acetone | 29.1 | 56.2 | -95.4 | -20.0 |
| diethyl ether | 26.5 | 34.6 | -116.3 | -30.0 |
| pentane | 25.8 | 36.1 | -129.8 | -30.0 |
| hexane | 28.9 | 68.8 | -95.4 | -10.0 |
| heptane | 32.0 | 98.4 | -90.6 | 10.0 |
| cyclohexane | 29.6 | 80.8 | 6.6 | 10.0 |
| benzene | 30.8 | 80.1 | 5.5 | 10.0 |
| toluene | 33.2 | 110.7 | -95.0 | 20.0 |
| chloroform | 29.2 | 61.2 | -63.6 | -10.0 |
| carbon tetrachloride | 30.0 | 76.7 | -22.9 | 0.0 |
| ethyl acetate | 31.0 | 77.1 | -83.6 | 0.0 |
| 2-butanol | 40.8 | 98.9 | -114.7 | -10.0 |
| isobutyl alcohol | 41.8 | 107.7 | -108.0 | -10.0 |
| tert-butyl alcohol | 39.1 | 82.4 | 25.1 | 26.0 |

Problems for the Rubbing Alcohol Chill opener draw methanol, ethanol, 1-propanol, 2-propanol.
Pressure units the problems use: atm, torr, kPa. Temperature units: K, °C. R = 8.314 J/(mol·K).
A simulation may show a liquid's curve only between its melting point and its boiling point plus a margin; below the melting point there is no liquid.
