from Data import Data

class Experiments:

    def __init__(self):
        self.data_directory = "COP_filt3_sub"
        self.data_zipfilename = "COP.filt3.sub.zip"


    def experimentOne(self):
        # Data().unzip_COP_data(self.data_zipfilename)

        Data().read_jsons(self.data_directory)