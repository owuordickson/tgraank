"""
@author: "Dickson Owuor"
@copyright: "Copyright (c) 2018 Université de Montpellier"
@credits: "Anne Laurent, Joseph Orero"
@license: "MIT"
@version: "1.0"
@email: "owuordickson@gmail.com"

This class prepares a dataset to be transformed by any step

"""

import csv
from PyCharm.algorithm.TimeLag import test_time
import numpy as np

class DataSet:

    def __init__(self,filename):

        #1. Test dataset
        ok,data = self.test_dataset(filename)

        if ok:
            print("Dataset Ok")
            self.data = data
            self.time_ok = ok
            self.multi_data = self.split_dataset()
        else:
            print("Dataset Error")
            self.data = data
            self.time_ok = ok
            self.multi_data = self.split_dataset()

    def split_dataset(self):
        #NB: Creates an (array) item for each column
        #NB: ignore first row and first column

        #1. get No. of columns (ignore 1st column)
        no_columns = (len(self.data[0]) - 1)

        #2. Create arrays for each gradual column item
        multi_data = [None] * (no_columns)
        for c in range(no_columns):
            multi_data[c] = []
            for i in range(1, len(self.data)):
                item = self.data[i][c + 1]  # because time is the first column in dataset (it is ignored)
                multi_data[c].append(item)

        # print(multi_dataset)
        return multi_data

    def transform_data(self,ref_column, step):
        #NB: Restructure dataset based on reference item

        #1. Load all the titles
        first_row = self.data[0]

        #2. Creating titles without time column
        no_columns = (len(first_row) - 1)
        title_row = [None] * no_columns
        for c in range(no_columns):
            title_row[c] = first_row[c + 1]

        ref_name = str(title_row[ref_column])
        title_row[ref_column] = ref_name + "**"
        new_dataset = [title_row]

        #3. Split the original dataset into gradual items
        gradual_items = self.multi_data

        #4. Transform the data using (row) n+step
        for j in range(len(self.data)):
            # time_diff = 0
            ref_item = gradual_items[ref_column]

            if j < len(ref_item) - step:
                init_array = [ref_item[j]]

                for i in range(len(gradual_items)):
                    if i < len(gradual_items) and i != ref_column:
                        gradual_item = gradual_items[i];
                        temp = [gradual_item[j + step]]
                        temp_array = np.append(init_array, temp, axis=0)
                        init_array = temp_array
                new_dataset.append(list(init_array))
                #return new_dataset

        return new_dataset;

    def get_representativity(self, step):

        #1. Get all rows minus the title row
        all_rows = (len(self.data) - 1)

        #2. Get selected rows
        sel_rows = (all_rows - step)

        #3. Calculate representativity
        if sel_rows > 0:
            rep = (sel_rows / all_rows)
            info = {"Transformation n+": step, "Representativity": rep, "Selected Rows": sel_rows,
                    "Total Rows": all_rows}
            return True, info
        else:
            return False, "Representativity is 0%"

    def get_max_step(self, minrep):
        #1. count the number of steps each time comparing the
        #calculated representativity with minimum representativity

        for i in range(len(self.data)):
            check, info = self.get_representativity(i + 1)
            if check:
                rep = info['Representativity']
                if rep < minrep:
                    return i
            else:
                return 0


    def test_dataset(self,filename):
        #NB: test the dataset attributes: time|item_1|item_2|...|item_n
        #return true and (list)dataset if it is ok

        #1. retrieve dataset from file
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            temp = list(reader)
        f.close()

        #2. Retrieve time in the first location
        raw_time = str(temp[1][0])

        #3. check if the retrieved time is valid
        try:
            time_ok,t_stamp = test_time(raw_time)
        except ValueError:
            return False,temp
        else:
            return time_ok,temp