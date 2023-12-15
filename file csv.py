# -*- coding: utf-8 -*-

import os
import glob
import pandas as pd
#seleziono la directory
os.chdir("C:\prova")

#ricerca tutti i file cs nella cartella / find all csv files in the folder
#utilizzo glob pattern matching -> extension = 'csv'
#salvo in una list -> tutti i file
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#print(all_filenames)

#combino tutti i file nella lista
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#esporto i file nel csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')