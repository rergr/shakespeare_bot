import tensorflow as tf

import numpy as np
import os
import time

path_to_file = "../data_set/shakespeare.txt"

text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
vocab = sorted(set(text))


# Process the text
# turn the text into ids
ids_from_chars = tf.keras.layers.StringLookup(
    vocabulary=list(vocab), mask_token=None)

# turns the ids back into chars
chars_from_ids = tf.keras.layers.StringLookup(
        vocabulary=ids_from_chars.get_vocabulary(), invert=True, mask_token=None)

# all the ids !!
all_ids = ids_from_chars(tf.strings.unicode_split(text, 'UTF-8'))
ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids)

for ids in ids_dataset.take(10):
    print(chars_from_ids(ids).numpy().decode('utf-8'))


