from afc.image import get_bot_img, save_image
from afc.utils import add_heading, get_exponential_moving_average, get_gaussian_intersect
import numpy as np
import random


def we_punch(value):
    if value > 301:
        return 2
    else:
        return 0

def process_bot_image(bot, model, motor):
    bot_image = get_bot_img(bot.addr[0])
    results = model.predict(
        source=bot_image,
        conf=0.25,
        imgsz=480,
        stream=False,
        show=True,
        hide_labels=False,
        hide_conf=False,
        device="cpu",
    )
    #
    if False:
        save_image(bot_image)
    #
    print(f"Mechs found: {len(results[0])}")
    if len(results[0]):
        for result in results:
            divisions = 6
            x = int(result.boxes.xyxy[0][0])
            y = int(result.boxes.xyxy[0][1])
            x2 = int(result.boxes.xyxy[0][2])
            y2 = int(result.boxes.xyxy[0][3])
            w = x2 - x
            h = y2 - y
            x_centre = x2 - (w / 2)
            y_center = y2 - (h / 2)
            add_heading(x_centre, bot.headings)
            #
            # Perform motion control (decide motor velocitys)
            left_servo, right_servo = get_gaussian_intersect(x_centre, motor)
            #
            print(f"Motor Value left: {left_servo}")
            print(f"Motor Value right: {right_servo}")
            data = (
                str(left_servo)
                + ","
                + str(right_servo)
                + ","
                + str(we_punch(w))
                + ",RFC"
            )
            return data
            # print(f'Bounding Box Coords xyxy:{result.boxes.xyxy[0]}')   # box with xyxy format, (N, 4)
    else:
        # Didn't see anything so....
        # Let's look where we last saw it
        result = get_exponential_moving_average(bot.headings, 0.95)
        print(f'Where to look using past data: {result}')
        if (result > 240):
            # Turn Right
            return "90,83,0,RFC"
        elif (result < 240):
            # Turn Left
            return "83,90,0,RFC"
        else:
            # Reverse    
            commands = ["80,100,0,RFC"]
            return(commands[random.randint(0, len(commands)-1)])
