"""
Calculation module
"""


def calc_price(room, persons, duration=None, begin=None, end=None):
    """
    Calc room price for period
    :param room: hotels.models.Room
    :param persons: adults + children
    :param duration: days
    :param begin: datetime
    :param end: datetime
    :return: integer
    """
    if begin and end and not duration:
        duration = (end - begin).days
    if not duration:
        raise AttributeError('Duration is not defined')
    price = duration * room.price
    if room.calculation_type == 'per_person':
        price = price * persons

    return price


def calc_commission(room, total=None, persons=None, duration=None, begin=None, end=None):
    """
    Calc partner income
    :param room: hotels.models.Room
    :param total: sum of order
    :param persons: adults + children
    :param duration: days
    :param begin: datetime
    :param end: datetime
    :return: dict {'property': 100, 'agent': 200, 'tariff_element': hotels.models.TariffElement}
    """
    if not total:
        total = calc_price(room, persons, duration, begin, end)

    tariff = room.property.get_tariff()
    el = tariff.get_element_for_sum(total)
    property_commission = total * el.commission / 100

    if property_commission < tariff.minimal_commission:
        property_commission = tariff.minimal_commission
    agent_commission = property_commission * el.agent_commission / 100

    return {'property': int(property_commission), 'agent': int(agent_commission), 'tariff_element': el}
