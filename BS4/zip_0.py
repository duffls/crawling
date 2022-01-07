numbers = [1, 2, 3]
letters = ["A", "B", "C"]

for pair in zip(numbers, letters):
    print(pair)
#(1, 'A')
#(2, 'B')
#(3, 'C')

# = 같은 과정,결과
for i in range(3):
    pair = (numbers[i], letters[i])
    print(pair)

# unzip
numbers, letters = zip(*pair)

print(numbers, pair)