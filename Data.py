import os
import zipfile
from pandas import read_json, DataFrame, concat, to_datetime

class Data:


    def unzip_COP_data(self, zipfilename):
        # Filebane should be : "COP.filt3.sub.zip"
        try:
            print("Unzipping files", zipfilename, '..')
            with zipfile.ZipFile(zipfilename, "r") as zip_ref:
                zip_ref.extractall(os.getcwd())
            print("Done")
        except FileNotFoundError:
            print("File", zipfilename, "was not found in directory.")

    def read_jsons(self, directory):

        list_of_items = os.listdir(directory)
        for elem in list_of_items:
            if os.path.splitext(elem)[1]!= '.json':
                path = os.path.join(os.getcwd(), directory, elem)
                os.remove(path)

        #made sure all files are .json files
        list_of_items = os.listdir(directory)
        first_read = True
        for elem in sorted(list_of_items):
            dt = read_json(os.path.join(os.getcwd(), directory, elem))
            if not first_read:
                frames = [data, dt]
                data = concat(frames)
            else:
                data = dt
                first_read = False
        if data.columns[1] == 'collection_start':
            try:
                data[data.columns[1]] = to_datetime(data[data.columns[1]])
            except:
                print("Cannot convert data['collection_start'] to datetime... ")
            data = data.sort_values(data.columns[1])
        else:
            print("Something went wrong with sorting besed on collection start datetime")

        # return sorted data based on collection_start
        return data