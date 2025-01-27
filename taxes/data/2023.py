import math

from taxes import TaxTable
from taxes.data import zero_tax_rules
from taxes.models import make_fica_rules, Ruleset, TaxRules

#
# 2023
#

federal_tax_rules_2023 = TaxRules(
    single=TaxTable(
        table=(
            (11_000, 0.10),
            (44_725, 0.12),
            (95_375, 0.22),
            (182_100, 0.24),
            (231_250, 0.32),
            (578_125, 0.35),
            (math.inf, 0.37)
        ),
        standard_deduction=13_850
    ),
    married=TaxTable(
        table=(
            (22_000, 0.10),
            (89_450, 0.12),
            (190_750, 0.22),
            (364_200, 0.24),
            (462_500, 0.32),
            (693_750, 0.35),
            (math.inf, 0.37)
        ),
        standard_deduction=27_700
    )
)

california_tax_rules_2023 = TaxRules(
    single=TaxTable(
        table=(
            (10_412, 0.01),
            (24_684, 0.02),
            (38_959, 0.04),
            (54_081, 0.06),
            (68_350, 0.08),
            (349_137, 0.093),
            (418_961, 0.103),
            (698_271, 0.113),
            (math.inf, 0.123)
        ),
        standard_deduction=5_363
    ),
    married=TaxTable(
        table=(
            (20_824, 0.01),
            (49_368, 0.02),
            (77_918, 0.04),
            (108_162, 0.06),
            (136_700, 0.08),
            (698_274, 0.093),
            (837_922, 0.103),
            (1_396_542, 0.113),
            (math.inf, 0.123)
        ),
        standard_deduction=10_726
    )
)

social_security_tax_rules_2023, medicare_tax_rules_2023 = make_fica_rules(0.062, 160_200, 0.0145, 0.009)

state_2023 = {
    'ca': california_tax_rules_2023,
    'wa': zero_tax_rules,
    'tx': zero_tax_rules
}

ruleset = Ruleset(federal_tax_rules_2023, state_2023, social_security_tax_rules_2023, medicare_tax_rules_2023)
