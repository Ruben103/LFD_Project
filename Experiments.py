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
        Data().scrape_bodies(data)

    def experimentOne(self):
        data = Data().read_data(self.data_directory)
        bodies = Data().read_saved_bodies()
        for newspaper in ['The Australian', 'Sydney Morning Herald (Australia)', 'The Age (Melbourne, Australia)',
                          'The Times of India (TOI)', 'The Hindu',
                          'The Times (South Africa)', 'Mail & Guardian', 'The Washington Post', 'The New York Times']:
            Data().scrape_bodies(data=data, newspaper=newspaper)

    def expCreateWordEmbeddingsInput(self):
        Data().create_word_embeddings_input()

    def experimentCreateInput(self):
        # read in embeddings
        embeddings_model = Data().read_embedding_model()
        google_model = Data().read_google_embeddings()
        for newspaper in ['Mail & Guardian']:
            input_data = Data().create_input_data(newspaper=newspaper, embeddings_model=embeddings_model,
                                                  google_model=google_model)

    def experimentTheWashingtonPost(self):
        data = Data().read_input_data(newspaper='The Washington Post')

        print("")