import math
from typing import Tuple


class TaxRules(object):
    def __init__(self):
        self.table: Tuple[Tuple[float, float], ...] = tuple()
        self.standard_deduction = 0


federal_tax_rules_2018 = TaxRules()
federal_tax_rules_2018.table = (
    (9_525, 0.10),
    (38_700, 0.12),
    (82_500, 0.22),
    (157_500, 0.24),
    (200_000, 0.32),
    (500_000, 0.35),
    (math.inf, 0.37)
)
federal_tax_rules_2018.standard_deduction = 12000


federal_tax_rules_2019 = TaxRules()
federal_tax_rules_2019.table = (
    (9_700, 0.10),
    (39_475, 0.12),
    (84_200, 0.22),
    (160_725, 0.24),
    (204_100, 0.32),
    (510_300, 0.35),
    (math.inf, 0.37)
)
federal_tax_rules_2019.standard_deduction = 12200


california_tax_rules_2018 = TaxRules()
california_tax_rules_2018.table = (
    (8_544, 0.01),
    (20_255, 0.02),
    (31_969, 0.04),
    (44_377, 0.06),
    (56_085, 0.08),
    (286_492, 0.093),
    (343_788, 0.103),
    (572_980, 0.113),
    (math.inf, 0.123)
)
california_tax_rules_2018.standard_deduction = 4401


def make_fica_rules(
        social_security_rate: float,
        social_security_max_taxable: float,
        medicare_rate: float,
        medicare_extra_rate: float,
        ) -> Tuple[TaxRules, TaxRules]:

    social_security_rules = TaxRules()
    social_security_rules.table = (
        (social_security_max_taxable, social_security_rate),
        (math.inf, 0)
    )

    medicare_rules = TaxRules()
    medicare_rules.table = (
        (200_000, medicare_rate),
        (math.inf, medicare_rate + medicare_extra_rate)
    )

    return social_security_rules, medicare_rules


social_security_tax_rules_2018, medicare_tax_rules_2018 = make_fica_rules(0.062, 128_400, 0.0145, 0.009)
social_security_tax_rules_2019, medicare_tax_rules_2019 = make_fica_rules(0.062, 132_900, 0.0145, 0.009)


rulesets_by_year = {
    2018: (federal_tax_rules_2018, california_tax_rules_2018, social_security_tax_rules_2018, medicare_tax_rules_2018),

    # TODO: California has not released 2019 tax material at the time this was written
    2019: (federal_tax_rules_2019, california_tax_rules_2018, social_security_tax_rules_2019, medicare_tax_rules_2019)
}


def calculate_net(ruleset: Tuple[TaxRules, ...], gross: float) -> float:
    taxed = 0

    for rules in ruleset:
        net, _ = calculate_net_for_rules(rules, gross)
        taxed += gross - net

    return gross - taxed


def calculate_net_for_rules(rules: TaxRules, gross) -> Tuple[float, float]:
    taxable = gross - rules.standard_deduction

    bracket_index = 0
    taxed = 0
    last_max_bracket = 0

    while True:
        max_income, rate = rules.table[bracket_index]
        taxed += (min(taxable, max_income) - last_max_bracket) * rate

        if taxable < max_income:
            break

        last_max_bracket = max_income
        bracket_index += 1

    effective_rate = 1 - taxable - taxed / taxable
    return gross - taxed, effective_rate


def calculate_gross(ruleset: Tuple[TaxRules, ...], net: float):
    calculators: Tuple[Tuple[TaxRules, GrossTaxFactorState]]
    calculators = tuple((rules, GrossTaxFactorState()) for rules in ruleset)

    for _, state in calculators:
        state.previous_net = net
        state.previous_gross = net

    gross = net

    total_delta_tax = math.inf

    iteration = 0
    while total_delta_tax > 0.01 and iteration < 100:
        total_delta_tax = 0
        for rules, state in calculators:
            delta_gross = gross - state.previous_gross
            net = state.previous_net + delta_gross
            gross = calculate_gross_for_rules(rules, net)

            total_delta_tax += gross - state.previous_gross

            state.previous_gross = gross
            state.previous_net = net

        iteration += 1

    return gross


class GrossTaxFactorState(object):
    def __init__(self):
        self.previous_net = 0
        self.previous_gross = 0


def calculate_gross_for_rules(rules: TaxRules, net):
    net -= rules.standard_deduction

    taxed = 0
    bracket_index = 0
    last_max_income = 0

    while bracket_index < len(rules.table):
        max_income, rate = rules.table[bracket_index]

        bracket_start = last_max_income

        while bracket_start < max_income:
            taxable_income = min(net + taxed, max_income) - bracket_start
            bracket_start = net + taxed
            bracket_taxed = taxable_income * rate
            taxed += bracket_taxed

            if bracket_taxed < 0.01:
                break

        if net + taxed < max_income:
            break

        last_max_income = max_income
        bracket_index += 1

    return net + taxed + rules.standard_deduction
