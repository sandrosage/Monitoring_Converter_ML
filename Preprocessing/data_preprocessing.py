import pandas as pd 
import numpy as np
import os

class Preprocessing:

    #get the filename for storing the datafile
    def convert_filename(string):
        idx = string.find("_", string.find("_") + 1)
        string = string.lower()
        string = string[(idx+1):]
        string = string[:-4]
        return string

    #function for cleaning the textfiles
    def clean_textfile(source_folder, folder):
            for idx, filename in enumerate(os.listdir(source_folder+folder)):
                print(source_folder+folder+filename)
                infile = open(source_folder +folder +filename, 'r')
                file = infile.read()
                file = file.replace("[", "")
                file = file.replace("]", "")
                file = file.replace("'", "")
                data = file
                infile.close()
                print("File closed")
                # opening the file in write mode
                fout = open(source_folder +folder +filename, 'w')
                fout.write(data)
                print("File written")
                fout.close()

    #simple function for prepCon-function to set the skipRows-parameter
    def logic(index):
        if index % 2 == 0:
            return True
        return False

    #final preprocessing function
    def prepCon_textfile(path_to_textfile, column_names, folder, destination_folder):

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        if not os.path.exists(destination_folder + '/' + folder):
            os.makedirs(destination_folder + '/' + folder)

        # Delimiter
        data_file_delimiter = ','

        # The max column count a line in the file could have
        largest_column_count = 0

        # Loop the data lines
        with open(path_to_textfile, 'r') as temp_f:
            # Read the lines
            lines = temp_f.readlines()

            for l in lines:
                # Count the column count for the current line
                column_count = len(l.split(data_file_delimiter)) + 1
                
                # Set the new most column count
                largest_column_count = column_count if largest_column_count < column_count else largest_column_count

        # Generate column names (will be 0, 1, 2, ..., largest_column_count - 1)
        column_indexes = [i for i in range(0, largest_column_count)]

        # Read csv
        df = pd.read_csv(path_to_textfile, header=None, delimiter=data_file_delimiter, names=column_indexes, skiprows= lambda x: Preprocessing.logic(x))
        df = df[df[len(column_names)].isnull()]
        for i in range(len(column_names),largest_column_count):
            df.drop([i], axis=1, inplace=True)
        #df.rename(columns={0: "v_in", 1: 'current', 2: "v_out", 3: "temperature"}, inplace=True)
        df.reindex()
        df.dropna(inplace=True)
        df.columns = column_names
        df.to_csv ((destination_folder + "\\" + folder + "\\" + Preprocessing.convert_filename(path_to_textfile)+ ".csv"), index=None)
    

# not jet used functions for preprocess the dataframes, also implemented in the sent/other project
class Dataframe_processing:
    def calculate_values(df: pd.DataFrame):
        values_dict  = {"T_min":  df["temperature"].min(), "T_max":  df["temperature"].max(), "T_delta": (df["temperature"].max()-df["temperature"].min()), "Pow_mean":  df["power"].mean()}
        df_dictionary = pd.DataFrame([values_dict])
        return df_dictionary

    def make_subsets_without_shift(df: pd.DataFrame, size: int, status: str):
        #1.Step: Devide the Dataframe in subsets with size of range
        output_df = pd.DataFrame(columns=["T_min", "T_max", "T_delta", "Pow_mean"])
        current_size = size
        for i in range(0,int(len(df)/size)):
            new_size = current_size + size
            if i == 0:
                df_subset = df.iloc[:current_size, :]
                print(0, current_size, sep="-----")
            else:
                df_subset = df.iloc[(current_size+1): new_size, :]
                print((current_size+1), new_size, sep="-----")
                current_size = new_size
            
            #2.Step: Calculate power, power_mean, temperature_max, temperature_min for each subset
            #        and transform it back into an dataframe
            df_subset["power"] = df_subset['current'] * df_subset['v_out']
            df_dictionary = Dataframe_processing.calculate_values(df_subset)
            
            #3.Step: merge the subsets back to one dataframe
            output_df = pd.concat([output_df, df_dictionary], ignore_index=True)
            
        output_df["status"] = status
        return output_df

    def make_subsets_with_shift(df: pd.DataFrame, size: int, status: str, shift: int):
    
        #1.Step: Devide the Dataframe in subsets with size of range
        output_df = pd.DataFrame(columns=["T_min", "T_max", "T_delta", "Pow_mean"])
        i = 0
        while (i+(size)) < len(df):
            df_subset = df.iloc[i:(i+size), :]
            print(i, size+i, sep="-----")
            i = i + shift
            #2.Step: Calculate power, power_mean, temperature_max, temperature_min for each subset
            #        and transform it back into an dataframe
            df_subset["power"] = df_subset['current'] * df_subset['v_out']
            df_dictionary = Dataframe_processing.calculate_values(df_subset)
            
            #3.Step: merge the subsets back to one dataframe
            output_df = pd.concat([output_df, df_dictionary], ignore_index=True)

        output_df["status"] = status
        return output_df
    
    def make_subsets(df: pd.DataFrame, size: int, status: str, shift: int):
        if shift:
            return Dataframe_processing.make_subsets_with_shift(df,size,status,shift)
        else:
            print("Unable shift-mode!")
            return Dataframe_processing.make_subsets_without_shift(df,size,status)
    
    def clean_dataframe(df: pd.DataFrame, max_Vin, min_Vin, max_temp, min_temp, max_Vout, min_Vout, max_current, min_current):
        #to keep it simple, it each operation is in one line
        df = df[(df["v_in"] >= min_Vin) & (df["v_in"] <= max_Vin)]
        df = df[(df["temperature"] >= min_temp) & (df["temperature"] <= max_temp)]
        df = df[(df["v_out"] >= min_Vout) & (df["v_out"] <= max_Vout)]
        df = df[(df["current"] >= min_current) & (df["current"] <= max_current)]
        return df