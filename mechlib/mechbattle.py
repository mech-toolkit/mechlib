from ultralytics import YOLO
import time
from mechlib.network import lan_server, receive_udp, send_response, end_fight
from mechlib import MechsList
from mechlib.motor import Motor
from mechlib.strategy import process_bot_image
import argparse
from pathlib import Path
import urllib.request


def motor_settings() -> Motor:
    motor = Motor(
        speed=39,  # 1 - 100
        img_width_min=0,
        img_width_max=480,  # Image width
        offset_left=0,  # -6
        offset_right=0,  # 2
        center_pos=90,  # Continuous Servo Centre Pos
        max_speed=35,  # This is the max offset from the motor_center_pos
        turn_rate=180,  # this controls the turn rate - higher equals slower
        slope_width=30,
    )
    return motor


def main(args):
    print("checking if model exists")
    if not Path(args.model).exists():
        if args.model == "yv8n_GC_20230205_1123.pt":
            print("Auto Downloading Default Model")
            url = "https://github.com/mech-toolkit/pretrained/releases/download/v0.0.1/yv8n_GC_20230205_1123.pt"
            urllib.request.urlretrieve(url, args.model)
        else:
            print("Model not found")
            return

    print("Loading model")
    model = YOLO(args.model)  # load a pmodel
    print("Model loaded")
    #
    # set-up a local lan server to serve any Mechs on the local wifi
    sock = lan_server(6969)
    # motor control setup values
    motor = motor_settings()

    countdown = 5
    fighters_needed_min = int(args.number)

    try:
        while True:
            # create an instance of the MechsList class
            Mechs_list = MechsList()
            print(f"Waiting for {fighters_needed_min} fighters to agree to fight!")
            for i in range(countdown, 0, -1):
                data, addr = receive_udp(sock)
                if addr:
                    # print(f'received message: {data} from {addr}')
                    Mech = Mechs_list.get_Mechs().get(addr)
                    if Mech is None:
                        Mech = Mechs_list.add_Mech(name=data.decode(), addr=addr)
                        print(f"{Mech.name} has signed up from {Mech.addr}")
                        send_response(sock, addr, "RFC")
                time.sleep(1)
                print(f"{i} seconds left to join!")
            if len(Mechs_list.get_Mechs().values()) >= fighters_needed_min:
                print(".......")
                print("The following are our next matches fighters")
                for Mech in list(Mechs_list.get_Mechs().values()):
                    print(f"{Mech.name}")
                print(".......")
                print("FIGHT!")
                print(".......")
                while True:
                    data, addr = receive_udp(sock)
                    if addr:
                        Mech = Mechs_list.get_Mech(addr)
                        if (
                            Mech is None
                        ):  # this will happen if an unknown Mech sends a message
                            print(f"Error: {addr} not found in Mechs_list")
                            continue
                        else:
                            print(
                                f"Received: {data.decode()} from {Mech.name} @ {addr}"
                            )
                        if data == b"ack":
                            Mech.received_response = True
                        if Mech.received_response:
                            #
                            # perform inference here and return a motion command
                            cmd = process_bot_image(Mech, model=model, motor=motor)
                            #
                            # this is where you send the motion command
                            print(f"Sending: {cmd} to {Mech.name} @ {addr}")
                            send_response(sock, addr, cmd)
                            Mech.received_response = False
                    time.sleep(0.1)
            else:
                print(".......")
                print(
                    f"Not enough fighters. Only {len(Mechs_list.get_Mechs().values())} signed up"
                )
                for Mech in list(Mechs_list.get_Mechs().values()):
                    print(f"{Mech.name}")
                print(f"We agreed to have a minimum of {fighters_needed_min}")
                print("Shutting down and getting out of here before the cops come!")
                print(".......")

    finally:
        print("Time is up")
        end_fight(sock, Mechs_list)
        sock.close()

    """ except Exception as e:
        print('Error:', e)
        sock.close() """


def start():
    parser = argparse.ArgumentParser(description="Example Mech Strategy Server")
    parser.add_argument(
        "-n", "--number", type=str, help="Number of Fighters expected.", default=0
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="Model to use.",
        default="yv8n_GC_20230205_1123.pt",
    )

    args = parser.parse_args()

    if args.number == 0:
        args.number = input("Number of Robots (can be set e.g. -n 2)? ")

    main(args)


if __name__ == "__main__":
    start()
