import math

from taxes import TaxTable
from taxes.data import zero_tax_rules
from taxes.models import make_fica_rules, Ruleset, TaxRules

#
# 2021
#

federal_tax_rules_2021 = TaxRules(
    single=TaxTable(
        table=(
            (9_950, 0.10),
            (40_525, 0.12),
            (86_375, 0.22),
            (164_925, 0.24),
            (209_425, 0.32),
            (523_600, 0.35),
            (math.inf, 0.37)
        ),
        standard_deduction=12_550
    ),
    married=TaxTable(
        table=(
            (19_900, 0.10),
            (81_050, 0.12),
            (172_750, 0.22),
            (329_850, 0.24),
            (418_850, 0.32),
            (628_300, 0.35),
            (math.inf, 0.37)
        ),
        standard_deduction=25_100
    )
)

california_tax_rules_2021 = TaxRules(
    single=TaxTable(
        table=(
            (9_325, 0.01),
            (22_107, 0.02),
            (34_892, 0.04),
            (48_435, 0.06),
            (61_214, 0.08),
            (312_686, 0.093),
            (375_221, 0.103),
            (625_369, 0.113),
            (math.inf, 0.123)
        ),
        standard_deduction=4_803
    ),
    married=TaxTable(
        table=(
            (18_650, 0.01),
            (44_214, 0.02),
            (69_784, 0.04),
            (96_870, 0.06),
            (122_428, 0.08),
            (625_372, 0.093),
            (750_442, 0.103),
            (1_250_738, 0.113),
            (math.inf, 0.123)
        ),
        standard_deduction=9_606
    )
)

social_security_tax_rules_2021, medicare_tax_rules_2021 = make_fica_rules(0.062, 142_800, 0.0145, 0.009)

state_2021 = {
    'ca': california_tax_rules_2021,
    'wa': zero_tax_rules,
    'tx': zero_tax_rules
}

ruleset = Ruleset(federal_tax_rules_2021, state_2021, social_security_tax_rules_2021, medicare_tax_rules_2021)
