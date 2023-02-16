import pandas as pd
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
import numpy as np
from keras.models import load_model
import time 
from keras.optimizers import Adam
from keras.losses import CategoricalCrossentropy, SparseCategoricalCrossentropy
from sklearn.preprocessing import MinMaxScaler
import os 
import zipfile
import tempfile

NUM_OF_CLASSES = 3

def prepare_train_test_dataset():
    train_data = pd.read_csv("train_data.csv")
    train_labels = pd.read_csv("train_labels.csv")
    test_data = pd.read_csv("test_data.csv")
    test_labels = pd.read_csv("test_labels.csv")
    whole_data = pd.concat([train_data, test_data])
    min_max_scaler = MinMaxScaler().fit(whole_data)
    train_data = min_max_scaler.transform(train_data)
    test_data = min_max_scaler.transform(test_data)
    train_labels = train_labels.status.astype('category').cat.codes.to_numpy()
    # train_labels = to_categorical(train_labels,NUM_OF_CLASSES)
    test_labels = test_labels.status.astype('category').cat.codes.to_numpy()
    # test_labels = to_categorical(test_labels,NUM_OF_CLASSES)
    return (train_data, train_labels),(test_data, test_labels)

def plot_history(history, epochs_size, file_name):
    loss_list = []
    accuracy_list = []
    history_keys = history.history.keys()
    for key in history_keys:
        if "loss" in key:
            loss_list.append(key)
        
        elif "acc" in key:
            accuracy_list.append(key)
        
        elif "accuracy" in key:
            accuracy_list.append(key)

    # print(loss_list)
    # print(accuracy_list)
    
    colors = list(mcolors.BASE_COLORS.keys())
    epochs = range(1, (epochs_size+1))
    fig, ax = plt.subplots(2, figsize=(20, 8))

    for key,color in zip(loss_list, colors):
        ax[0].plot(epochs ,history.history[key], str(color), label=str(key))

    ax[0].set_xlabel("Epochs")
    ax[0].set_ylabel("%")
    ax[0].set_title("Loss of Model:")
    ax[0].legend()

    for key,color in zip(accuracy_list, colors):
        ax[1].plot(epochs, history.history[key], str(color), label=str(key))
        
    ax[1].set_xlabel("Epochs")
    ax[1].set_ylabel("%")
    ax[1].set_title("Accuracy of Model:")
    ax[1].legend()

    # set the spacing between subplots
    plt.subplots_adjust(left=0.1,
                        bottom=0.1, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.4, 
                        hspace=0.8)

    plt.show()

    fig.savefig(file_name + ".pgf", backend="pgf", dpi=1000, bbox_inches="tight")

def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value

def print_best_history(history, training_time):
    history_dict = {}
    fnn_history_keys = history.history.keys()
    params_index = np.argmax(history.history["val_acc"])
    for key in fnn_history_keys:
        append_value(history_dict, key, history.history[key][params_index])
    history_dict["training_time"] = training_time
    print(history_dict)
    return history_dict

# Evaluate the model on the test data using `evaluate`
def evaluate_model(model_path, test_data, test_labels):
    best_fnn = load_model(model_path)
    print("Evaluate on test data:")
    test_start = time.time()
    results = best_fnn.evaluate(test_data, test_labels, batch_size=128)
    testing_time = time.time() - test_start
    print("test loss, test acc:", results)
    return results[0], results[1], testing_time

# Compile and Train model
def train_model(model,train_data,train_labels, epochs):
    model_checkpoint_callback_fnn = ModelCheckpoint(
    filepath=(model.name + ".h5"),
    save_weights_only=False,
    monitor='val_acc',
    mode='max',
    save_best_only=True)

    model.compile(optimizer="adam", loss=SparseCategoricalCrossentropy(from_logits=True), metrics=["acc"])

    training_start = time.time()
    model_history = model.fit(train_data, train_labels, epochs=epochs, validation_split=0.1, callbacks=model_checkpoint_callback_fnn)
    training_time = time.time() - training_start
    return model, model_history, training_time

def get_gzipped_model_size(file):
  # Returns size of gzipped model, in bytes.
  _, zipped_file = tempfile.mkstemp('.zip')
  with zipfile.ZipFile(zipped_file, 'w', compression=zipfile.ZIP_DEFLATED) as f:
    f.write(file)

  return os.path.getsize(zipped_file)