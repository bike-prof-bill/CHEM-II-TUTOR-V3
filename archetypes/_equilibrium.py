"""Equilibrium arithmetic shared by chapter 13 (used by ch13_eq; ch13_ice keeps its own copy until it retires, so its shipped
content does not move). Every function takes a reaction record:
  species  symbols in reaction order        coef   stoichiometric coefficients
  side     -1 reactant, +1 product          active True for a species that appears in the expression (gas or solute), False for a
                                            pure solid or liquid (activity 1, left out: OpenStax 13.2)
  K        the constant                     dH_sign +1 endothermic forward, -1 exothermic, 0 unknown/declared none
  gas      True for a gas species (for a volume change)
A perturbation is a type and the species it names; `perturb_direction` gives the net direction a textbook student is expected to
predict (+1 forward, -1 reverse, 0 none). Types:
  add_reactant | add_product | remove_reactant | remove_product (species named) | add_common_ion (a product ion; same as add_product)
  heat | cool (needs dH_sign) | compress | expand (a volume change; by gas-mole count) | add_solid | add_liquid | add_inert_gas | catalyst (no shift)
"""
import math
from engine import round_sig

def quotient(rx, conc, exponents=True):
    num = den = 1.0; zero_bottom = False
    for i, s in enumerate(rx["side"]):
        if not rx["active"][i]: continue
        p = rx["coef"][i] if exponents else 1
        if s > 0: num *= conc[i] ** p
        else:
            if conc[i] == 0: zero_bottom = True
            den *= conc[i] ** p
    return None if zero_bottom else num / den

def multipliers_quotient(rx, conc):              # the named error: coefficients multiplied in, not used as exponents
    num = den = 1.0; zero_bottom = False
    for i, s in enumerate(rx["side"]):
        if not rx["active"][i]: continue
        v = rx["coef"][i] * conc[i]
        if s > 0: num *= v
        else:
            if conc[i] == 0: zero_bottom = True
            den *= v
    return None if zero_bottom else num / den

def half_ulp_rel(v, sf):                          # the relative half-unit in the last place of a value written to sf figures
    if v == 0: return 0.0
    return 0.5 * 10 ** (math.floor(math.log10(abs(v))) - sf + 1) / abs(v)

def equality_tolerance(rx, conc, sf):            # how far Q may sit from K and still be "equal to the figures given":
    tol = half_ulp_rel(rx["K"], sf)              # K's own last place, plus each active concentration's, propagated by its exponent
    for i, s in enumerate(rx["side"]):
        if rx["active"][i] and conc[i]: tol += rx["coef"][i] * half_ulp_rel(conc[i], sf)
    return tol

def direction(rx, conc, sf=3):                    # +1 forward, -1 reverse, 0 none. Q = K is judged to the figures given (the
    Q = quotient(rx, conc)                        # instructor, 13 Oct: 1.8e-10 has two significant figures; (1.3e-5)^2 = 1.7e-10 is equal to it)
    if Q is None: return -1
    if abs(Q - rx["K"]) <= equality_tolerance(rx, conc, sf) * rx["K"]: return 0
    return 1 if Q < rx["K"] else -1

def mass_action(rx, conc, d, x):
    num = den = 1.0
    for i, s in enumerate(rx["side"]):
        if not rx["active"][i]: continue
        v = conc[i] + s * d * rx["coef"][i] * x
        if s > 0: num *= v ** rx["coef"][i]
        else: den *= v ** rx["coef"][i]
    return num / den

def x_max(rx, conc, d):                           # the largest x before a consumed (active) species runs out
    return min(conc[i] / rx["coef"][i] for i, s in enumerate(rx["side"]) if s * d < 0 and rx["active"][i])

def solve_x(rx, conc, d):                         # bisection on the mass-action equation
    lo, hi = 0.0, x_max(rx, conc, d) * 0.999999
    for _ in range(300):
        m = 0.5 * (lo + hi)
        if (mass_action(rx, conc, d, m) < rx["K"]) == (d > 0): lo = m
        else: hi = m
    return 0.5 * (lo + hi)

def quadratic_roots(rx, conc, d):
    """Both roots of K = products/reactants when it is quadratic in x (every active coefficient 1, two on each side, or one each
    side with coefficient 2 on each): solved from the polynomial by the formula, independent of bisection."""
    a2 = a1 = a0 = 0.0
    # expand num - K*den as a polynomial in x by sampling (degree <= 2): three points
    f = lambda x: _poly_num(rx, conc, d, x) - rx["K"] * _poly_den(rx, conc, d, x)
    y0, y1, y2 = f(0.0), f(1.0), f(2.0)
    a2 = (y2 - 2 * y1 + y0) / 2.0; a1 = y1 - y0 - a2; a0 = y0
    if abs(a2) < 1e-12: return [-a0 / a1]
    disc = a1 * a1 - 4 * a2 * a0
    if disc < 0: return []
    r = math.sqrt(disc); return sorted([(-a1 - r) / (2 * a2), (-a1 + r) / (2 * a2)])
def _poly_num(rx, conc, d, x):
    v = 1.0
    for i, s in enumerate(rx["side"]):
        if s > 0 and rx["active"][i]: v *= (conc[i] + d * rx["coef"][i] * x) ** rx["coef"][i]
    return v
def _poly_den(rx, conc, d, x):
    v = 1.0
    for i, s in enumerate(rx["side"]):
        if s < 0 and rx["active"][i]: v *= (conc[i] - d * rx["coef"][i] * x) ** rx["coef"][i]
    return v
def polynomial_degree(rx):
    return max(sum(c for c, s, a in zip(rx["coef"], rx["side"], rx["active"]) if s > 0 and a), sum(c for c, s, a in zip(rx["coef"], rx["side"], rx["active"]) if s < 0 and a))

def gas_moles_change(rx):                         # products minus reactants, gas species only
    return sum(s * c for s, c, g in zip(rx["side"], rx["coef"], rx.get("gas", [False] * len(rx["coef"]))) if g)

def perturb_direction(rx, ptype, species=None):
    """The direction a change pushes the reaction (what the student should predict). Raises when the data cannot decide."""
    if species is not None and species not in rx["species"]: raise ValueError(f"{rx['id']}: perturbation names unknown species {species}")
    side = rx["side"][rx["species"].index(species)] if species else None
    active = rx["active"][rx["species"].index(species)] if species else None
    if ptype in ("add_reactant", "add_product", "remove_reactant", "remove_product", "add_common_ion"):
        if species is None: raise ValueError("perturbation needs a species")
        if not active: return 0                     # more or less of a pure solid or liquid changes nothing
        adding = ptype.startswith("add")
        return (-side) if adding else side          # add a reactant (side -1): forward (+1); add a product: reverse
    if ptype in ("heat", "cool"):
        if not rx.get("dH_sign"): raise ValueError(f"{rx['id']}: heat/cool perturbation needs dH_sign")
        return rx["dH_sign"] if ptype == "heat" else -rx["dH_sign"]
    if ptype in ("compress", "expand"):
        dn = gas_moles_change(rx)
        if dn == 0: return 0
        return (-1 if dn > 0 else 1) if ptype == "compress" else (1 if dn > 0 else -1)
    if ptype in ("add_solid", "add_liquid", "add_inert_gas", "catalyst"): return 0
    raise ValueError(f"unknown perturbation type {ptype}")

PERTURBATION_TYPES = ["add_reactant", "add_product", "remove_reactant", "remove_product", "add_common_ion", "heat", "cool",
                      "compress", "expand", "add_solid", "add_liquid", "add_inert_gas", "catalyst"]
