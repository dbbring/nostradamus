class Base_Model(object):

    default_float = 999599.59    # TODO swap out for null when done!!!
    default_int = -999

    def __init__(self):
        return


    def to_percent_with_diff(self, initial_value: float, difference: float) -> float:
        change = initial_value + difference
        return ((change - initial_value) / initial_value) * 100


    def to_percent(self, initial_value: float, new_value: float) -> float:
        return ((new_value - initial_value) / initial_value) * 100