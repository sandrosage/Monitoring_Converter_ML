##############################################################################
# this code is only for checking wether the specific error still occurs or not
##############################################################################

import pandas as pd

arr = ["drossel", "normal", "mosfets"]
naming = ["DROSSEL", "NORMAL", "MOSFETS"]
output_file = open("error_occurances.txt", "w")     # file as table to show the occurances of error per file


# iterate through the directory an its subdirectories and files
for j in range(0,3):
    
    for i in range(0,6):
        text = "Data/Static_Data/" + arr[j] + "/STAT_" + naming[j] + "_" + str(i) + "A.txt"
        print(text)
        file = open(text, "r")

        # read content of file to string
        data = file.read()

        # get number of occurrences of the substring in the string
        occurrances = data.count("3068.")

        statictest = naming[j] + "_" + str(i) + "A" 
        occ = str(occurrances) + "\n"

        # store everything into the mentioned file
        output_file.write(statictest + ": " + occ)
        
        file.close()
output_file.close()