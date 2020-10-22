from Data import Data
import gensim
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
        bodies = Data().read_bodies(data)
        labels = Data().one_hot_encode(bodies['year'])


    def expCreateWordEmbeddingsInput(self):

        Data().create_word_embeddings_input()

    def expUseBinFile(self):
        path = os.path.join(os.getcwd(), 'wordEmb_project.bin')
        model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
        vocab = model.vocab.keys()
        wordsInVocab = len(vocab)
        print(wordsInVocab)
        print(model.similarity('this', 'is'))
        print(model.similarity('post', 'book'))
        print("bug stop")
