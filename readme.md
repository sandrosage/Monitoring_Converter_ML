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