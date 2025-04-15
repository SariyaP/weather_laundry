import math

def calc(temp, humid, wind, width):
    # Convert wind speed from km/h to m/s
    wind = wind / 3.6
    kelvin = temp + 273.15

    # Absolute humidity (AH) in kg/kg
    AH = ((0.000002 * temp**4) + (0.0002 * temp**3) + (0.0095 * temp**2) + (0.337 * temp) + 4.9034) * (humid / 100.0)
    AH /= 1000

    ground_pressure = 101325  # in Pascals
    area = 1  # drying area in m^2

    # Saturation vapor pressure and humidity ratio
    pws = math.exp(77.345 + 0.0057 * kelvin - 7235.0 / kelvin) / (kelvin ** 8.2)
    saturation_humidity = (0.62198 * pws) / (ground_pressure - pws)

    # Alternate form of absolute humidity for gs
    BH = ((0.000002 * temp**4) + (0.0002 * temp**3) + (0.0095 * temp**2) + (0.337 * temp) + 4.9034) / 1000.0

    # Drying speed in kg/hour (gs)
    gs = (25 + 19 * wind) * area * BH * (1 - humid / 100.0)

    if gs <= 0:
        return float('inf')  # Avoid division by zero

    hours = (1 / gs) * width
    return math.ceil(hours)


def forecast_drying_time(temps, humids, winds, precipitations, width):
    total_hours = 0
    total_rain = 0
    max_wind = 0
    hour = 0

    while width > 0 and hour < len(temps):
        temp = temps[hour]
        humid = humids[hour]
        wind = winds[hour] / 2  # adjust for 1.5m height

        hours_needed = calc(temp, humid, wind, width)
        width -= width / hours_needed
        total_hours += 1
        total_rain += precipitations[hour]
        max_wind = max(max_wind, winds[hour])

        hour += 1

    if total_rain > 0.1:
        message = "It looks like it will rain before the laundry has a chance to dry. Consider waiting."
    elif max_wind > 12:
        message = "It will be windy. Use extra clothespins."
    else:
        message = "Drying conditions look good."

    return total_hours, message
