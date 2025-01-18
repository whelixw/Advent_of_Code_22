input_doc=open("05/input.txt")
#input_doc=open("05/test_input.txt")
lines = input_doc.readlines()






list_of_stacks = [[] for i in range(9)]

def crate_mover_1(command):
    extracted_ints = [int(s) for s in command.split() if s.isdigit()]
    amount, from_col, to_col = extracted_ints
    len_from = len(list_of_stacks[from_col-1])
    len_to = len(list_of_stacks[to_col-1])
    [list_of_stacks[to_col-1].append(i) for i in list_of_stacks[from_col-1][::-1][:amount]]
    list_of_stacks[from_col-1] = list_of_stacks[from_col-1][:len_from-amount:]
    #return list_of_stacks[from_col-1], list_of_stacks[to_col-1]

for i in range(7,-1,-1): # read stacks from bot to top
    level = lines[i]
    crates_for_level = lines[i][1::4]
    for crate_index in range(len(crates_for_level)):
        if crates_for_level[crate_index] != " ":
            list_of_stacks[crate_index].append(crates_for_level[crate_index])

for i in range(10,len(lines)):
    print(i)
    crate_mover_1(lines[i])

"".join([i[-1] for i in list_of_stacks])


def crate_mover_2(command):
    extracted_ints = [int(s) for s in command.split() if s.isdigit()]
    amount, from_col, to_col = extracted_ints
    len_from = len(list_of_stacks[from_col-1])
    len_to = len(list_of_stacks[to_col-1])
    #[list_of_stacks[to_col-1].append(i) for i in list_of_stacks[from_col-1][::-1][:amount]]
    [list_of_stacks[to_col - 1].append(i) for i in list_of_stacks[from_col - 1][len_from-amount:]]
    list_of_stacks[from_col-1] = list_of_stacks[from_col-1][:len_from-amount:]

for i in range(10,len(lines)):
    print(i)
    crate_mover_2(lines[i])

"".join([i[-1] for i in list_of_stacks])