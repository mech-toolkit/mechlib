import time
from collections import deque
from dataclasses import dataclass


@dataclass
class Mech:
    name: str
    addr: tuple[str, int]
    received_response: bool = True
    timestamp: float = time.time()
    headings: deque =  deque([], maxlen=5)


class MechsList:
    Mechs: dict[str, Mech]

    def __init__(self):
        self.Mechs = {}

    def add_Mech(self, name, addr):
        if addr not in self.Mechs:
            self.Mechs[addr] = Mech(name=name, addr=addr)
        return self.Mechs[addr]

    def get_Mechs(self) -> dict[str, Mech]:
        return self.Mechs

    def get_Mech(self, addr) -> Mech | None:
        return self.Mechs.get(addr)
