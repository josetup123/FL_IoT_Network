# #!/usr/bin/env python3 #
# """
#     This script launches the independent version of a MLP, it has both MLP classifier and regressor models for the
#     offset data and RUL predictor. The script uses its specific small dataset version: ex. if this machine is labeled
#     as 0 then it will use data_set_0.csv therefore it will only process data that belongs to this label.
#     It fillows the same execution steps and model as the independent learning. It is important to mention,
#     it performs the testing process with 20% of the entire datasat. This allows to validate if the model trained with 
#     a small dataset like data_set_0.csv is capable to offer overall good predictions for all classes (entire dataset).
     
    
# """

# # Libraries
# from tensorflow.keras.layers import Dropout
# import tensorflow as tf
# import argparse
# import numpy as np
# import pandas as pd
# import os
# import pickle
# import random as rn
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import (
#     mean_squared_error,
#     mean_absolute_error,
#     explained_variance_score,
#     r2_score,
# )
# from sklearn.metrics import (
#     classification_report,
#     confusion_matrix,
#     roc_auc_score,
#     recall_score,
#     cohen_kappa_score,
#     matthews_corrcoef,
#     precision_recall_fscore_support,
# )
# from sklearn import preprocessing
# from sklearn.model_selection import StratifiedKFold
# from sklearn.metrics import r2_score, mean_squared_error
# from sklearn.metrics import cohen_kappa_score
# import tensorflow as tf
# from sklearn.model_selection import KFold
# import sys
# import argparse
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import os
# import itertools
# import pickle
# import random as rn
# from sklearn.preprocessing import StandardScaler
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.callbacks import EarlyStopping
# from tensorflow.keras.layers import Dense
# from tensorflow.random import set_seed
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import (
#     mean_squared_error,
#     mean_absolute_error,
#     explained_variance_score,
#     r2_score,
#     mean_absolute_percentage_error,
#     max_error,
#     median_absolute_error,
# )
# from sklearn.metrics import (
#     classification_report,
#     confusion_matrix,
#     roc_auc_score,
#     recall_score,
#     cohen_kappa_score,
#     matthews_corrcoef,
#     precision_recall_fscore_support,
# )
# from sklearn import preprocessing


# class Independent:

#     def __init__(
#         self,
#         data_file_name,
#         rndseed,
#         epochs,
        
#         model,
#         clients_max,
#         clients_number,
#         ip,
#         comparative_path_y_test,
#         comparative_path_X_test,
#     ):

#         self.data_file_name = data_file_name
#         self.rndseed = rndseed
#         self.epochs = epochs
#         self.learning_rate = learning_rate
#         self.model = model
#         self.clients_max = clients_max
#         self.clients_number = clients_number
#         self.ip = ip
#         self.comparative_path_y_test = comparative_path_y_test
#         self.comparative_path_X_test = comparative_path_X_test

#         self.concatenated_identifier = (str(self.epochs) + "_" +
#                                         str(self.learning_rate) + "_" +
#                                         str(self.model) + "_" +
#                                         str(self.clients_max) + "_" +
#                                         str(self.clients_number) + "_" +
#                                         str(self.data_file_name) + "__")
#         self.DATA_FOLDER = "fl_testbed/version2/data/initial/"
#         self.TRANSFORMED_FOLDER = "fl_testbed/version2/data/transformed/"
#         self.FILE_NAME = "client_independent"
#         self.DATA_FILE = "DATASET_"
#         self.DATA_FILE2 = "combined_offset_misalignment"
#         self.PRECISION = 4

#         self.y_train = None
#         self.X_train = None
#         self.y_test = None
#         self.X_test = None
#         self.df = None
#         self.model = None
#         self.X = None
#         self.y = None
#         self.clf = None

#     def load_data(self):

#         df_temp = pd.read_csv(self.TRANSFORMED_FOLDER + self.data_file_name,
#                               chunksize=50000)
#         self.df = pd.concat(df_temp)

#     def train_cut_split_1(self):
#         df = self.df
#         # drop unwanted cols
#         # drop Unnamed
#         df = df[df.columns.drop(list(df.filter(regex="Unnamed")))]
#         # drop time column
#         df = df[df.columns.drop(list(df.filter(regex="wf_start_time")))]

#         status_map = {
#             "No_Offset": 0,
#             "1mm_Offset": 1,
#             "3mm_Offset": 2,
#             "6.25mm_Offset": 3,
#             "12.7mm_Offset": 4,
#         }

#         df["status"] = df["status"].map(status_map)

#         self.y = df["status"]  # pop response
#         self.X = df.drop("status", axis=1)  # drop response
#         print(self.X.shape)
#         print(self.y.shape)

#     def train_cut_split_2(self):
#         df = self.df

#         # drop unwanted cols
#         df = df[df.columns.drop(list(
#             df.filter(regex="Unnamed")))]  # drop Unnamed
#         df = df[df.columns.drop(
#             list(df.filter(
#                 regex="Waveform_VA_wf_start_time")))]  # drop time column
#         df = df[df.columns.drop(list(
#             df.filter(regex="status")))]  # drop status column

#         df = df[df.columns.drop(list(df.filter(regex="string")))]
#         df = df[df.columns.drop(list(df.filter(regex="NodeId")))]
#         df = df[df.columns.drop(list(df.filter(regex="AssetName")))]
#         df = df[df.columns.drop(list(df.filter(regex="Group_wf_start_time")))]

#         df = df[df.columns.drop(
#             list(df.filter(regex="Waveform_VB_wf_start_time")))]
#         df = df[df.columns.drop(
#             list(df.filter(regex="Waveform_VC_wf_start_time")))]
#         df = df[df.columns.drop(
#             list(
#                 df.filter(
#                     regex=
#                     "Waveform_Probe_1_AxialDirection_NI_CM_FftAmplitudeScale"))
#         )]
#         df = df[df.columns.drop(
#             list(
#                 df.filter(
#                     regex="Waveform_Probe_6_BearingRadial_wf_start_time")))]
#         df = df[df.columns.drop(
#             list(
#                 df.filter(
#                     regex="Waveform_Probe_5_RadialHorizontal_wf_start_time")))]
#         df = df[df.columns.drop(list(df.filter(regex="wf_start_time")))]

#         df = df[df.columns.drop(list(df.filter(regex="CM_Unit")))]
#         df = df[df.columns.drop(list(df.filter(regex="CM_ResultUnits")))]

#         df = df.dropna(axis=1, how="all")  # drop cols with all NaN

#         # further cleaning
#         df = df.fillna(0)

#         print(df.isnull().values.any())

#         self.y = df["rul"]  # pop response
#         self.X = df.drop("rul", axis=1)  # drop response

#         print(self.X.shape)
#         print(self.y.shape)

#     def pre_modeling_2(self):
#         # self.clf = preprocessing.LabelBinarizer()
#         # self.clf.fit(self.y)

#         X_train, X_test, y_train, y_test = train_test_split(
#             self.X,
#             self.y,
#             random_state=self.rndseed,
#             shuffle=True,
#             test_size=0.2)

#         # saving files.
#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "y_train.pkl",
#                 "wb",
#         ) as file:
#             pickle.dump(y_train, file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "X_train.pkl",
#                 "wb",
#         ) as file:
#             pickle.dump(X_train, file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "y_test.pkl",
#                 "wb",
#         ) as file:
#             pickle.dump(y_test, file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "X_test.pkl",
#                 "wb",
#         ) as file:
#             pickle.dump(X_test, file)

#         # cleaning
#         del y_train
#         del X_train
#         del y_test
#         del X_test

#         # loading
#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "y_train.pkl",
#                 "rb",
#         ) as file:
#             self.y_train = pickle.load(file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "X_train.pkl",
#                 "rb",
#         ) as file:
#             self.X_train = pickle.load(file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "y_test.pkl",
#                 "rb",
#         ) as file:
#             self.y_test = pickle.load(file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "X_test.pkl",
#                 "rb",
#         ) as file:
#             self.X_test = pickle.load(file)

#     def pre_modeling_1(self):
#         self.clf = preprocessing.LabelBinarizer()
#         self.clf.fit(self.y)

#         X_train, X_test, y_train, y_test = train_test_split(
#             self.X,
#             self.y,
#             random_state=self.rndseed,
#             shuffle=True,
#             test_size=0.2)

#         # saving files.
#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "y_train.pkl",
#                 "wb",
#         ) as file:
#             pickle.dump(y_train, file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "X_train.pkl",
#                 "wb",
#         ) as file:
#             pickle.dump(X_train, file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "y_test.pkl",
#                 "wb",
#         ) as file:
#             pickle.dump(y_test, file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "X_test.pkl",
#                 "wb",
#         ) as file:
#             pickle.dump(X_test, file)

#         # cleaning
#         del y_train
#         del X_train
#         del y_test
#         del X_test

#         # loading
#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "y_train.pkl",
#                 "rb",
#         ) as file:
#             self.y_train = pickle.load(file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "X_train.pkl",
#                 "rb",
#         ) as file:
#             self.X_train = pickle.load(file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "y_test.pkl",
#                 "rb",
#         ) as file:
#             self.y_test = pickle.load(file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.concatenated_identifier +
#                 self.FILE_NAME + "X_test.pkl",
#                 "rb",
#         ) as file:
#             self.X_test = pickle.load(file)

#     def modeling_2(self):

#         X = self.X_train
#         y = self.y_train

#         X_columns = X.columns
#         scaler = StandardScaler()
#         X = scaler.fit_transform(X)

#         X = pd.DataFrame(X, columns=X_columns)

#         print(X.shape)
#         print(y.shape)

        
#         # Early Stopping
#         es = EarlyStopping(monitor="val_loss",
#                            mode="auto",
#                            verbose=2,
#                            patience=1,
#                            min_delta=0.001)


#         # define 10-fold cross validation test harness
#         skf = KFold(n_splits=10, shuffle=True, random_state=RNDSEED)

#         # self.model
#         self.model = Sequential()

#         # hidden layers

#         self.model.add(
#             Dense(120, activation="relu",
#                   input_dim=X.shape[1]))  # 0.01 74121 LeakyReLU(alpha=0.001)
#         # self.model.add(Dropout(0.1))
#         self.model.add(Dense(100, activation="relu"))
#         # self.model.add(Dropout(0.1))
#         self.model.add(Dense(60, activation="relu"))

#         # output layer
#         self.model.add(Dense(1, activation="linear")
#                        )  # softmax for probability, #values are sigmoid

#         self.model.compile(
#             optimizer=tf.keras.optimizers.Adam(
#                 learning_rate=self.learning_rate),
#             loss=["mse"],
#             metrics=["mae"],
#         )

#         lst_accu_stratified = []

#         for train_index, test_index in skf.split(X, y):
#             X_train_fold, X_test_fold = X.iloc[train_index], X.iloc[test_index]
#             y_train_fold, y_test_fold = y.iloc[train_index], y.iloc[test_index]

#             self.model.fit(
#             x=X_train_fold,
#             y=y_train_fold,
#             callbacks=[es],
#             batch_size=128,
#             epochs=self.epochs,
#             validation_data=(X_test_fold,y_test_fold))

#             lst_accu_stratified.append(
#                 self.model.evaluate(X_test_fold, y_test_fold))

#         # only accuracy
#         lst_accu_stratified = [inner[1] for inner in lst_accu_stratified]
#         print("List of possible mae:", lst_accu_stratified)
#         print(
#             "Maximum mae That can be obtained from this model is:",
#             max(lst_accu_stratified),
#         )
#         print("Minimum mae:", min(lst_accu_stratified))
#         print("Overall mae:", np.average(lst_accu_stratified))

#     def modeling_1(self):
#         X = self.X_train
#         y = self.y_train

#         print(X.shape)
#         print(y.shape)

#         # Early Stopping
#         es = EarlyStopping(monitor="val_loss",
#                            mode="auto",
#                            verbose=2,
#                            patience=1,
#                            min_delta=0.001)


#         # define 10-fold cross validation test harness
#         skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=RNDSEED)

#         # self.model
#         self.model = Sequential()

#         # hidden layers
        

#         self.model.add(Dense(80, activation="relu", input_dim=X.shape[1]))
        

#         self.model.add(Dropout(0.2))


#         self.model.add(Dense(60, activation="relu"))

#         # output layer
#         self.model.add(Dense(len(y.unique()), activation="softmax")
#                     )  # softmax for probability, #values are sigmoid

#         self.model.compile(
#             optimizer=tf.keras.optimizers.Adam(
#                 learning_rate=self.learning_rate),
#             loss="categorical_crossentropy",
#             metrics=["accuracy"],
#         )

#         lst_accu_stratified = []

#         for train_index, test_index in skf.split(X, y):
#             X_train_fold, X_test_fold = X.iloc[train_index], X.iloc[test_index]
#             y_train_fold, y_test_fold = y.iloc[train_index], y.iloc[test_index]

#             self.model.fit(
#             x=X_train_fold,
#             y=self.clf.transform(y_train_fold),
#             callbacks=[es],
#             batch_size=128,
#             epochs=self.epochs,
#             validation_data=(X_test_fold,self.clf.transform(y_test_fold)))
            

             

#             lst_accu_stratified.append(
#                 self.model.evaluate(X_test_fold,
#                                     self.clf.transform(y_test_fold)))

#         # only accuracy
#         lst_accu_stratified = [inner[1] for inner in lst_accu_stratified]
#         print("List of possible accuracy:", lst_accu_stratified)
#         print(
#             "Maximum Accuracy That can be obtained from this model is:",
#             max(lst_accu_stratified),
#         )
#         print("Minimum Accuracy:", min(lst_accu_stratified))
#         print("Overall Accuracy:", np.average(lst_accu_stratified))

#     def testing_1(self):

#         self.FILE_NAME = "centralized_global_multiclass"

#         with open(
#                 self.TRANSFORMED_FOLDER + self.comparative_path_y_test,
#                 "rb",
#         ) as file:
#             y_test = pickle.load(file)

#         with open(
#                 self.TRANSFORMED_FOLDER + self.comparative_path_X_test,
#                 "rb",
#         ) as file:
#             X_test = pickle.load(file)

#         print("Test set")
#         print("LOSS", "ACCURACY")

#         y_test = self.y_test

#         # prob as an output
#         y_prob = self.model.predict(self.X_test, batch_size=128, verbose=0)
#         print("PROBS")
#         print(self.X_test[:5])
#         print(y_prob[:5])
#         print(y_prob.shape)

#         macro_roc_auc_ovo = roc_auc_score(y_test,
#                                           y_prob,
#                                           multi_class="ovo",
#                                           average="macro")
#         weighted_roc_auc_ovo = roc_auc_score(y_test,
#                                              y_prob,
#                                              multi_class="ovo",
#                                              average="weighted")
#         macro_roc_auc_ovr = roc_auc_score(y_test,
#                                           y_prob,
#                                           multi_class="ovr",
#                                           average="macro")
#         weighted_roc_auc_ovr = roc_auc_score(y_test,
#                                              y_prob,
#                                              multi_class="ovr",
#                                              average="weighted")
#         print("One-vs-One ROC AUC scores:\n{:.6f} (macro),\n{:.6f} "
#               "(weighted by prevalence)".format(macro_roc_auc_ovo,
#                                                 weighted_roc_auc_ovo))
#         print("One-vs-Rest ROC AUC scores:\n{:.6f} (macro),\n{:.6f} "
#               "(weighted by prevalence)".format(macro_roc_auc_ovr,
#                                                 weighted_roc_auc_ovr))

#         # class transformation

#         y_pred = np.argmax(y_prob, axis=-1)

#         print("CLASSES")
#         print("unique", np.unique(y_pred.tolist()))
#         print(y_pred.shape)
#         print(y_pred[:20])

#         print(
#             "precision_recall_fscore_support \n",
#             precision_recall_fscore_support(y_pred=y_pred,
#                                             y_true=y_test,
#                                             average="micro"),
#         )
#         print(
#             "confusion_matrix \n",
#             confusion_matrix(y_pred=y_pred, y_true=y_test),
#         )
#         print(
#             "metrics.recall_score =>",
#             recall_score(y_pred=y_pred, y_true=y_test, average="micro"),
#         )
#         print("cohen_kappa_score => ", cohen_kappa_score(y_pred, y_test))
#         print(
#             "metrics.classification_report \n",
#             classification_report(y_pred=y_pred, y_true=y_test),
#         )
#         print(
#             "metrics.matthews_corrcoef =>",
#             matthews_corrcoef(y_pred=y_pred, y_true=y_test),
#         )

#     def testing_2(self):
#         y_test = self.y_test
#         X_test = self.X_test

#         X_columns = X_test.columns
#         scaler = StandardScaler()
#         X_test = scaler.fit_transform(X_test)

#         # X_test = pd.DataFrame(X_test, columns = X_columns)

#         # print(X_test.shape)

#         # prob as an output
#         y_pred = self.model.predict(X_test, batch_size=128, verbose=2)

#         print(X_test[:5])
#         print(y_pred[:5])
#         print(y_test[:5])

#         print(y_pred.shape)

#         print("R^2:", r2_score(y_test, y_pred))
#         print("Mean Absolute Error (MAE):",
#               mean_absolute_error(y_test, y_pred))
#         print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
#         print(
#             "Mean Absolute Percentage Error (MAPE):",
#             mean_absolute_percentage_error(y_test, y_pred),
#         )
#         print(
#             "Root Mean Squared Error (RMSE):",
#             np.sqrt(mean_squared_error(y_test, y_pred)),
#         )  # np.sqrt

#         print("Explained Variance Score:",
#               explained_variance_score(y_test, y_pred))
#         print("Max Error:", max_error(y_test, y_pred))
#         # print('Mean Squared Log Error:', mean_squared_log_error(y_test, y_pred))
#         print("Median Absolute Error:", median_absolute_error(y_test, y_pred))


# if __name__ == "__main__":

#     # Arguments
#     parser = argparse.ArgumentParser()

#     parser.add_argument("-ml", "--model", help="Predined model run", type=int)
#     parser.add_argument(
#         "-cm",
#         "--clients_max",
#         help="Maximun number of clients",
#         type=int,
#         required=True,
#     )
#     parser.add_argument(
#         "-cn",
#         "--clients_number",
#         help="Number of a specific client <= maximun number of clients",
#         type=int,
#         required=True,
#     )
#     parser.add_argument(
#         "-e",
#         "--epochs",
#         help="epochs",
#         type=int,
#         required=True,
#         default=0,
#     )
#     parser.add_argument(
#         "-lr",
#         "--learning_rate",
#         help="learning_rate",
#         type=float,
#         required=True,
#         default=0,
#     )
#     parser.add_argument("-dfn",
#                         "--data_file_name",
#                         help="Data file name",
#                         type=str)
#     parser.add_argument("-ip", "--ip", help="IP adress", type=str)

#     parser.add_argument(
#         "-c_path_y_test",
#         "--comparative_path_y_test",
#         help="comparative_path y_test",
#         required=True,
#         default=None,
#     )
#     parser.add_argument(
#         "-c_path_X_test",
#         "--comparative_path_X_test",
#         help="comparative_path y_test",
#         required=True,
#         default=None,
#     )

#     args = parser.parse_args()

#     model = int(args.model)
#     clients_max = int(args.clients_max)
#     clients_number = int(args.clients_number)
#     epochs = int(args.epochs)
#     learning_rate = float(args.learning_rate)
#     data_file_name = str(args.data_file_name)
#     ip = str(args.ip)
#     comparative_path_y_test = args.comparative_path_y_test
#     comparative_path_X_test = args.comparative_path_X_test

#     # Configuration
#     root_path = os.path.dirname(os.path.abspath("__file__"))
#     os.chdir(root_path)

#     RNDSEED = np.random.seed(39)
#     np.random.seed(RNDSEED)
#     set_seed(RNDSEED)
#     os.environ["PYTHONHASHSEED"] = str(RNDSEED)
#     rn.seed(RNDSEED)

#     independent = Independent(
#         data_file_name,
#         RNDSEED,
#         epochs,
#         learning_rate,
#         model,
#         clients_max,
#         clients_number,
#         ip,
#         comparative_path_y_test,
#         comparative_path_X_test,
#     )

#     independent.load_data()
#     if model == 1:
#         independent.train_cut_split_1()
#         independent.pre_modeling_1()
#         independent.modeling_1()
#         independent.testing_1()
#     elif model == 2:
#         independent.train_cut_split_2()
#         independent.pre_modeling_2()
#         independent.modeling_2()
#         independent.testing_2()

#     exit()





#!/usr/bin/env python3 #
"""
    This script lauches the independent version of a MLP and has both Regression and classification models for the
    offset data and RUL predictor respectively.
    The script uses the entire dataset.
    
"""




import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


#MLP

from tensorflow.keras.regularizers import L1L2

import tensorflow as tf
import numpy as np



from sklearn.model_selection import train_test_split

# from autosklearn.regression import AutoSklearnRegressor

# from tensorflow.keras.regularizers import L2,L1,L1L2
import tensorflow as tf









from tensorflow.keras.regularizers import L2,L1,L1L2
#LSTM
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
# from tensorflow.keras.regularizers import L1L2




RNDSEED = np.random.seed(39)
PRECISION = 4 # 3 of digits to keep after the decimal point
from sklearn import tree
from sklearn import metrics
from sklearn.metrics import f1_score, cohen_kappa_score

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_regression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler, MinMaxScaler
RUNNING_ON_COLAB = False # we assume running on CoLab! Change to False if running locally.








from keras.regularizers import l2, l1

# Libraries
from tensorflow.keras.layers import Dropout
from keras.layers import LeakyReLU
import json
from sklearn.metrics import r2_score, mean_squared_error,classification_report
from sklearn.metrics import f1_score, cohen_kappa_score
import tensorflow as tf
from sklearn.model_selection import KFold
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
from collections.abc import Iterable
import pandas as pd
import os
import itertools
import pickle
import random as rn
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense
from tensorflow.random import set_seed
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    explained_variance_score,
    accuracy_score,
    r2_score,
    mean_absolute_percentage_error,
    max_error,
    mean_squared_log_error,
    median_absolute_error,
)
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    recall_score,
    cohen_kappa_score,
    matthews_corrcoef,
    precision_recall_fscore_support,
)
from sklearn import preprocessing
from sklearn.model_selection import StratifiedKFold

print("SCRIPT INITIATED")
class Independent:

    def __init__(
        self,
        data_file_name,
        dfn_test_x,
        dfn_test_y,
        rndseed,
        epochs,
        # learning_rate,
        model,
        clients_max,
        clients_number,
        ip,
    ):

        self.data_file_name = data_file_name
        self.rndseed = rndseed
        self.epochs = epochs
        # self.learning_rate = learning_rate
        self.model = model
        self.clients_max = clients_max
        self.clients_number = clients_number
        self.ip = ip
        self.dfn_test_x=dfn_test_x
        self.dfn_test_y=dfn_test_y

        self.concatenated_identifier = (str(self.epochs) + "_" +
                                        # str(self.learning_rate) + "_" +
                                        str(self.model) + "_" +
                                        str(self.clients_max) + "_" +
                                        str(self.clients_number) + "_" +
                                        str(self.data_file_name) + "__")
        self.DATA_FOLDER = "fl_testbed/version2/data/transformed/"
        self.TRANSFORMED_FOLDER = "fl_testbed/version2/data/transformed/"
        self.FILE_NAME = "client_independent"
        self.DATA_FILE = "combined_offset_misalignment"
        self.PRECISION = 4

        self.y_train = None
        self.X_train = None
        self.y_test = None
        self.X_test = None
        self.df = None
        self.model = None
        self.X = None
        self.y = None
        self.clf = None

    def load_data(self):
        print("INI")

        #TRAINING
        with open(
                self.TRANSFORMED_FOLDER + self.data_file_name,
                # self.concatenated_identifier +
                # self.FILE_NAME + "y_train.pkl",
                "rb",
        ) as file:
            self.df=pd.read_pickle(file)
            # self.df = pickle.load(file)
        

        #TEST
        with open(
                self.TRANSFORMED_FOLDER + self.dfn_test_x,
                # self.concatenated_identifier +
                # self.FILE_NAME + "y_train.pkl",
                "rb",
        ) as file:
            self.X_test = pd.read_pickle(file)

        with open(
                self.TRANSFORMED_FOLDER + self.dfn_test_y,
                # self.concatenated_identifier +
                # self.FILE_NAME + "y_train.pkl",
                "rb",
        ) as file:
            self.y_test = pd.read_pickle(file)

        
        
        
        
        
        print("CHECKPOINT")
        print(self.df.X)
        print(self.df.y)


        


        # self.X_train=self.df.X
        # self.y_train=self.df.y








        # print(self.X_test)
        # print(self.y_test)

        # df_temp = pd.read_csv(self.DATA_FOLDER + self.data_file_name,
                            #   chunksize=50000)
        # self.df = pd.concat(df_temp)

    # def train_cut_split_1(self):
    #     df = self.df
    #     # drop unwanted cols
    #     # drop Unnamed
    #     # df = df[df.columns.drop(list(df.filter(regex="Unnamed")))]
    #     # # drop time column
    #     # df = df[df.columns.drop(list(df.filter(regex="wf_start_time")))]
    #     df = df[df.columns.drop(list(df.filter(regex='Unnamed')))] # drop Unnamed
    #     df = df[df.columns.drop(list(df.filter(regex='wf_start_time')))] # drop time column
    #     df = df[df.columns.drop(list(df.filter(regex='rul')))] # drop status column
    #     df = df[df.columns.drop(list(df.filter(regex='index')))] # drop status column


    #     status_map = {
    #         "No_Offset": 0,
    #         "1mm_Offset": 1,
    #         "3mm_Offset": 2,
    #         "6.25mm_Offset": 3,
    #         "12.7mm_Offset": 4,
    #     }

    #     df["status"] = df["status"].map(status_map)

    #     self.y = df["status"]  # pop response
    #     self.X = df.drop("status", axis=1)  # drop response
    #     self.df=df

    # def train_cut_split_2(self):
    #     #THIS IS FOR THE RUL!!
    #     #I SHOULD START FROM SELF.X AND SELF.Y
    #     df = self.df
    #     # drop Unnamed columns
    #     # df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]

    #     # drop unwanted cols
    #     df = df[df.columns.drop(list(df.filter(regex='Unnamed')))] # drop Unnamed
    #     df = df[df.columns.drop(list(df.filter(regex='wf_start_time')))] # drop time column
    #     #df = df[df.columns.drop(list(df.filter(regex='status')))] # drop status column
    #     df = df[df.columns.drop(list(df.filter(regex='index')))] # drop status column

    #     status_map = {
    #         "No_Offset": 0,
    #         "1mm_Offset": 1,
    #         "3mm_Offset": 2,
    #         "6.25mm_Offset": 3,
    #         "12.7mm_Offset": 4,
    #     }

    #     df["status"] = df["status"].map(status_map)

    #     #PLOTTER NOT INCLUDED 


    #     #COLUMNS
    #     from scipy import stats


    #     cols = list(df.columns[:-3])

    #     print(cols)


    #     #MANUAL OUTLIER REMOVAL!
    #     # df['S1_CrestFactor_g~g'] = df['S1_CrestFactor_g~g'].mask(np.abs(stats.zscore(df['S1_CrestFactor_g~g'])) >= 20)
    #     # df['S1_DerivedPeak_g'] = df['S1_DerivedPeak_g'].mask(np.abs(stats.zscore(df['S1_DerivedPeak_g'])) >= 2)
    #     # df['S1_Peak~Peak_g'] = df['S1_Peak~Peak_g'].mask(np.abs(stats.zscore(df['S1_Peak~Peak_g'])) >= 15)
    #     # df['S1_RMS_g'] = df['S1_RMS_g'].mask(np.abs(stats.zscore(df['S1_RMS_g'])) >= 1)
    #     # df['S1_TruePeak_g'] = df['S1_TruePeak_g'].mask(np.abs(stats.zscore(df['S1_TruePeak_g'])) >= 4)
    #     # df['S1_HighFrequency_grms'] = df['S1_HighFrequency_grms'].mask(np.abs(stats.zscore(df['S1_HighFrequency_grms'])) >= 1.5)
    #     # df['S1_Kurtosis_g~g'] = df['S1_Kurtosis_g~g'].mask(np.abs(stats.zscore(df['S1_Kurtosis_g~g'])) >= 50)
    #     # df['S2_CrestFactor_g~g'] = df['S2_CrestFactor_g~g'].mask(np.abs(stats.zscore(df['S2_CrestFactor_g~g'])) >= 8)
    #     # df['S2_DerivedPeak_g'] = df['S2_DerivedPeak_g'].mask(np.abs(stats.zscore(df['S2_DerivedPeak_g'])) >= 1)
    #     # df['S2_Peak~Peak_g'] = df['S2_Peak~Peak_g'].mask(np.abs(stats.zscore(df['S2_Peak~Peak_g'])) >= 6)
    #     # df['S2_RMS_g'] = df['S2_RMS_g'].mask(np.abs(stats.zscore(df['S2_RMS_g'])) >= 0.6)
    #     # df['S2_TruePeak_g'] = df['S2_TruePeak_g'].mask(np.abs(stats.zscore(df['S2_TruePeak_g'])) >= 3)
    #     # df['S2_HighFrequency_grms'] = df['S2_HighFrequency_grms'].mask(np.abs(stats.zscore(df['S2_HighFrequency_grms'])) >= 0.50)
    #     # df['S2_Kurtosis_g~g'] = df['S2_Kurtosis_g~g'].mask(np.abs(stats.zscore(df['S2_Kurtosis_g~g'])) >= 20)





    #      #DROPPING!!
    #     df = df.apply (pd.to_numeric, errors='coerce')
    #     df = df.dropna()


       


    #     # Get X & y
    #     # Naming convention: X as predictors; y as response.
    #     from sklearn.model_selection import train_test_split

    #     self.y = df[['status','rul']] # pop response

    #     self.X = df.drop('rul',axis = 1) # drop response

    #     self.df=df



        


    def modeling_1(self):
        
        
        print("#ASSIGNAMEMNT")
        df=self.df

        # X_train=df.X.values
        # y_train=df.y.values
        X_train=np.array(df.X.apply(lambda x: np.array(x)).tolist())#
        # train_inputs=train_inputs
        # self.df.X.apply(lambda row: row[:][:-1])
        y_train=np.array(df.y.apply(lambda x: np.array(x)).tolist())#.

    
        # print(X_train)
        # print(y_train)

        # print(X_train.shape)
        # print(y_train.shape)
        # input()
        #TESTS PKL
        X_test=self.X_test
        y_test=self.y_test
        


        #JT CHANANGES
        # Use the same function above for the validation set
        X_train, X_vals, y_train, y_vals = train_test_split(X_train, y_train, 
            test_size=0.25, random_state= RNDSEED,shuffle=True,stratify=y_train) # 0.25 x 0.8 = 0.2


        # df=self.df

        print("X_train",X_train)
        print("X_test",X_test)
        print("X_vals",X_vals)


        unique, counts = np.unique(y_test, return_counts=True)
        print("y_test Classes",dict(zip(unique, counts)))

        unique, counts = np.unique(y_train, return_counts=True)
        print("y_train Classes",dict(zip(unique, counts)))
        
        unique, counts = np.unique(y_vals, return_counts=True)
        print("y_vals Classes",dict(zip(unique, counts)))



        # X_train=np.array(df.X.apply(lambda x: np.array(x)).tolist())#
        # # train_inputs=train_inputs
        # # self.df.X.apply(lambda row: row[:][:-1])
        # y_train=np.array(df.y.apply(lambda x: np.array(x)).tolist())#.




        print(df.shape)
        print(df.X.shape)
        print(df.y.shape)
        


        
        # # set aside 20% of train and test data for evaluation
        # # X_train, X_test, y_train, y_test = train_test_split(X, y,
        # #     test_size=0.2, shuffle = True, random_state = RNDSEED)

        # # # Use the same function above for the validation set
        # #JT NEW CHANGES
        # X_train, X_vals, y_train, y_vals = train_test_split(df.X, df.y, 
        #     test_size=0.25, random_state= RNDSEED,shuffle=True) # 0.25 x 0.8 = 0.2



        # # saving files. HERE AVOIDS DATA LEAKEAGE!!!
        # with open(
        #         self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #         self.FILE_NAME + "y_train.pkl",
        #         "wb",
        # ) as file:
        #     pickle.dump(y_train, file)

        # with open(
        #         self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #         self.FILE_NAME + "X_train.pkl",
        #         "wb",
        # ) as file:
        #     pickle.dump(X_train, file)

        # with open(
        #         self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #         self.FILE_NAME + "y_test.pkl",
        #         "wb",
        # ) as file:
        #     pickle.dump(y_test, file)

        # with open(
        #         self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #         self.FILE_NAME + "X_test.pkl",
        #         "wb",
        # ) as file:
        #     pickle.dump(X_test, file)

        # with open(
        #     self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #     self.FILE_NAME + "y_vals.pkl",
        #     "wb",
        # ) as file:
        #     pickle.dump(y_vals, file)

        # with open(
        #         self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #         self.FILE_NAME + "X_vals.pkl",
        #         "wb",
        # ) as file:
        #     pickle.dump(X_vals, file)
        

        # self.clf = preprocessing.LabelBinarizer()
        # self.clf.fit(self.y)




        from sklearn.preprocessing import StandardScaler,LabelBinarizer
        lbz = LabelBinarizer()

        # print("MODELSLSSDLLDSLSD")
        # print(X_train.shape)
        # print(X_train.dtype)
        # print(X_train)

        scaler=StandardScaler()
        X_train=scaler.fit_transform(X_train)
        y_train=lbz.fit_transform(y_train)



        scaler=StandardScaler()
        X_vals=scaler.fit_transform(X_vals)
        y_vals=lbz.fit_transform(y_vals)


        scaler=StandardScaler()
        X_test=scaler.fit_transform(X_test)
        y_test=lbz.fit_transform(y_test)







        print(X_train.shape)
        print(X_vals.shape)
        print(X_test.shape)











        from  datetime import datetime
        log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        print(log_dir)
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
        lr = tf.keras.callbacks.LearningRateScheduler(lambda epoch: 10**-7 * 10**(epoch/3))








        #TRAINING
        tf.keras.backend.clear_session()


        # self.model
        self.model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(60, activation="relu", input_dim=X_train.shape[1],kernel_regularizer=L1L2(l2=0.001,l1=0.001)), #Better

        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(30, activation="relu",kernel_regularizer=L2(l2=0.001)),  #Better
        tf.keras.layers.Dropout(0.5),

 
        # output layer
        tf.keras.layers.Dense(5, activation="softmax")])
                    # softmax for probability, #values are sigmoid



        # Configure the model and start training
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])

        # y_train


        # Early Stopping
        es = EarlyStopping(monitor="val_loss",
                        mode="auto",
                        verbose=2,
                        patience=1,
                        min_delta=0.001,
                        restore_best_weights=True)


        #FAST AI SEE IF TRIANING IMPROVES !
        # 1420492

        history=self.model.fit(X_train, y_train,epochs=self.epochs,batch_size=32,validation_data=(X_vals,y_vals) ,verbose=1,callbacks=[tensorboard_callback,lr,es],)



        y_prob = self.model.predict(X_test)
        
        y_prob_am=np.argmax(y_prob, axis=1)
        y_test_am=np.argmax(y_test, axis=1)
        
        # print(y_prob_am)
        # print(y_test_am)

        macro_roc_auc_ovo = roc_auc_score(y_test, y_prob, multi_class="ovo", average="macro")
        weighted_roc_auc_ovo = roc_auc_score(
            y_test, y_prob, multi_class="ovo", average="weighted"
        )
        macro_roc_auc_ovr = roc_auc_score(y_test, y_prob, multi_class="ovr", average="macro")
        weighted_roc_auc_ovr = roc_auc_score(
            y_test, y_prob, multi_class="ovr", average="weighted"
        )
        print(
            "One-vs-One ROC AUC scores:\n{:.6f} (macro),\n{:.6f} "
            "(ovo weighted by prevalence)".format(macro_roc_auc_ovo, weighted_roc_auc_ovo)
        )
        print(
            "One-vs-Rest ROC AUC scores:\n{:.6f} (macro),\n{:.6f} "
            "(ovr weighted by prevalence)".format(macro_roc_auc_ovr, weighted_roc_auc_ovr)
        )

        # print()


        print(classification_report(y_test_am,y_prob_am ))
        # print(roc_auc_score(y_test_am,y_prob_am , average="macro",  multi_class="ovr"  ))
        # print(roc_auc_score(y_test_am,y_prob_am , average="macro",  multi_class="ovo"  ))
        print("MCS", matthews_corrcoef(y_test_am,y_prob_am ))


        # df=self.df
        # X=self.X
        # y=self.y


        # # set aside 20% of train and test data for evaluation
        # # X_train, X_test, y_train, y_test = train_test_split(X, y,
        # #     test_size=0.2, shuffle = True, random_state = RNDSEED)

        # # Use the same function above for the validation set
        # X_train, X_vals, y_train, y_vals = train_test_split(self.X_train, self.y_train, 
        #     test_size=0.25, random_state= RNDSEED,shuffle=True) # 0.25 x 0.8 = 0.2



        # # saving files. HERE AVOIDS DATA LEAKEAGE!!!
        # with open(
        #         self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #         self.FILE_NAME + "y_train.pkl",
        #         "wb",
        # ) as file:
        #     pickle.dump(y_train, file)

        # with open(
        #         self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #         self.FILE_NAME + "X_train.pkl",
        #         "wb",
        # ) as file:
        #     pickle.dump(X_train, file)

        # with open(
        #         self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #         self.FILE_NAME + "y_test.pkl",
        #         "wb",
        # ) as file:
        #     pickle.dump(y_test, file)

        # with open(
        #         self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #         self.FILE_NAME + "X_test.pkl",
        #         "wb",
        # ) as file:
        #     pickle.dump(X_test, file)

        # with open(
        #     self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #     self.FILE_NAME + "y_vals.pkl",
        #     "wb",
        # ) as file:
        #     pickle.dump(y_vals, file)

        # with open(
        #         self.TRANSFORMED_FOLDER + self.concatenated_identifier +
        #         self.FILE_NAME + "X_vals.pkl",
        #         "wb",
        # ) as file:
        #     pickle.dump(X_vals, file)
        

        # # self.clf = preprocessing.LabelBinarizer()
        # # self.clf.fit(self.y)

        # from sklearn.preprocessing import StandardScaler,LabelBinarizer
        # lbz = LabelBinarizer()


        # scaler=StandardScaler()
        # X_train=scaler.fit_transform(X_train)
        # y_train=lbz.fit_transform(y_train)



        # scaler=StandardScaler()
        # X_vals=scaler.fit_transform(X_vals)
        # y_vals=lbz.fit_transform(y_vals)


        # scaler=StandardScaler()
        # X_test=scaler.fit_transform(X_test)
        # y_test=lbz.fit_transform(y_test)
















        # from  datetime import datetime
        # log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        # print(log_dir)
        # tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
        # lr = tf.keras.callbacks.LearningRateScheduler(lambda epoch: 10**-7 * 10**(epoch/3))








        # #TRAINING
        # tf.keras.backend.clear_session()



        # # self.model
        # model = Sequential()

        # # hidden layers
        # model.add(Dense(60, activation="relu", input_dim=X_train.shape[1],kernel_regularizer=L1L2(l2=0.001,l1=0.001))) #Better
        # #GOOD 60

        # model.add(Dropout(0.5))


        # model.add(Dense(30, activation="relu",kernel_regularizer=L2(l2=0.001)))  #Better
        # #GOOD 40
        # model.add(Dropout(0.5))

        # # model.add(Dense(40, activation="relu"))
        # # model.add(Dropout(0.2))
        # # model.add(Dense(10, activation="relu",kernel_regularizer=L2(l2=0.001)))  #Better
        # # output layer
        # model.add(Dense(5, activation="softmax"))
        #             # softmax for probability, #values are sigmoid



        # # Configure the model and start training
        # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])

        # # y_train


        # # Early Stopping
        # es = EarlyStopping(monitor="val_loss",
        #                 mode="auto",
        #                 verbose=2,
        #                 patience=1,
        #                 min_delta=0.001,
        #                 restore_best_weights=True)


        # #FAST AI SEE IF TRIANING IMPROVES !
        # # 1420492

        # history=model.fit(X_train, y_train,epochs=self.epochs,batch_size=32,validation_data=(X_vals,y_vals) ,verbose=1,callbacks=[tensorboard_callback,lr,es],)



        # y_prob = model.predict(X_test)

        # macro_roc_auc_ovo = roc_auc_score(y_test, y_prob, multi_class="ovo", average="macro")
        # weighted_roc_auc_ovo = roc_auc_score(
        #     y_test, y_prob, multi_class="ovo", average="weighted"
        # )
        # macro_roc_auc_ovr = roc_auc_score(y_test, y_prob, multi_class="ovr", average="macro")
        # weighted_roc_auc_ovr = roc_auc_score(
        #     y_test, y_prob, multi_class="ovr", average="weighted"
        # )
        # print(
        #     "One-vs-One ROC AUC scores:\n{:.6f} (macro),\n{:.6f} "
        #     "(weighted by prevalence)".format(macro_roc_auc_ovo, weighted_roc_auc_ovo)
        # )
        # print(
        #     "One-vs-Rest ROC AUC scores:\n{:.6f} (macro),\n{:.6f} "
        #     "(weighted by prevalence)".format(macro_roc_auc_ovr, weighted_roc_auc_ovr)
        # )


        # # X = self.X_train
        # # y = self.y_train

        # # print(X.shape)
        # # print(y.shape)


        # # define 10-fold cross validation test harness
        # skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=RNDSEED)

        # # self.model
        # self.model = Sequential()

        # # hidden layers
        

        # self.model.add(Dense(80, activation="relu", input_dim=X.shape[1]))
        

        # self.model.add(Dropout(0.2))


        # self.model.add(Dense(60, activation="relu"))

        # # output layer
        # self.model.add(Dense(len(y.unique()), activation="softmax")
        #             )  # softmax for probability, #values are sigmoid

        # self.model.compile(
        #     optimizer=tf.keras.optimizers.Adam(
        #         learning_rate=self.learning_rate),
        #     loss="categorical_crossentropy",
        #     metrics=["accuracy"],
        # )

        # lst_accu_stratified = []

        # for train_index, test_index in skf.split(X, y):
        #     X_train_fold, X_test_fold = X.iloc[train_index], X.iloc[test_index]
        #     y_train_fold, y_test_fold = y.iloc[train_index], y.iloc[test_index]

        #     self.model.fit(
        #         x=X_train_fold,
        #         y=self.clf.transform(y_train_fold),
        #         callbacks=[es],
        #         batch_size=128,
        #         epochs=self.epochs,
        #         validation_data=(X_train_fold,self.clf.transform(y_train_fold))
        #     )

        #     lst_accu_stratified.append(
        #         self.model.evaluate(X_test_fold,
        #                             self.clf.transform(y_test_fold)))

        # # only accuracy
        # lst_accu_stratified = [inner[1] for inner in lst_accu_stratified]
        # print("List of possible accuracy:", lst_accu_stratified)
        # print(
        #     "Maximum Accuracy That can be obtained from this model is:",
        #     max(lst_accu_stratified),
        # )
        # print("Minimum Accuracy:", min(lst_accu_stratified))
        # print("Overall Accuracy:", np.average(lst_accu_stratified))


    def modeling_2(self):
        
        print("#ASSIGNAMEMNT")
        #MANIN ASSIGNAMENT 

        train_inputs=np.array(self.df.X.apply(lambda x: np.array(x)).tolist())
        # train_inputs=train_inputs
        # self.df.X.apply(lambda row: row[:][:-1])
        train_out=np.array(self.df.y.apply(lambda x: np.array(x)).tolist())
        # np.array(self.df.y).reshape(-1,1)
        
    
        print(train_inputs)
        print(train_out)

        #GETTING RID OF LAST STATUS COLUM!!
        # print(len(self.df.X.to_numpy()[0][0][:-1]))
        # print(len(self.df.X.to_numpy()[0][:]))
        # print(self.df.X.shape[0])
        # print(self.df.X.values[0].shape)


        
        # print(len(self.df.X.to_numpy()[0][0][:-1])) self.df.X.shape[0],
        
        # for i in self.df.X:
        # train_inputs=np.array(self.df.X).reshape((len(self.df.X.to_numpy()[0][:]),len(self.df.X.to_numpy()[0][0][:-1])))
        # train_out=np.array(self.df.y).reshape(-1,1)

        print(train_inputs.shape)
        print(train_out.shape)
        # input()
        #TESTS PKL
        test_inputs=self.X_test
        test_out=self.y_test
        

        print("PRINTING TRAIN_TEST_SPLIT")
        print(train_out)

        stra_train_inputs=train_inputs[:,:,-1]

        # Use the same function above for the validation set WE JUST SPLIT IT IN 0.25 and 0.75 OF THE PREVIOUS SPLIT
        train_inputs, vals_inputs, train_out, vals_out = train_test_split(train_inputs, train_out, 
            test_size=0.25,shuffle=True, random_state= RNDSEED,stratify=stra_train_inputs) # 0.25 x 0.8 = 0.2




        #DROPPING STATUS

        print(train_inputs.shape)
        train_inputs=train_inputs[:,:,:-1]
        test_inputs=test_inputs[:,:,:-1]
        vals_inputs=vals_inputs[:,:,:-1]
        print(train_inputs.shape)
        # input()

        print("train_out")
        print(train_out.shape)
        # polyline = np.array(np.linspace(0,len(train_out),len(train_out) ) )
        scaler=MinMaxScaler(feature_range=(0, 1))
        train_out=scaler.fit_transform(train_out)
        # train_out = train_out.apply(NormalizeData)
        # NormalizeData(polyline)
        train_out=train_out.reshape(-1,1)
        

        print("test_out")
        print(test_out.shape)
        # polyline = np.array(np.linspace(0,len(test_out),len(test_out) ) )
        scaler=MinMaxScaler(feature_range=(0, 1))
        test_out=scaler.fit_transform(test_out)
        # test_out = test_out.apply(NormalizeData)
        # test_out = NormalizeData(polyline)
        test_out=test_out.reshape(-1,1)


        print("vals_out")
        print(vals_out)
        print(vals_out.shape)
        # polyline = np.array(np.linspace(0,len(vals_out),len(vals_out) ) )
        scaler=MinMaxScaler(feature_range=(0, 1))
        vals_out=scaler.fit_transform(vals_out)
        # vals_out = vals_out.apply(NormalizeData)
        # vals_out = NormalizeData(polyline)
        vals_out=vals_out.reshape(-1,1)
        print(vals_out)
        print(vals_out.shape)
        





        #NOW THE SEQUENCES
        "train_inputs"
        for seq in range(train_inputs.shape[0]):
            scaler=StandardScaler()
            
            train_inputs[seq]=scaler.fit_transform(train_inputs[seq])

        "test_inputs"
        for seq in range(test_inputs.shape[0]):
            scaler=StandardScaler()
            
            test_inputs[seq]=scaler.fit_transform(test_inputs[seq])



        "vals_inputs"
        for seq in range(vals_inputs.shape[0]):
            scaler=StandardScaler()
            
            vals_inputs[seq]=scaler.fit_transform(vals_inputs[seq])



            
                











        print(train_inputs.shape)
        print(test_inputs.shape)
        print(vals_inputs.shape)
        # print("Worked: ",worked)
            #     worked = True
                
            # except:
            #     print("Failed: ",seq_length)    
            #     seq_length=seq_length-1
            #     if seq_length<10:
            #         break









     
        from  datetime import datetime

        log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        print(log_dir)
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

        # es=EarlyStopping(
        # monitor="val_loss",
        # patience=6,
        # verbose=1,
        # mode="auto",
        # min_delta=0.0001,
        # restore_best_weights=True)
        
        
        tf.keras.backend.clear_session()

        nb_features = train_inputs.shape[2]
        sequence_length  = train_inputs.shape[1]
        nb_out = train_out.shape[1]

        self.model = tf.keras.models.Sequential([
            tf.keras.layers.LSTM(64, input_shape = (sequence_length, nb_features), return_sequences = True),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.LSTM(32),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(nb_out, activation = 'relu')
        ])

        lr = tf.keras.callbacks.LearningRateScheduler(lambda epoch: 10**-7 * 10**(epoch/3))

        self.model.compile(loss=tf.keras.losses.Huber(), optimizer = tf.keras.optimizers.Adam(lr = 10**-7), metrics =['mse','mae'])


        #FAST AI SEE IF TRIANING IMPROVES !

        es = EarlyStopping(monitor="val_loss",
                mode="auto",
                verbose=2,
                patience=1,
                min_delta=0.001,
                restore_best_weights=True)
        # 1420492
        # history = model.fit(train_inputs, train_out, epochs = 20, callbacks = [lr])
        history=self.model.fit(train_inputs,train_out,epochs=self.epochs,validation_data= (vals_inputs,vals_out) ,verbose=2,callbacks=[tensorboard_callback,lr,es],)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model train vs validation loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper right')
        plt.show()



        # loading the saved modelweights-improvement-87-0.16.h /home/jose/FL_AM_Defect-Detection/checkpoint/RUL16LSTM/weights-improvement-07-0.04.h5
        # model = tf.keras.models.load_model('/home/jose/FL_AM_Defect-Detection/checkpoint/RUL16LSTM/weights-improvement_BEST.h5')

        print(test_inputs.shape)

        _test_inputs=test_inputs[0:]
        _test_out=test_out[0:]


        y_pred = self.model.predict(_test_inputs) ## using the untinted dataset!
    
        print('R^2:', metrics.r2_score(_test_out, y_pred))
        print('Mean Absolute Error (MAE):', metrics.mean_absolute_error(_test_out, y_pred))
        print('Mean Squared Error (MSE):', metrics.mean_squared_error(_test_out, y_pred))
        print('Mean Absolute Percentage Error (MAPE):', metrics.mean_absolute_percentage_error(_test_out, y_pred))
        print('Root Mean Squared Error (RMSE):', np.sqrt(metrics.mean_squared_error(_test_out, y_pred))) # np.sqrt

        print('Explained Variance Score:', metrics.explained_variance_score(_test_out, y_pred))
        print('Max Error:', metrics.max_error(_test_out, y_pred))
        print('Mean Squared Log Error:', metrics.mean_squared_log_error(_test_out, y_pred))
        print('Median Absolute Error:', metrics.median_absolute_error(_test_out, y_pred))


        # X = self.X_train
        # y = self.y_train

        # X_columns = X.columns
        # scaler = StandardScaler()
        # X = scaler.fit_transform(X)

        # X = pd.DataFrame(X, columns=X_columns)

        # print(X.shape)
        # print(y.shape)

        # # Early Stopping
        # es = EarlyStopping(monitor="val_loss",
        #                 mode="auto",
        #                 verbose=2,
        #                 patience=1,
        #                 min_delta=0.001)


        # # define 10-fold cross validation test harness
        # skf = KFold(n_splits=2, shuffle=False, random_state=RNDSEED)

        # # self.model
        # self.model = Sequential()

        # self.model.add(
        #     Dense(
        #         120,
        #         activation=LeakyReLU(alpha=0.005),
        #         input_dim=X.shape[1],
        #         activity_regularizer=l1(0.0001),
        #     ))  # 0.01 74121
        # # self.model.add(Dropout(0.1))
        # self.model.add(Dense(100, activation="relu"))
        # # self.model.add(Dropout(0.1))
        # self.model.add(Dense(80, activation="relu"))

        # # output layer
        # self.model.add(Dense(1, activation="linear")
        #                )  # softmax for probability, #values are sigmoid

        # self.model.compile(
        #     optimizer=tf.keras.optimizers.Adam(
        #         learning_rate=self.learning_rate),
        #     loss=["mse"],
        #     metrics=["mae"],
        # )
        # print(self.model.summary())

        # lst_accu_stratified = []

        # for train_index, test_index in skf.split(X, y):
        #     X_train_fold, X_test_fold = X.iloc[train_index], X.iloc[test_index]
        #     y_train_fold, y_test_fold = y.iloc[train_index], y.iloc[test_index]

        #     self.model.fit(
        #         x=X_train_fold,
        #         y=y_train_fold,
        #         callbacks=[es],
        #         batch_size=200,
        #         epochs=self.epochs,
        #         validation_data=(X_train_fold,y_train_fold)
        #     )

        #     lst_accu_stratified.append(
        #         self.model.evaluate(X_test_fold, y_test_fold))

        # # only accuracy
        # lst_accu_stratified = [inner[1] for inner in lst_accu_stratified]
        # print("List of possible mae:", lst_accu_stratified)
        # print(
        #     "Maximum mae That can be obtained from this model is:",
        #     max(lst_accu_stratified),
        # )
        # print("Minimum mae:", min(lst_accu_stratified))
        # print("Overall mae:", np.average(lst_accu_stratified))


    # def testing_1(self):
        

    #     print("Test set")
    #     print("LOSS", "ACCURACY")

    #     y_test = self.y_test
    #     X_test = self.X_test

    #     # prob as an output
    #     y_prob = self.model.predict(X_test, batch_size=128, verbose=2)
    #     print("PROBS")
    #     print(self.X_test[:5])
    #     print(y_prob[:5])
    #     print(y_prob.shape)

    #     macro_roc_auc_ovo = roc_auc_score(y_test,
    #                                       y_prob,
    #                                       multi_class="ovo",
    #                                       average="macro")
    #     weighted_roc_auc_ovo = roc_auc_score(y_test,
    #                                          y_prob,
    #                                          multi_class="ovo",
    #                                          average="weighted")
    #     macro_roc_auc_ovr = roc_auc_score(y_test,
    #                                       y_prob,
    #                                       multi_class="ovr",
    #                                       average="macro")
    #     weighted_roc_auc_ovr = roc_auc_score(y_test,
    #                                          y_prob,
    #                                          multi_class="ovr",
    #                                          average="weighted")
    #     print("One-vs-One ROC AUC scores:\n{:.6f} (macro),\n{:.6f} "
    #           "(weighted by prevalence)".format(macro_roc_auc_ovo,
    #                                             weighted_roc_auc_ovo))
    #     print("One-vs-Rest ROC AUC scores:\n{:.6f} (macro),\n{:.6f} "
    #           "(weighted by prevalence)".format(macro_roc_auc_ovr,
    #                                             weighted_roc_auc_ovr))

    #     # class transformation

    #     y_pred = np.argmax(y_prob, axis=-1)

    #     print("CLASSES")
    #     print("unique", np.unique(y_pred.tolist()))
    #     print(y_pred.shape)
    #     print(y_pred[:20])

    #     print(
    #         "precision_recall_fscore_support \n",
    #         precision_recall_fscore_support(y_pred=y_pred,
    #                                         y_true=y_test,
    #                                         average="micro"),
    #     )
    #     print(
    #         "confusion_matrix \n",
    #         confusion_matrix(y_pred=y_pred, y_true=y_test),
    #     )
    #     print(
    #         "metrics.recall_score =>",
    #         recall_score(y_pred=y_pred, y_true=y_test, average="micro"),
    #     )
    #     print("cohen_kappa_score => ", cohen_kappa_score(y_pred, y_test))
    #     print(
    #         "metrics.classification_report \n",
    #         classification_report(y_pred=y_pred, y_true=y_test),
    #     )
    #     print(
    #         "metrics.matthews_corrcoef =>",
    #         matthews_corrcoef(y_pred=y_pred, y_true=y_test),
    #     )
    # def testing_2(self):
    #     y_test = self.y_test
    #     X_test = self.X_test

    #     X_columns = X_test.columns
    #     scaler = StandardScaler()
    #     X_test = scaler.fit_transform(X_test)

    #     # X_test = pd.DataFrame(X_test, columns = X_columns)

    #     # print(X_test.shape)

    #     # prob as an output
    #     y_pred = self.model.predict(X_test, batch_size=128, verbose=2)

    #     print(X_test[:5])
    #     print(y_pred[:5])
    #     print(y_test[:5])

    #     print(y_pred.shape)

    #     print("R^2:", r2_score(y_test, y_pred))
    #     print("Mean Absolute Error (MAE):",
    #           mean_absolute_error(y_test, y_pred))
    #     print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
    #     print(
    #         "Mean Absolute Percentage Error (MAPE):",
    #         mean_absolute_percentage_error(y_test, y_pred),
    #     )
    #     print(
    #         "Root Mean Squared Error (RMSE):",
    #         np.sqrt(mean_squared_error(y_test, y_pred)),
    #     )  # np.sqrt

    #     print("Explained Variance Score:",
    #           explained_variance_score(y_test, y_pred))
    #     print("Max Error:", max_error(y_test, y_pred))
    #     # print('Mean Squared Log Error:', mean_squared_log_error(y_test, y_pred))
    #     print("Median Absolute Error:", median_absolute_error(y_test, y_pred))


if __name__ == "__main__":

    # Arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-ml", "--model", help="Predined model run", type=int)
    parser.add_argument(
        "-e",
        "--epochs",
        help="epochs",
        type=int,
        required=True,
        default=0,
    )


    parser.add_argument(
        "-cm",
        "--clients_max",
        help="Maximun number of clients",
        type=int,
        required=True,
    )
    parser.add_argument(
        "-cn",
        "--clients_number",
        help="Number of a specific client <= maximun number of clients",
        type=int,
        required=True,
    )
    parser.add_argument("-dfn",
                        "--data_file_name",
                        help="data file name",
                        type=str)

    parser.add_argument("-ip", "--ip", help="IP address", type=str)

    parser.add_argument("-dfn_test_x",
                        "--dfn_test_x",
                        help="dfn_test_x",
                        type=str)
    

    parser.add_argument("-dfn_test_y",
                    "--dfn_test_y",
                    help="dfn_test_y",
                    type=str)



    args = parser.parse_args()

    model = int(args.model)
    clients_max = int(args.clients_max)
    clients_number = int(args.clients_number)
    epochs = int(args.epochs)
    # learning_rate = float(args.learning_rate)
    data_file_name = str(args.data_file_name)
    ip = str(args.ip)

    dfn_test_x=str(args.dfn_test_x)
    dfn_test_y=str(args.dfn_test_y)

    # Configuration
    root_path = os.path.dirname(os.path.abspath("__file__"))
    os.chdir(root_path)

    RNDSEED = np.random.seed(39)
    np.random.seed(RNDSEED)
    set_seed(RNDSEED)
    os.environ["PYTHONHASHSEED"] = str(RNDSEED)
    rn.seed(RNDSEED)

    independent = Independent(
        data_file_name,
        dfn_test_x,
        dfn_test_y,
        RNDSEED,
        epochs,
        # learning_rate,
        model,
        clients_max,
        clients_number,
        ip,
    )

    independent.load_data()
    if model == 1:
        # centralized.train_cut_split_1()
        # centralized.pre_modeling_1()
        # pass
        independent.modeling_1()
        # centralized.testing_1()
    elif model == 2:
        # centralized.train_cut_split_2()
        # centralized.pre_modeling_2()
        independent.modeling_2()
        # centralized.testing_2()

    exit()

