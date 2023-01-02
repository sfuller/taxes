import math

from taxes import TaxTable
from taxes.data import zero_tax_rules
from taxes.models import make_fica_rules, Ruleset, TaxRules

#
# 2022
#

federal_tax_rules_2022 = TaxRules(
    single=TaxTable(
        table=(
            (10_275, 0.10),
            (41_775, 0.12),
            (89_075, 0.22),
            (170_050, 0.24),
            (215_950, 0.32),
            (539_900, 0.35),
            (math.inf, 0.37)
        ),
        standard_deduction=12_950
    ),
    married=TaxTable(
        table=(
            (20_550, 0.10),
            (83_550, 0.12),
            (178_150, 0.22),
            (340_100, 0.24),
            (431_900, 0.32),
            (647_850, 0.35),
            (math.inf, 0.37)
        ),
        standard_deduction=25_900
    )
)

california_tax_rules_2022 = TaxRules(
    single=TaxTable(
        table=(
            (8_809, 0.01),
            (20_883, 0.02),
            (32_960, 0.04),
            (45_753, 0.06),
            (57_824, 0.08),
            (295_373, 0.093),
            (354_445, 0.103),
            (590_742, 0.113),
            (1_000_000, 0.123),
            (math.inf, 0.133)
        ),
        standard_deduction=4_803
    ),
    married=TaxTable(
        table=(
            (17_618, 0.01),
            (41_766, 0.02),
            (65_920, 0.04),
            (91_506, 0.06),
            (115_648, 0.08),
            (590_746, 0.093),
            (708_890, 0.103),
            (1_000_000, 0.113),
            (1_181_484, 0.123),
            (math.inf, 0.133)
        ),
        standard_deduction=9_606
    )
)

social_security_tax_rules_2022, medicare_tax_rules_2022 = make_fica_rules(0.062, 147_000, 0.0145, 0.009)

state_2022 = {
    'ca': california_tax_rules_2022,
    'wa': zero_tax_rules,
    'tx': zero_tax_rules
}

ruleset = Ruleset(federal_tax_rules_2022, state_2022, social_security_tax_rules_2022, medicare_tax_rules_2022)
