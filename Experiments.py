from Data import Data
import os

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


        # train_x = Data().r

        print("")