cycle = 0
val = 1 #x
signal_strength_sum = 0
crt=""
verbose = True

def increase(cycle, val):
    global signal_strength_sum
    global crt
    global verbose
    cycle += 1



    if val-1 <= ((cycle-1) % 40) <= val+1:
        crt += "#"
    else:
        crt += "."
    if cycle > 20 and verbose:
        verbose = False
    elif verbose:
        print(cycle, val)
        print(crt)
    if cycle%40 == 0:
        print(cycle)
        #print(cycle*val)
        signal_strength_sum += cycle*val
        print(crt)
        crt = crt + "\n"

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
        cycle = increase(cycle, val)
        val = addx(val, int(line[1]))

print(signal_strength_sum)
print(crt)