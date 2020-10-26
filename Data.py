import os
import zipfile
from pandas import read_json, read_csv, DataFrame, concat, to_datetime, concat
from sklearn.preprocessing import label_binarize
from datetime import datetime
from numpy.random import rand
import random
import numpy as np
import gensim


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
        print("\nReading data...")
        start_time = datetime.utcnow()
        list_of_items = os.listdir(directory)
        for elem in list_of_items:
            if os.path.splitext(elem)[1] != '.json':
                path = os.path.join(os.getcwd(), directory, elem)
                os.remove(path)

        # make sure all files are .json files
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

    def read_bodies(self, data, newspaper,save_bodies=True):
        # takes around 2 minutes 20 seconds on my Macbook Pro
        print("\nReading bodies...")
        start_time = datetime.utcnow()
        bodies = DataFrame(columns=['date', 'body', 'year'])

        for id in range(data.shape[0]):
            article = data.iloc[id]['articles']
            if article['newspaper'] == newspaper:
                dtime = to_datetime(article['date'])
                body = article['body']
                bodies = bodies.append(DataFrame(data=[[dtime, body, dtime.year]], columns=['date', 'body', 'year']))
        print("Done.", 'Time:', datetime.utcnow() - start_time)
        if save_bodies:
            print("Saving bodies to csv")
            filename = 'bodies' + newspaper.replace(" ", '') + '.csv'
            bodies.to_csv(filename)
        return bodies

    def read_saved_bodies(self, newspaper='all'):
        bodies=None
        newspaper = newspaper.replace(" ", "")
        if newspaper == 'all':
            bodies = read_csv('bodies.csv')
        elif newspaper == 'TheAustralian':
            bodies = read_csv('bodiesTheAustralian.csv')
        try:
            bodies = bodies.drop(columns=bodies.columns[0])
            bodies['year'] = bodies['year'].astype(int)
            bodies['date'] = to_datetime(bodies['date'])
            return bodies
        except FileNotFoundError:
            print(
                "Specified bodies .csv-file was not found..\nCheck if you are in the correct directory or construct them using the method read_bodies in the Data class")
            quit()

    def create_word_embeddings_input(self):
        print("\ncreating input for word embeddings. Writing to BigAss.txt")
        bodies = self.read_saved_bodies()

        with open("BigAss.txt", 'w+') as handle:
            # loop over all the rows in bodies
            for id in range(bodies.shape[0]):
                handle.write(bodies.iloc[id]['body'])
        handle.close()

    def read_embedding_model(self):
        print("Reading Our Embeddings...")
        path = os.path.join(os.getcwd(), 'wordEmb_project.bin')
        model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
        print("Done")
        return model

    def read_google_embeddings(self):
        print("Reading Google Embeddings...")
        path = os.path.join(os.getcwd(), 'GoogleNews-vectors-negative300.bin')
        model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
        print("Done")
        return model

    @staticmethod
    def one_hot_encode(labels):
        return label_binarize(labels, classes=list(set(labels)))

    def create_pattern(self, google_model, embeddings_model, body, label):

        embedding_struct = DataFrame()
        words = body.split()
        count = 0
        for word in set(words):
            try:
                embedding_struct[count] = np.append(embeddings_model.get_vector(word), label)
            except KeyError:
                # print(word, "\nnot in EmbeddingsModel-vectors")
                try:
                    # print("But", word, "is in GoogleNews-vectors")
                    embedding_struct[count] = np.append(google_model.get_vector(word), label)
                except KeyError:
                    # print(word, 'also not in GoogleNews-vectors')
                    embedding_struct[count] = np.append(rand(1, 300), label)
            count += 1
        return embedding_struct

    def create_input_data(self, newspaper, save_data=True):
        #read data and create data structure
        data = self.read_saved_bodies(newspaper='The Australian')
        input_data = DataFrame()

        # read in embeddings
        embeddings_model = self.read_embedding_model()
        google_model = self.read_google_embeddings()

        for id in range(data.shape[0]):
            print("row", str(id) + '/' + str(data.shape[0]))
            body = data.iloc[id]['body']
            year = data.iloc[id]['year']
            pattern = Data().create_pattern(google_model=google_model, embeddings_model=embeddings_model, body=body,
                                            label=year)
            if input_data.empty:
                input_data = pattern.transpose()
            else:
                input_data = concat([input_data, pattern.transpose()], ignore_index=True)
        if save_data:
            print("Saving input data for", newspaper)
            filename = 'input_data' + newspaper.replace(" ", '') + '.csv'
            input_data.to_csv(filename)
        return input_data
