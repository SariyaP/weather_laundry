import math

def calc_drying_hours(temp, humid, wind_kph, width=2):
    """
    Calculates the estimated drying time in hours for a material of a given width.

    Args:
        temp (float): Temperature in Celsius.
        humid (float): Relative humidity as a percentage (0-100).
        wind_kph (float): Wind speed in kilometers per hour.
        width (float, optional): The "width" or thickness factor of the material. Defaults to 2.

    Returns:
        int: The estimated drying time in whole hours (rounded up).
    """
    exp = 2.71828182846
    kelvin = temp + 273.15
    wind = wind_kph / 3.6

    AH = ((0.000002 * temp**4) + (0.0002 * temp**3) + (0.0095 * temp**2)
        + (0.337 * temp)
        + 4.9034
    ) * (humid / 100.0)
    AH = AH / 1000
    groundpressure = 101325
    area = 1  

    pws = (exp ** (77.345 + 0.0057 * kelvin - 7235.0 / kelvin)) / (kelvin**8.2)
    # sturation pressure
    saturationhumidity = (0.62198 * pws) / (groundpressure - pws)  # humidity ratio in saturated air (kg/kg) (kg H2O in kg Dry Air)
    gs = ((25 + 19 * wind) * (area) * (saturationhumidity - AH))
    BH = (
        (0.000002 * temp**4)
        + (0.0002 * temp**3)
        + (0.0095 * temp**2)
        + (0.337 * temp)
        + 4.9034
    ) / 1000.0
    gs = ((25 + 19 * wind) * (area) * BH * (1.0 - humid / 100.0))
    hours = 1 / gs
    hours = hours * width

    return math.ceil(hours) - 1
