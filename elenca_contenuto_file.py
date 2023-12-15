with open('file_di_input', 'r') as reader:
    for line in reader.readlines():
        print(line, end='')

# The end='' is to prevent Python from adding an additional newline to the text that 
# is being printed and only print what is being read from the file.
