Taxes
=====

This repo contains some tax formulas I wrote for fun.


It lacks a lot of features. Turns out taxes are complicated.
Right now it can handle tax calculations for single, standard deduction taking plebs like me.


Given a 'ruleset', it can calculate a net (post-tax) income based on a given gross income, and vice versa.
Each ruleset is a collection of rules for all types of taxes you may be subject to. 
This repo contains rulesets for the 2018 and 2019\* tax years, for federal, California, and FICA tax. 
It's not hard to define the tax rules for your own state, just create a new TaxRules object and fill in the tables and standard deduction fields.


\* The 2019 ruleset is not complete yet, as California has not released 2019 tax information at the time of writing.


I cannot guarantee the information in this repo is accurate, and therefore I cannot take any legal responsibility for trouble you may get yourself into by using this code. 
Not that I'd want to take legal responsibility for your taxes in the first place :) .


Have fun! Or not.. it _is_ taxes we're talking about here...


Example Usage
=============

```python
>>> import taxes
>>> ruleset = taxes.get_ruleset_for_year('2019')
>>> tables = ruleset.get_tables(state='ca', joint_federal=False, joint_state=False)
>>> taxes.calculate_net(tables, 120_000)
82769.35800000001
>>> taxes.calculate_gross(tables, 82769.35800000001)
119999.99809149538
```

