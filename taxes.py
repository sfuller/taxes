import math
from typing import Tuple


class TaxRules(object):
    def __init__(self):
        self.table: Tuple[Tuple[float, float], ...] = tuple()
        self.standard_deduction = 0
        self.max_taxable_income = math.inf


federal_tax_rules_2018 = TaxRules()
federal_tax_rules_2018.table = (
    (9525, 0.10),
    (38700, 0.12),
    (82500, 0.22),
    (157500, 0.24),
    (200000, 0.32),
    (500000, 0.35),
    (math.inf, 0.37)
)
federal_tax_rules_2018.standard_deduction = 12000


federal_tax_rules_2019 = TaxRules()
federal_tax_rules_2019.table = (
    (9700, 0.10),
    (39475, 0.12),
    (84200, 0.22),
    (160725, 0.24),
    (204100, 0.32),
    (510300, 0.35),
    (math.inf, 0.37)
)
federal_tax_rules_2019.standard_deduction = 12200


california_tax_rules_2018 = TaxRules()
california_tax_rules_2018.table = (
    (8544, 0.01),
    (20255, 0.02),
    (31969, 0.04),
    (44377, 0.06),
    (56085, 0.08),
    (286492, 0.093),
    (343788, 0.103),
    (572980, 0.113),
    (math.inf, 0.123)
)
california_tax_rules_2018.standard_deduction = 4401


def make_fica_rules(rate: float, max_taxable: float) -> TaxRules:
    rules = TaxRules()
    rules.table = ((math.inf, rate),)
    rules.max_taxable_income = max_taxable
    return rules


fica_tax_rules_2018 = make_fica_rules(0.0765, 128400)
fica_tax_rules_2019 = make_fica_rules(0.0765, 132900)


rulesets_by_year = {
    2018: (federal_tax_rules_2018, california_tax_rules_2018, fica_tax_rules_2018),

    # TODO: California has not released 2019 tax material at the time this was written
    2019: (federal_tax_rules_2019, california_tax_rules_2018, fica_tax_rules_2019)
}


def calculate_net(ruleset: Tuple[TaxRules, ...], gross: float) -> float:
    taxed = 0

    for rules in ruleset:
        net, _ = calculate_net_for_rules(rules, gross)
        taxed += gross - net

    return gross - taxed


def calculate_net_for_rules(rules: TaxRules, gross) -> Tuple[float, float]:
    gross -= rules.standard_deduction
    gross = min(gross, rules.max_taxable_income)

    bracket_index = 0
    taxed = 0
    last_max_bracket = 0

    while True:
        max_income, rate = rules.table[bracket_index]
        taxed += (min(gross, max_income) - last_max_bracket) * rate

        if gross < max_income:
            break

        last_max_bracket = max_income
        bracket_index += 1

    net = gross - taxed
    effective_rate = 1 - net / gross
    return net + rules.standard_deduction, round(effective_rate, 4)


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
        max_income = min(max_income, rules.max_taxable_income)

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
