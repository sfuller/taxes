import math
import importlib
from taxes.models import TaxTable, Ruleset, TaxRules

# Note: Best way to get California docs is here: https://www.ftb.ca.gov/forms/Search/
# Look up the 540 Booklet.
# The in-site documents typically aren't on the site outside of PDF form until a few months into the year.
#
# FICA numbers can be found on the IRS's Publication 15.
#
# Be careful with the IRS's website when looking up the federal tax rates! Especially earlier in the year!
# Sometimes the IRS will reference the year as the year when the taxes are due
# (E.g: The IRS may display 'rates for tax year 2023' and show 2022 tax rates)
#
# Resources to avoid:
# http://www.tax-rates.org/ consistently has incorrect information for California tax rates, year round. Avoid!
#


zero_tax_table = TaxTable(table=((math.inf, 0.0),), standard_deduction=0)
zero_tax_rules = TaxRules(zero_tax_table, zero_tax_table)


def get_ruleset_for_year(year: int) -> Ruleset:
    module = importlib.import_module('.' + str(year), __package__)
    return getattr(module, 'ruleset')
