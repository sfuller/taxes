import math
from typing import Tuple

from taxes.models import TaxRules


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
