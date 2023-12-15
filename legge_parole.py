# legge il file e stampa un elemento per riga
inputFile = open("C:\\Users\\u_ex210831.log", "r")
for line in inputFile :
    wordList = line.split()
    for word in wordList :
        word = word.rstrip(".,?!")
        print(word)
        
inputFile.close()