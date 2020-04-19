class Base_Model(object):

    default_float = None
    default_int = None

    def __init__(self):
        return


    def to_percent_with_diff(self, initial_value: float, difference: float) -> float:
        change = initial_value + difference
        return ((change - initial_value) / initial_value) * 100


    def to_percent(self, initial_value: float, new_value: float) -> float:
        return ((new_value - initial_value) / initial_value) * 100