import math

from taxes import TaxTable
from taxes.data import zero_tax_rules
from taxes.models import make_fica_rules, Ruleset, TaxRules

#
# 2024
#

federal_tax_rules_2024 = TaxRules(
    single=TaxTable(
        table=(
            (11_600, 0.10),
            (47_150, 0.12),
            (100_525, 0.22),
            (191_950, 0.24),
            (243_725, 0.32),
            (609_350, 0.35),
            (math.inf, 0.37)
        ),
        standard_deduction=14_600
    ),
    married=TaxTable(
        table=(
            (23_200, 0.10),
            (94_300, 0.12),
            (201_050, 0.22),
            (383_900, 0.24),
            (487_450, 0.32),
            (731_200, 0.35),
            (math.inf, 0.37)
        ),
        standard_deduction=29_200
    )
)

california_tax_rules_2024 = TaxRules(
    single=TaxTable(
        table=(
            (10_756, 0.01),
            (25_549, 0.02),
            (40_245, 0.04),
            (55_866, 0.06),
            (70_606, 0.08),
            (360_659, 0.093),
            (432_787, 0.103),
            (721_314, 0.113),
            (math.inf, 0.123)
        ),
        standard_deduction=5_540
    ),
    married=TaxTable(
        table=(
            (21_512, 0.01),
            (50_998, 0.02),
            (80_490, 0.04),
            (111_732, 0.06),
            (141_212, 0.08),
            (721_318, 0.093),
            (865_574, 0.103),
            (1_442_628, 0.113),
            (math.inf, 0.123)
        ),
        standard_deduction=11_080
    )
)

social_security_tax_rules_2024, medicare_tax_rules_2024 = make_fica_rules(
    social_security_rate=0.062,
    social_security_max_taxable=160_200,
    medicare_rate=0.0145,
    medicare_extra_rate= 0.009)

state_2024 = {
    'ca': california_tax_rules_2024,
    'wa': zero_tax_rules,
    'tx': zero_tax_rules
}

ruleset = Ruleset(federal_tax_rules_2024, state_2024, social_security_tax_rules_2024, medicare_tax_rules_2024)
