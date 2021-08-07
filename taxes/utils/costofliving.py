import taxes
import taxes.data


def converter(current_state: str, current_gross: float, current_costs: float, new_state: str, new_costs: float) -> float:
    ruleset = taxes.data.get_ruleset_for_year('2020')
    current_net = taxes.calculate_net(ruleset.get_tables(current_state, False, False), current_gross)
    current_leftover = current_net - current_costs
    new_net = current_leftover + new_costs
    return taxes.calculate_gross(ruleset.get_tables(new_state, False, False), new_net)


def main():
    current_state = input('Current State: ').strip().lower()
    current_gross = float(input('Current Gross: '))
    current_costs = float(input('Current Costs: '))
    new_state = input('New State: ').strip().lower()
    new_costs = float(input('New Costs: '))
    print(f'New Gross: {converter(current_state, current_gross, current_costs, new_state, new_costs)}')


if __name__ == '__main__':
    main()
