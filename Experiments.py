from Data import Data

class Experiments:

    def __init__(self):
        self.data_directory = "COP_filt3_sub"
        self.data_zipfilename = "COP.filt3.sub.zip"


    def experimentOne(self):
        # Data().unzip_COP_data(self.data_zipfilename)

        data = Data().read_data(self.data_directory)
        bodies = Data().read_bodies(data)
        bodies2 = Data().read_saved_bodies()

        if bodies == bodies2:
            print("Great success")