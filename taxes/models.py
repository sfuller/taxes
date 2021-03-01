import math
from typing import Tuple, Dict


class TaxRules(object):
    def __init__(self,
                 table: Tuple[Tuple[float, float], ...],
                 standard_deduction: float = 0):
        self.table = table
        self.standard_deduction = standard_deduction


def make_fica_rules(
        social_security_rate: float,
        social_security_max_taxable: float,
        medicare_rate: float,
        medicare_extra_rate: float,
        ) -> Tuple[TaxRules, TaxRules]:

    social_security_rules = TaxRules((
        (social_security_max_taxable, social_security_rate),
        (math.inf, 0)
    ))

    medicare_rules = TaxRules((
        (200_000, medicare_rate),
        (math.inf, medicare_rate + medicare_extra_rate)
    ))

    return social_security_rules, medicare_rules


class Ruleset(object):
    def __init__(self, federal: TaxRules, state: Dict[str, TaxRules], social_security: TaxRules, medicare: TaxRules):
        self.federal = federal
        self.state = state
        self.social_security = social_security
        self.medicare = medicare

    def get_rules_for_state(self, state: str) -> Tuple[TaxRules, ...]:
        return self.federal, self.state[state], self.social_security, self.medicare
