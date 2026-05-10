import tensorflow as tf
from keras.layers import (
    Bidirectional,
    Convolution2D,
    Dense,
    Dropout,
    Flatten,
    GRU,
    Input,
    Layer,
    LSTM,
    MaxPooling2D,
    RepeatVector,
)
from keras.models import Sequential


class Attention(Layer):
    def __init__(self, return_sequences=True, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.return_sequences = return_sequences

    def build(self, input_shape):
        self.W = self.add_weight(
            name="att_weight",
            shape=(input_shape[-1], 1),
            initializer="normal",
        )
        self.b = self.add_weight(
            name="att_bias",
            shape=(input_shape[1], 1),
            initializer="zeros",
        )
        super().build(input_shape)

    def call(self, x):
        e = tf.math.tanh(tf.matmul(x, self.W) + self.b)
        a = tf.nn.softmax(e, axis=1)
        output = x * a
        if self.return_sequences:
            return output
        return tf.reduce_sum(output, axis=1)

    def compute_output_shape(self, input_shape):
        if self.return_sequences:
            return input_shape
        return (input_shape[0], input_shape[-1])


def build_forecasting_model(recurrent="gru", input_shape=(10, 1, 1)):
    model = Sequential()
    model.add(Input(shape=input_shape))
    model.add(Convolution2D(32, (1, 1), activation="relu"))
    model.add(MaxPooling2D(pool_size=(1, 1)))
    model.add(Convolution2D(32, (1, 1), activation="relu"))
    model.add(MaxPooling2D(pool_size=(1, 1)))
    model.add(Flatten())
    model.add(RepeatVector(3))
    model.add(Attention(return_sequences=True, name="attention"))

    if recurrent == "lstm":
        recurrent_layer = lambda: Bidirectional(LSTM(64, activation="relu"))
    else:
        recurrent_layer = lambda: Bidirectional(GRU(64, activation="relu", reset_after=False))

    model.add(recurrent_layer())
    model.add(RepeatVector(3))
    model.add(recurrent_layer())
    model.add(Dense(units=256, activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(units=1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model
