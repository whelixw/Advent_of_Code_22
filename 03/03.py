def convert_char_to_int(char):
    if char.islower():
        return(ord(char)-96)
    else:
        return(ord(char)-38)

input_doc=open("03/input.txt")
sum1 = 0
sum2 = 0
current_backpack = input_doc.readline()
triple_buffer = list()
while current_backpack != "":
    compartment1 = current_backpack[int(len(current_backpack)/2):]
    compartment2 = current_backpack[:int(len(current_backpack)/2)]
    common_element = list(set(compartment1).intersection(set(compartment2)))[0]
    sum1 += convert_char_to_int(common_element)
    triple_buffer.append(current_backpack[:-1])
    current_backpack = input_doc.readline()
    if len(triple_buffer) == 3:
        #print(triple_buffer)
        common_element = list(set.intersection(set(triple_buffer[0]),set(triple_buffer[1]),set(triple_buffer[2])))[0]
        sum2 += convert_char_to_int(common_element)
        triple_buffer = list()

print(sum1)
print(sum2)