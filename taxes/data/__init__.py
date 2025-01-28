import math
import importlib
from taxes.models import TaxTable, Ruleset, TaxRules


# =====
# State Notes
# =====
#
# Note: Best way to get California docs is here: https://www.ftb.ca.gov/forms/Search/
# Look up the 540 Booklet.
# The in-site documents typically aren't on the site outside of PDF form until a few months into the year.
# Relevant parts of the 540 Booklet:
# - California Tax Rate Schedules, contains the tax brackets.
# - Instructions, contains the Standard Deduction ammount. (Ctrl+F for Standard Deduction)
#
# California's 540 documents show tax bracks as numbers in columns 'over' and 'but not over'.
# The second column means greater than, so we must +1 the ammount for our data, which expects greather than or equal.
#
# =====
# Federal Notes
# =====
#
# FICA numbers can be found on the IRS's Publication 15.
#
# Be careful with the IRS's website when looking up the federal tax rates! Especially earlier in the year!
# Sometimes the IRS will reference the year as the year when the taxes are due
# (E.g: The IRS may display 'rates for tax year 2023' and show 2022 tax rates)
#


zero_tax_table = TaxTable(table=((math.inf, 0.0),), standard_deduction=0)
zero_tax_rules = TaxRules(zero_tax_table, zero_tax_table)


def get_ruleset_for_year(year: int) -> Ruleset:
    module = importlib.import_module('.' + str(year), __package__)
    return getattr(module, 'ruleset')
