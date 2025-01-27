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
            (10_099, 0.01),
            (23_942, 0.02),
            (37_788, 0.04),
            (52_455, 0.06),
            (66_295, 0.08),
            (338_639, 0.093),
            (406_364, 0.103),
            (677_275, 0.113),
            (math.inf, 0.123)
        ),
        standard_deduction=5_202
    ),
    married=TaxTable(
        table=(
            (20_198, 0.01),
            (47_884, 0.02),
            (75_576, 0.04),
            (104_910, 0.06),
            (132_590, 0.08),
            (677_278, 0.093),
            (812_728, 0.103),
            (1_354_550, 0.113),
            (math.inf, 0.133)
        ),
        standard_deduction=10_404
    )
)

social_security_tax_rules_2022, medicare_tax_rules_2022 = make_fica_rules(0.062, 147_000, 0.0145, 0.009)

state_2022 = {
    'ca': california_tax_rules_2022,
    'wa': zero_tax_rules,
    'tx': zero_tax_rules
}

ruleset = Ruleset(federal_tax_rules_2022, state_2022, social_security_tax_rules_2022, medicare_tax_rules_2022)
