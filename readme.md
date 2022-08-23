# Description:

## Background:
Repository which processes the recordings/data of DCDC-Converter regarding V_in, V_out, Current, OnBoard temperature and room temperature. It contains all the necessary 
preprocessing function to clean the data, transform it into the right data format and stores the final dataset for train-, test- and validationset. Further it also includes the Machine Learning part.

![Sequencediagram](Ressources/Data_Preprocessing_Sequencediagram.png)
![Scatterplot](Ressources/scatterplot_audio_merged_dataset.png)

## Installation:
#### using python 3.10.5

```python
# Create environment and upgrade package manager
python3 -m venv venv

# Activate venv
venv\Scripts\activate

# Install the requirements
pip install -r requirements.txt
```

## Project Structure:

### 1. Layer of data preprocessing

In this layer the original, raw data files are processed and cleaned. This means that there can be faulty rows with more than expected features, or the syntax of the files has to be edited (f.ex. leave out the brackets [ ; ]). The data files are also transformed into the needed csv-format with the right column names in the header.
### 2. Layer of data preprocessing 

In the *converter_relevant_operations.ipynb* you can find the code for processing all the edited files regarding the shift and subset function. You have to devide the whole datafiles into subsets with a specific range to then afterwards calculate the significant features like:
    - mean of power
    - max. temperature
    - min. temperature
    - delta of temperature

```python
make_subsets(df: pd.DataFrame, size: int, status: str, shift: int, song_title: str)
```
In this function you have to specify the size of the subsets, the shift attribute if necessary, the status, so wether it is normal, drossel or mosfets and for the audio recordings you can set the song title if necessary. This means if you don't have audio recordings you can just leave out the song title parameter.