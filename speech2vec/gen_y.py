import os
import numpy as np

def generate_y(folder):
    accents = {}
    counts = {}
    y = []
    index = 0
    # folder = '/media/enigmaeth/My Passport/sounds_wav/'

    for filename in os.listdir(folder):
        name = ''.join([i for i in filename if not i.isdigit()])
        name = name.split('_')[0]
        if name not in accents:
            accents[name] = index
            index += 1
            counts[name] = 0

        counts[name] += 1
        y.append(accents[name])

    print(counts)
    print(accents)

    sorted_counts = sorted(counts, key=counts.get, reverse=True)
    for r in sorted_counts:
        print(r, counts[r])

    return np.reshape(np.array(y), (len(y), 1))
