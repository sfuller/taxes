import math
from typing import Tuple, Dict


class TaxTable(object):
    def __init__(self,
                 table: Tuple[Tuple[float, float], ...],
                 standard_deduction: float = 0):
        self.table = table
        self.standard_deduction = standard_deduction


class TaxRules(object):
    def __init__(self, single: TaxTable, married: TaxTable):
        self.single = single
        self.married = married


def make_fica_rules(
        social_security_rate: float,
        social_security_max_taxable: float,
        medicare_rate: float,
        medicare_extra_rate: float,
        ) -> Tuple[TaxTable, TaxRules]:

    social_security_rules = TaxTable((
        (social_security_max_taxable, social_security_rate),
        (math.inf, 0)
    ))

    def make_medicare_table(threshold: float) -> TaxTable:
        return TaxTable((
            (threshold, medicare_rate),
            (math.inf, medicare_rate + medicare_extra_rate)
        ))

    medicare_rules = TaxRules(single=make_medicare_table(200_000), married=make_medicare_table(250_000))

    return social_security_rules, medicare_rules


class Ruleset(object):
    def __init__(self, federal: TaxRules, state: Dict[str, TaxRules], social_security: TaxTable, medicare: TaxRules):
        self.federal = federal
        self.state = state
        self.social_security = social_security
        self.medicare = medicare

    def get_tables(self, state: str, joint_federal: bool, joint_state: bool) -> Tuple[TaxTable, ...]:
        state_rules = self.state[state]
        federal_table = self.federal.married if joint_federal else self.federal.single
        medicare_table = self.medicare.married if joint_federal else self.medicare.single
        state_table = state_rules.married if joint_state else state_rules.married
        return federal_table, state_table, self.social_security, medicare_table
