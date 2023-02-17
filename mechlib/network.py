import socket


# How we handle receiving UDP Data
def receive_udp(sock):
    data, addr = sock.recvfrom(1024)
    return data, addr


# How we handle sending UDP Data
def send_response(sock, addr, response_type):
    sock.sendto(response_type.encode(), addr)


def end_fight(sock, Mechs_list):
    for Mech in list(Mechs_list.get_Mechs().values()):
        print(f"Telling {Mech.name} @ {Mech.addr} to stop!")
        send_response(sock, Mech.addr, "90,90,0,STOP")


def lan_server(port):
    # listen on all available interfaces
    UDP_IP = "0.0.0.0"
    UDP_PORT = 6969

    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    return sock
