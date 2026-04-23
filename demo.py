import os
import random
import numpy as np
import matplotlib.pyplot as plt

from scipy.io.wavfile import read
from algorithm import *

# ----------------------------------------------
# Run the script
# ----------------------------------------------
if __name__ == '__main__':

    # 1: Load the database
    with open('songs.pickle', 'rb') as handle:
        database = pickle.load(handle)

    # 2: Encoder
    nperseg=128
    noverlap=32
    min_distance=25
    time_window=1.
    freq_window=1500
    encoder = Encoding(nperseg=nperseg, noverlap=noverlap, 
      min_distance=min_distance,
      time_window=time_window, 
      freq_window=freq_window)
      
   
    # 3: Randomly get an extract from one of the songs of the database
    songs = [item for item in os.listdir('./samples') if item[:-4] != '.wav']
    song = random.choice(songs)
    print('Selected song: ' + song[:-4])
    filename = './samples/' + song

    fs, s = read(filename)
    #tstart = np.random.randint(20, 90)
    #On modifie la définition de tstart pour éviter de récupérer des extrait de moins de 10 secondes voir vide
    song_duration = len(s) / fs
    max_start = max(1, int(song_duration - 10))
    tstart = np.random.randint(0, max_start)
    tmin = int(tstart*fs)
    duration = int(10*fs)

    # 4: Use the encoder to extract a signature from the extract
    encoder.process(fs, s[tmin:tmin + duration])
    hashes = encoder.hashes

    # 5: TODO: Using the class Matching, compare the fingerprint to all the 
    # fingerprints in the database
    un_mauvais_morceau_affiche = False

    for item in database:
        # On utilise la classe Matching pour comparer l'extrait (hashes) 
        # avec le morceau actuel de la boucle (item['hashcodes'])
        matcher = Matching(hashes1=hashes, hashes2=item['hashcodes'])
        if len(matcher.matching) > 0:
            # CAS 1 : C'est le BON morceau
            if item['song'] == song[:-4]:
                print(f"\n--- VRAI MORCEAU ({item['song']}) ---")
                matcher.display_scatterplot()
                
            # CAS 2 : C'est un MAUVAIS morceau (on n'en affiche qu'un seul)
            elif not un_mauvais_morceau_affiche:
                print(f"\n--- MAUVAIS MORCEAU ({item['song']}) ---")
                matcher.display_scatterplot()
                un_mauvais_morceau_affiche = True





