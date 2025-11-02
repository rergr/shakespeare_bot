import tensorflow as tf

import os
import time
from model import ShakespeareModel
import generate_text
from consts import SHAKESPEARE_PATH, ONE_STEP_DIR

text = open(SHAKESPEARE_PATH, 'rb').read().decode(encoding='utf-8')
vocab = sorted(set(text))

# process the text
# turn the text into ids
ids_from_chars = tf.keras.layers.StringLookup(
    vocabulary=list(vocab), mask_token=None)

# turns the ids back into chars
chars_from_ids = tf.keras.layers.StringLookup(
    vocabulary=ids_from_chars.get_vocabulary(), invert=True, mask_token=None)

# all the ids !!
all_ids = ids_from_chars(tf.strings.unicode_split(text, 'UTF-8'))
ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids)

# length of the sentence
seq_length = 100

# one sequences
sequences = ids_dataset.batch(seq_length + 1, drop_remainder=True)


# creates an input and label -> sequence: "Hello World"
# input: "Hello Worl"
# label: "ello World"
def split_input_target(sequence):
    input_text = sequence[:-1]
    target_text = sequence[1:]
    return input_text, target_text


# does this to a sequences of length seq_length
dataset = sequences.map(split_input_target)

# creating training batches
# batch size
BATCH_SIZE = 64

# buffer size to shuffle the dataset
# (TF data is designed to work with possibly infinite sequences,
# so it doesn't attempt to shuffle the entire sequence in memory. Instead,
# it maintains a buffer in which it shuffles elements).
BUFFER_SIZE = 10000

dataset = (
    dataset
    .shuffle(BUFFER_SIZE)
    .batch(BATCH_SIZE, drop_remainder=True)
    .prefetch(tf.data.experimental.AUTOTUNE))

##################################### USED FOR TRAINING #####################################

# length of the vocabulary in StringLookup Layer
vocab_size = len(ids_from_chars.get_vocabulary())

# the embedding dimension
embedding_dim = 256

# number of RNN units can use LSTM
rnn_units = 2048

model = ShakespeareModel(
    vocab_size=vocab_size,
    embedding_dim=embedding_dim,
    rnn_units=rnn_units)

for input_example_batch, target_example_batch in dataset.take(1):
    example_batch_predictions = model(input_example_batch)

# train model
# loss function returns logits
loss = tf.losses.SparseCategoricalCrossentropy(from_logits=True)

model.compile(optimizer='adam', loss=loss)

# directory where the checkpoints will be saved
checkpoint_dir = '../checkpoints'
# name of the checkpoint files
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}.weights.h5")

checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_prefix,
    save_weights_only=True)

# training
# epochs
EPOCHS = 1

history = model.fit(dataset, epochs=EPOCHS, callbacks=[checkpoint_callback])

one_step_model = generate_text.OneStep(model, chars_from_ids, ids_from_chars)

# sets states
states = None
next_char = tf.constant(['ROMEO'])
result = [next_char]

for _ in range(10):
    next_char, states = one_step_model.generate_one_step(next_char, states=states)
    result.append(next_char)

# save model
tf.saved_model.save(one_step_model, ONE_STEP_DIR)

##################################### USED FOR TRAINING #####################################
