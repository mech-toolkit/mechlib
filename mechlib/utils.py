import time
import numpy as np

def add_heading(box_centre, headings):
    try:
        box_centre = float(box_centre)
        timestamp = int(time.time())
        headings.append((box_centre, timestamp))
    except (ValueError, TypeError):
        print("Invalid value or timestamp.")
        
def reverse_values(value, input_min, input_max):
    # Map value from range [input_min, input_max] to range [input_max, input_min]
    return int(
        input_max
        + ((value - input_min) * (input_min - input_max)) / (input_max - input_min)
    )

def get_exponential_moving_average(headings, smoothing_factor):
    ema = 0
    total_weight = 0
    for i, (value, timestamp) in enumerate(headings):
        weight = smoothing_factor ** (time.time() - timestamp)
        ema += weight * value
        total_weight += weight
    try:
        return ema / total_weight
    except ZeroDivisionError:
        return 240
    
def get_gaussian_intersect(bb_centre, motor):
    x_intersect = bb_centre
    print(f"Centre of BB: {x_intersect}")
    # Motor Velocity Control
    x = np.linspace(motor.img_width_min, motor.img_width_max, 1000)
    y = motor.velocity_min + (motor.velocity_max - motor.velocity_min) * np.exp(
        -((x - motor.mean) ** 2) / (2 * motor.turn_rate**2)
    )
    dydx = (
        -(x - motor.mean)
        * (motor.velocity_max - motor.velocity_min)
        * np.exp(-((x - motor.mean) ** 2) / (2 * motor.turn_rate**2))
        / motor.turn_rate**2
    )
    y_intersect = y[np.argmin(np.abs(x - x_intersect))]
    dydx_intersect = dydx[np.argmin(np.abs(x - x_intersect))]
    #
    left_servo = int(y_intersect if dydx_intersect > 0 else motor.velocity_max)
    right_servo = reverse_values(
        y_intersect if dydx_intersect < 0 else motor.velocity_max,
        motor.velocity_max,
        motor.velocity_min,
    )
    return left_servo, right_servo