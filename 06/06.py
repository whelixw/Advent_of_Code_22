input_doc=open("06/input.txt")
line = input_doc.readline()
#line = "bvwbjplbgvbhsrlpgdmjqwftvncz"
#line = "nppdvjthqldpwncqszvftbrmjlhg"
#line = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
#line = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
#line = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
#line = "mjqpqmgbljsphdztnvjfqwrcgsmlb"
pos = 0
while len(set(line[pos:pos+4])) != 4 :
    pos += 1
print(pos+4)

#or len(set(line[pos:pos+4]).intersection(set(line[0:3]))) == 0

pos = 0
while len(set(line[pos:pos+14])) != 14 :
    pos += 1

print(pos+14)