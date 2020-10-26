







with open('UlaznaDatoteka.txt', 'r') as file:
    input_lines = [line.strip() for line in file]

regDefs = ""
while (input_lines[0][0:2] != "%X"):
    regDefs += input_lines[0]
    input_lines.pop(0)

print(regDefs)
