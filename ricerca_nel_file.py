# apriamo il file da esaminare. Con with evitiamo il close alla fine
with open('C:\\Users\\u_ex210831.log', 'r') as reader:
    key = '114.119.147.205' # chiave da ricercare
    i = 0 # contatore per le corrispondenze
    # Legge e stampa l'intero file riga per riga
    for line in reader:
        if key in line:
            i+=1
            print(i,' ', key, ' ---> ',line, end='')
    if i > 0:
        print(i, 'occorrenze di',key)
    else:
        print('Nessuna corrispondenza trovata!')