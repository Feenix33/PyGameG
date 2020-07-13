'''
ai.py

need up/down queues
need direction of travel
'''
from enum import Enum, auto

class ElevatorStates(Enum):
    REST = auto()
    CLOSE = auto()
    MOVE = auto()
    OPEN = auto()
    LOAD = auto()

class aiElevator:
    def __init__(self, constants, building, on_floor):
        self.building = building
        self.on_floor = on_floor
        self.state = ElevatorStates.REST
        self.stops = []
        self.timer = 0
        self.times = {
                ElevatorStates.CLOSE : constants['elev_tclose'],
                ElevatorStates.OPEN : constants['elev_topen'],
                ElevatorStates.LOAD : constants['elev_tload'],
                }


    def __repr__(self):
        return "aiElev owner={} stops=[{}]".format(
                self.owner.name, 
                ' '.join(str(e) for e in self.stops),
                *self.stops,
                )

    def update(self):
        if self.state == ElevatorStates.CLOSE:
            self.timer -= 1
            if self.timer <= 0:
                if len(self.stops) > 0:
                    self.state = ElevatorStates.MOVE
                else:
                    self.state = ElevatorStates.REST
                return

        elif self.state == ElevatorStates.MOVE:
            if len(self.stops) > 0:
                target = self.stops[0]
                if self.owner.py == target:
                    self.stops.pop(0)
                    self.state = ElevatorStates.OPEN
                    self.timer = self.times[self.state]
                elif self.owner.py < target:
                    self.owner.py += 1
                else:
                    self.owner.py -= 1
            else:
                self.state = ElevatorStates.REST

        elif self.state == ElevatorStates.OPEN:
            self.timer -= 1
            if self.timer <= 0:
                self.state = ElevatorStates.LOAD
                self.timer = self.times[self.state]

        elif self.state == ElevatorStates.LOAD:
            self.timer -= 1
            if self.timer <= 0:
                self.state = ElevatorStates.CLOSE
                self.timer = self.times[self.state]

        elif self.state == ElevatorStates.REST:
            if len(self.stops) > 0:
                self.state = ElevatorStates.MOVE




    def add_stop(self, floor_num):
        if floor_num > self.building.bldgc.nfloors:
            return
        ypos = self.building.bldgc.floor2ypos(floor_num)
        if ypos not in self.stops:
            self.stops.append(ypos)
            self.state = ElevatorStates.MOVE
