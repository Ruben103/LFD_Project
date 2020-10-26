from Data import Data
import os
from ClassifierService import Classifier
from Data import Data
from numpy import arange
from pandas import DataFrame, read_json
from sklearn.metrics import precision_score, recall_score, f1_score

class Experiments:

    def __init__(self):
        self.data_directory = "COP_filt3_sub"
        self.data_zipfilename = "COP.filt3.sub.zip"

    def settingUp(self):
        Data().unzip_COP_data(self.data_zipfilename)
        data = Data().read_data(self.data_directory)
        Data().read_bodies(data)

    def experimentOne(self):
        data = Data().read_data(self.data_directory)
        bodies = Data().read_bodies(data=data, newspaper='The Australian')


    def expCreateWordEmbeddingsInput(self):
        Data().create_word_embeddings_input()

    def experimentCreateInput(self):
        input_data = Data().create_input_data()


    def experimentClassifier(self, args):
        X_train, X_dev, X_test, Y_train, Y_dev, classes = Data().load_data()
        nb_features = X_train.shape[1]
        print(nb_features, 'features')
        nb_classes = Y_train.shape[1]
        print(nb_classes, 'classes')
        args.epochs = 100
        model = None
        metrics_per_set = DataFrame()

        model = Classifier(type='DropoutAdam', nb_features=nb_features, nb_classes=nb_classes,
                           epochs=args.epochs,
                           batch_size=64,
                           classes=classes, run_number=args.run, rate=0.4)
        model.fit(X_train=X_train, Y_train=Y_train, X_dev=X_dev, Y_dev=Y_dev)

        scores = model.predict(X_test=X_dev, X_dev=X_dev, Y_dev=Y_dev)
        metrics_per_set['scores'] = scores
        metrics_per_set['cols'] = ['Accuracy-score', 'Precision-score', 'Recall-score', 'F1-score']
        metrics_per_set.set_index('cols', drop=1)
        print(metrics_per_set)
        # train_x = Data().r

        print("")