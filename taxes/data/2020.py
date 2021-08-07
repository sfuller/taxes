import math

from taxes import TaxTable
from taxes.data import zero_tax_rules
from taxes.models import make_fica_rules, Ruleset, TaxRules

#
# 2020
#

federal_tax_rules_2020 = TaxRules(
    single=TaxTable(
        table=(
            (9_875, 0.10),
            (40_125, 0.12),
            (85_525, 0.22),
            (163_300, 0.24),
            (207_350, 0.32),
            (518_400, 0.35),
            (math.inf, 0.37)
        ),
        standard_deduction=12_400
    ),
    married=TaxTable(
        table=(
            (19_750, 0.10),
            (80_250, 0.12),
            (171_050, 0.22),
            (326_600, 0.24),
            (414_700, 0.32),
            (622_050, 0.35),
            (math.inf, 0.37)
        ),
        standard_deduction=24_800
    )
)

california_tax_rules_2020 = TaxRules(
    single=TaxTable(
        table=(
            (8_932, 0.01),
            (21_175, 0.02),
            (33_421, 0.04),
            (46_394, 0.06),
            (58_634, 0.08),
            (299_508, 0.093),
            (359_407, 0.103),
            (599_012, 0.113),
            (math.inf, 0.123)
        ),
        standard_deduction=4_601
    ),
    married=TaxTable(
        table=(
            (17_864, 0.01),
            (42_350, 0.02),
            (66_842, 0.04),
            (92_788, 0.06),
            (117_268, 0.08),
            (599_016, 0.093),
            (718_814, 0.103),
            (1_198_024, 0.113),
            (math.inf, 0.123)
        ),
        standard_deduction=9_202
    )
)

social_security_tax_rules_2020, medicare_tax_rules_2020 = make_fica_rules(0.062, 137_700, 0.0145, 0.009)

state_2020 = {
    'ca': california_tax_rules_2020,
    'wa': zero_tax_rules,
    'tx': zero_tax_rules
}

ruleset = Ruleset(federal_tax_rules_2020, state_2020, social_security_tax_rules_2020, medicare_tax_rules_2020)
