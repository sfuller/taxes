import math
import importlib
from taxes.models import TaxTable, Ruleset

# Note: Best way to get California docs is here: https://www.ftb.ca.gov/forms/Search/
# Look up the 540 Booklet.
# The in-site documents typically aren't on the site outside of PDF form until a few months into the year.
#
# FICA numbers can be found on the IRS's Publication 15.

zero_tax_rules = TaxTable(table=((math.inf, 0.0),), standard_deduction=0)


def get_ruleset_for_year(year: str) -> Ruleset:
    module = importlib.import_module('.'+year, __package__)
    return getattr(module, 'ruleset')
