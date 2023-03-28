# Description:

## Introduction:

### Data Acquisition:
#### Static Data:
For the static data generation we tested the below dcdc-Converters. They were all tested with different loads (0A, 1A, 2A, 3A, 4A, 5A, 6A). Communication: 115200 kbps UART, delay(2) excluded. Every recording had a duration of 30 minutes. We also measured the room temperature to have a reference value.

    We used three different dcdc-Converter:
        - DCHY2400-08 (Normal)
        - DCHY2400-15 (manipulated with Drossel)
        - DCHY2400-12 (manipulated with Mosfets)

    Attributes of dcdc-Converter:
        - On-Board temperature
        - input voltage
        - output voltage
        - output current

   
For the recording an input voltage of 24V was used. The measurements were determined with a Arduino UNO through I2C (100 kHz) and sent to a Raspberry PI 4 with UART (baudrate: 115200). 

#### Audio Recordings:

For the audio amplifier a "Conrad Components Stereo-Verstärker Bausatz 9 V/DC, 12 V/DC, 18 V/DC 35 W 2 Ω" with 2 x 35 W NF-Verstärker was used. The input voltage for the amplifier was 12V. The resistor load is 2.5 Ω.

For the audio signal a normal pc/laptop which played a MP3-File was used.
#### Steps:
##### 1. Data recording/generation for "NORMAL"-dcdc
    data for every song(3) was recorded thrice and labeled as V1, V2, V3
##### 2. Data recording/generation for "DROSSEL"-dcdc
    data for every song(3) was recorded thrice and labeled as V1, V2, V3
##### 3. Data recording/generation for "MOSFET"-dcdc
    data for every song(3) was recorded thrice and labeled as V1, V2, V3

#### Songs:
    Labeled as NG <--- Rick Astley - Never Gonna Give You Up: https://www.youtube.com/watch?v=dQw4w9WgXcQ

    Labeled as PIECES <--- AVAION, VIZE, Leony - Pieces: https://www.youtube.com/watch?v=mMbGQkvxVag
    
    Labeled as NEELIX <--- Neelix - The Twenty Five: https://www.youtube.com/watch?v=SPY1sGZN6hc

#### Code:
The code running on the Arduino is **``Arduino/i2c_data_transmission.ino``**. The implementation for the Raspberry Pi is located in **``Arduino/new_Get_Data_Ard.py``**. Both are new versions which no longer contain the transmission error.
### Preprocessing

Each recording is stored in a textfile at first. Then the textfile is cleaned and processed. Afterward, the files are converted into CSV files. The next processing step is to divide each CSV-file into subsets for the windowing method. This is achieved with a subset size of 5000 and a shift (samples in which the subsets are overlapping) of 100. The significant information is extracted of each subset:

- max. OB temperature
- min. OB temperature
- delta temperature
- power

Then the significant information of all subsets is merged togehter into a final CSV file, which is used for the training and testing data.
The diagram displays an overview of the processing phase:

![Sequencediagram](Ressources/Data_Preprocessing_Sequencediagram.png)

The processing for the audio recordings is quite the same, but you also add the song labels into the csv file.

### Installation:
#### using python 3.10.5

```python
# Create environment and upgrade package manager
python3 -m venv venv

# Activate venv
venv\Scripts\activate

# Install the requirements
pip install -r requirements.txt
```

### Machine Learning:
This section contains the whole machine learning phase based on Scikit-Learn, TensorFlow and Keras. The data is not provided in this repository. You can download it here (https://nextcloud.th-deg.de/apps/files/?dir=/Bachelor%20thesis%20-%20Data%20and%20models/DCDC&fileid=59568684) and add it to the workspace.
#### Scikit-Learn:
The four algorithms are used:

- DecionTreeClassifier()
- LinearSVC()
- KNeighborsClassifier()
- RandomForestClassifier()

For determining the highest score hyperparameter GridSearchCV is used for an exhaustive search of hyperparameters. This is encapsulated in the ``GridSearch`` class. 
The implemented code is located in **``/Machine_Learning/gridsearch_models.ipynb``**.

#### Deep Learning with TensorFlow and Keras:
Two different architectures are considered: 

- Dense Neural Network
- Convolutional Neural Network

During the process, it turns out that the DNN outperforms the CNN. The goal is to also compress and optimize the models with the *TensorFlow Model Optimization Toolkit*. So for the further steps, only the DNN model is considered. The four optimization techniques are:

- Quantization
- Pruning
- Weight clustering
- Combination of quantization-aware training and weight clustering

The comparison between both architectures is in **``/Machine_Learning/neural_network_comparison.ipynb``**. The fine-tuning for each optimization technique is in:

- **``Machine_Learning/quantization.ipynb``**
- **``Machine_Learning/weight_pruning.ipynb``**
- **``Machine_Learning/weight_clustering.ipynb``** (+ combination strategy)

The necessary functions for all the training, fine-tuning and evaluation steps are in the module **`Machine_Learning/Neural_Network_Tools`**. Include ``import Neural_Network_Tools.tools as nnt`` to use them.

*Sandro Sage; last updated: 23.03.2023*

