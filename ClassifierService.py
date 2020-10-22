from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import sgd, adam

class Classifier:

    def __init__(self, type, data):
        self.data = data
        self.type = type
        self.INPUT_DIM = self.get_INPUT_DIM(self.data)
        self.number_of_labels = self.get_number_of_labels(self.data)

        if self.type == 'MLP':
            self.MLP()

    def MLP(self):

        model = Sequential()
        model.add(Dense(input_shape=self.INPUT_DIM, units=600, activation='relu'))
        model.add(Dense(input_shape=600, units=300, activation='relu'))
        model.add(Dense(input_shape=300, units=self.number_of_labels, activation='softmax'))

        optimizer = sgd(momentum=0.9)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics='accuracy')
        self.model = model

    def fit_input(self, X, Y):

        self.model.fit(X, Y)

    def get_INPUT_DIM(self, data):
        pass

    def get_number_of_labels(self, data):
        return 25