# default delimiter \t
cut -f2 "Notre-Dame de Paris songs.txt"

# concat with space
paste -d ' ' <(cut -f1 "Notre-Dame de Paris songs.txt") <(cut -f2 "Notre-Dame de Paris songs.txt")