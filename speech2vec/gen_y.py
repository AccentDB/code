import os
import numpy as np

def generate_y(folder):
    accents = {}
    counts = {}
    y = []
    index = 0

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

    np_y = np.reshape(np.array(y), (len(y), 1))

    Y_file = '../data/numpy_vectors/y_label_'+ (folder.split('/'))[-1]
    print("saving  labels to ", Y_file)
    np.save(Y_file, y)

folder = "../data/splits"
generate_y(folder)