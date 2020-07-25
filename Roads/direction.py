'''
direction.py
'''

from enum import Enum

class Dir(Enum):
    U = 8,
    R = 6,
    D = 2,
    L = 4,

    def r(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members): index = 0
        return members[index]

    def l(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) - 1
        if index < 0: index = len(members)-1
        return members[index]

    def rev(self):
        cls = self.__class__
        members = list(cls)
        index = (members.index(self) + len(members) + 2) % len(members)
        return members[index]

    def xy(self):
        #if self.value == Dir.U.value: return (0, -1)
        if self == Dir.U: return (0, -1)
        if self == Dir.D: return (0,  1)
        if self == Dir.L: return (-1, 0)
        if self == Dir.R: return ( 1, 0)
        return (0,0)


if __name__ == '__main__':
    for x in [Dir.R, Dir.U, Dir.L, Dir.D]:
        if x != x.r().l(): print ("Error")
        if x != x.l().r(): print ("Error")
        if x != x.rev().rev(): print ("Error")
        if x != x.rev().r().r(): print ("Error")
        if x != x.rev().l().l(): print ("Error")

    print ("self test fini")
    for d in [Dir.R, Dir.U, Dir.L, Dir.D]:
        x, y, = d.xy()
        print (d, x, y)

