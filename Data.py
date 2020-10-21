import os
import zipfile
from pandas import read_json, read_csv, DataFrame, concat, to_datetime, Series
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime
from numpy import datetime64

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

    def read_data(self, directory):
        print("\nReading data..."); start_time = datetime.utcnow()
        list_of_items = os.listdir(directory)
        for elem in list_of_items:
            if os.path.splitext(elem)[1]!= '.json':
                path = os.path.join(os.getcwd(), directory, elem)
                os.remove(path)

        #make sure all files are .json files
        list_of_items = os.listdir(directory)
        data = None

        for elem in sorted(list_of_items):
            dt = read_json(os.path.join(os.getcwd(), directory, elem))
            if data is not None:
                frames = [data, dt]
                data = concat(frames)
            else:
                data = dt
        if data.columns[1] == 'collection_start':
            try:
                data[data.columns[1]] = to_datetime(data[data.columns[1]])
            except:
                print("Cannot convert data['collection_start'] to datetime... ")
            data = data.sort_values(data.columns[1])
        else:
            print("Something went wrong with sorting besed on collection start datetime")

        # return sorted data based on collection_start
        print("Done.", 'Time:', datetime.utcnow() - start_time)
        return data

    def read_bodies(self, data, save_bodies=True):
        #takes around 2 minutes 20 seconds on my Macbook Pro
        print("\nReading bodies..."); start_time = datetime.utcnow()
        bodies = DataFrame(columns=['date', 'body', 'year'])

        for id in range(data.shape[0]):
            article = data.iloc[id]['articles']
            dtime = to_datetime(article['date'])
            body = article['body']
            bodies = bodies.append(DataFrame(data=[[dtime, body, dtime.year]], columns=['date', 'body', 'year']), ignore_index=True)
        print("Done.", 'Time:', datetime.utcnow() - start_time)
        if save_bodies:
            print("Saving bodies to csv")
            bodies.to_json('bodies.csv')
        return bodies

    def read_saved_bodies(self):
        bodies = read_csv('bodies.csv')
        return bodies

    def vectorise_input(self):
        pass

    def vectorise_labels(self, labels):

        labels = OneHotEncoder


