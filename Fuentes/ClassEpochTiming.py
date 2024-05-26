import numpy as np
import tensorflow
from tensorflow.keras.callbacks import Callback


class EpochTiming(Callback):

    def on_train_begin(self, logs=None):
        self._epochs_time = np.array([])  # arreglo para tiempo de cada época

    def on_train_end(self, logs=None):
        self.epochs = len(self._epochs_time)
        self.avg_epoch_time = self._epochs_time.mean()
        self.min_epoch_time = self._epochs_time.min()
        self.max_epoch_time = self._epochs_time.max()

    def on_epoch_begin(self, epoch, logs=None):
        self._start_time = tensorflow.timestamp()

    def on_epoch_end(self, epoch, logs=None):
        time = tensorflow.timestamp() - self._start_time
        self._epochs_time = np.append(self._epochs_time, time)
