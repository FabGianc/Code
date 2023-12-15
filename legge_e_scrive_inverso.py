# legge il primo file e scrive sul secopndo in ordine inverso
d_path = 'C:\\Users\\u_ex210831.log'
d_r_path = 'C:\\Users\\prova.txt'
with open(d_path, 'r') as reader, open(d_r_path, 'w') as writer:
    appoggio = reader.readlines()
    writer.writelines(reversed(appoggio))
