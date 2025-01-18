input_doc=open("02/input.txt")
match_to_score_1 = {"A X": 3+1,
                  "A Y": 6+2,
                  "A Z": 0+3,
                  "B X": 0 + 1,
                  "B Y": 3 + 2,
                  "B Z": 6 + 3,
                  "C X": 6 + 1,
                  "C Y": 0 + 2,
                  "C Z": 3 + 3
                  }
match_to_score_2 = {"A Y": 3+1,
                  "A Z": 6+2,
                  "A X": 0+3,
                  "B X": 0 + 1,
                  "B Y": 3 + 2,
                  "B Z": 6 + 3,
                  "C Z": 6 + 1,
                  "C X": 0 + 2,
                  "C Y": 3 + 3
                  }
score_sum = 0
score_sum_2 = 0
current_game = input_doc.readline()
while current_game != "":
    score_sum += match_to_score_1[current_game[:-1]]
    score_sum_2 += match_to_score_2[current_game[:-1]]
    current_game = input_doc.readline()
print(str(score_sum))
print(str(score_sum_2))