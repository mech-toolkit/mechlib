from dataclasses import dataclass


def remap(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


@dataclass
class Motor:
    speed: int
    img_width_min: int
    img_width_max: int  # Image width
    offset_left: int  # 
    offset_right: int  #
    center_pos: int  # Continuous Servo Centre Pos
    max_speed: int  # This is the max offset from the motor_center_pos
    turn_rate: int  # this controls the turn rate - higher equals slower
    slope_width: int

    @property
    def velocity_min(self):
        return remap(
            self.speed, 0, 100, self.center_pos, self.center_pos - self.max_speed
        )

    @property
    def velocity_max(self):
        return remap(
            self.speed, 0, 100, self.center_pos, self.center_pos + self.max_speed
        )

    @property
    def mean(self):
        return self.img_width_max / 2
