# Lo script viene usato per verificare se in un file di log <s_path> 
# vi sono exit node di TOR <k_path>

# file contenente le chiavi di ricerca
k_path = 'C:\\Users\\tor-exit-nodes.lst'

# file in cui ricercare
s_path = 'C:\\Users\\u_ex210831.log'

def trova_nel_file(k_path, s_path):
    # apriamo entrambi i file, con with non abbiamo bisogno di eseguire il close finale
    with open(k_path, 'r') as reader, open(s_path, 'r') as search:
        i = 0 # contatore per le corrispondenze
        for line in reader:
            l = line.replace('\n', '')
            # print(line, end='')
            for line1 in search:
                if l in line1:
                    i+=1
                    print(i, ' ', l, '--->', line1,  end='')
                    key = l
                # print(line1, end='')
            search.seek(0) # riporta all'inizio del file
        if i > 0:
            print(i, 'occorrenze di',key)
        else:
            print('Nessuna corrispondenza trovata!')

# end='' serve per impedire a Python di aggiungere una nuova riga al testo che
# viene stampato, quindi solo ciò che viene letto dal file.

trova_nel_file(k_path, s_path)