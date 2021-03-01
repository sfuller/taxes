import math
from taxes.models import make_fica_rules, TaxRules, Ruleset

# Note: Best way to get California docs is here: https://www.ftb.ca.gov/forms/Search/
# Look up the 540 Booklet.
# The in-site documents typically aren't on the site outside of PDF form until a few months into the year.

# FICA numbers can be found on the IRS's Publication 15.


washington_tax_rules = TaxRules(table=((math.inf, 0.0),), standard_deduction=0)


#
# 2018
#
federal_tax_rules_2018 = TaxRules(
    table=(
        (9_525, 0.10),
        (38_700, 0.12),
        (82_500, 0.22),
        (157_500, 0.24),
        (200_000, 0.32),
        (500_000, 0.35),
        (math.inf, 0.37)
    ),
    standard_deduction=12_000)

california_tax_rules_2018 = TaxRules(
    table=(
        (8_544, 0.01),
        (20_255, 0.02),
        (31_969, 0.04),
        (44_377, 0.06),
        (56_085, 0.08),
        (286_492, 0.093),
        (343_788, 0.103),
        (572_980, 0.113),
        (math.inf, 0.123)
    ),
    standard_deduction=4_401)

social_security_tax_rules_2018, medicare_tax_rules_2018 = make_fica_rules(0.062, 128_400, 0.0145, 0.009)
state_2018 = {'ca': california_tax_rules_2018, 'wa': washington_tax_rules}


#
# 2019
#
federal_tax_rules_2019 = TaxRules(
    table=(
        (9_700, 0.10),
        (39_475, 0.12),
        (84_200, 0.22),
        (160_725, 0.24),
        (204_100, 0.32),
        (510_300, 0.35),
        (math.inf, 0.37)
    ),
    standard_deduction=12_200)

california_tax_rules_2019 = TaxRules(
    table=(
        (8_809, 0.01),
        (20_883, 0.02),
        (32_960, 0.04),
        (45_753, 0.06),
        (57_824, 0.08),
        (295_373, 0.093),
        (354_445, 0.103),
        (590_742, 0.113),
        (math.inf, 0.123)
    ),
    standard_deduction=4_537)

social_security_tax_rules_2019, medicare_tax_rules_2019 = make_fica_rules(0.062, 132_900, 0.0145, 0.009)
state_2019 = {'ca': california_tax_rules_2019, 'wa': washington_tax_rules}

#
# 2020
#
federal_tax_rules_2020 = TaxRules(
    table=(
        (9_875, 0.10),
        (40_125, 0.12),
        (85_525, 0.22),
        (163_300, 0.24),
        (207_350, 0.32),
        (518_400, 0.35),
        (math.inf, 0.37)
    ),
    standard_deduction=12_400)

california_tax_rules_2020 = TaxRules(
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
    standard_deduction=4_601)

social_security_tax_rules_2020, medicare_tax_rules_2020 = make_fica_rules(0.062, 137_700, 0.0145, 0.009)
state_2020 = {'ca': california_tax_rules_2020, 'wa': washington_tax_rules}

#
# Rulesets
#
rulesets_by_year = {
    2018: Ruleset(federal_tax_rules_2018, state_2018, social_security_tax_rules_2018, medicare_tax_rules_2018),
    2019: Ruleset(federal_tax_rules_2019, state_2019, social_security_tax_rules_2019, medicare_tax_rules_2019),
    2020: Ruleset(federal_tax_rules_2020, state_2020, social_security_tax_rules_2020, medicare_tax_rules_2020)
}
