cycle = 1
val = 1
signal_strength_sum = 0

def increase(cycle, val):
    global signal_strength_sum
    cycle += 1
    if cycle%40 == 20:
        print(cycle)
        print(cycle*val)
        signal_strength_sum += cycle*val
    return cycle

def addx(x, val):
    #print(x, val)
    val += x
    return val


input_doc = open("10/input.txt").readlines()


for line in input_doc:
    line = line.split(" ")
    if cycle > 200 and cycle < 221:
        print(val, cycle)
    if (len (line) == 1):
        cycle = increase(cycle, val)
    else:
        cycle = increase(cycle, val)
        val = addx(val, int(line[1]))
        cycle = increase(cycle, val)

print(signal_strength_sum)