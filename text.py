"""pos = []

for x in range(1,10,1):
    for y in range(1,10,1):
        pos.append((x,y))
print(pos[2][1])
pos2 = list(pos[1])
pos2.append(1)
print(pos2)"""
p1 = 1
p2 = 2
p3 = 3
p4 = 4
pos = []
pos.append((p1, p2))
pos.append((p3, p4))
print(pos)
pos1 = list(pos[0])
pos1.append(1)
print(pos1)