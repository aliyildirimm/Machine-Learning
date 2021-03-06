# -*- coding: utf-8 -*-
"""hw2-yildirim-ali.ipynb


**CS412 - Machine Learning - 2020**

Homework 2

**Goal**

The goal of this homework is to get familiar feature handling and cross validation.

**Dataset**

German Credit Risk dataset, prepared by Prof. Hoffman, classifies each person as having a good or bad credit risk. The dataset that we use consists of both numerical and categorical features.

**Task**

Build a k-NN classifier with scikit-learn library to classify people as bad or good risks for the german credit dataset.

**1)** **Initialize**
"""

from google.colab import drive
drive.mount('/content/drive')

from google.colab import drive
drive.mount('/content/drive')

"""**2) Load Dataset**"""

import pandas as pd

train_df = pd.read_csv('/content/drive/My Drive/german_credit_train.csv')
test_df = pd.read_csv('/content/drive/My Drive/german_credit_test.csv')

"""**3) Optional -Analyze the Dataset**

* Display the number of instances and features 
in the train 
* Display 5 random examples from the train 

* Display the information about each features

"""

# Print shape
print("Train data dimensionality: ", train_df.shape)

# Print random 5 rows
print("Examples from train data: ") 
train_df.sample(5)

# Print the information about the dataset
print("Information about train data ", train_df.info() )

"""**4) Define your train and test labels**

*  Define labels for both train and test data in new arrays 
*  And remove the label column from both train and test sets do tht it is not used as a feature.

"""

from sklearn.utils import shuffle
train_df = shuffle(train_df, random_state=42)

train_label = train_df.pop('Risk')
test_label  = test_df.pop('Risk')

train_label.shape
#train_df.columns

"""**5) Handle missing values if any**

*   Print the columns that have **NaN** values 
*   Impute missing values with mode of that feature or remove samples or attributes
"""

# Print columns with NaN values
print(train_df.isnull().any(), "\n")

print(test_df.isnull().any(), "\n")

print("\nNan values percentege for housing in train data ",
      train_df['Housing'].isnull().sum()/len(train_df))

print("\nNan values percentege for housing in test data ",
      test_df['Housing'].isnull().sum()/len(test_df))

train_df['Housing'] = train_df['Housing'].fillna(train_df['Housing'].mode()[0])
test_df['Housing']  = test_df['Housing'].fillna(train_df['Housing'].mode()[0])

train_df.info(), test_df.info()

"""**6) Transform categorical / ordinal features**

* Transform all categorical / ordinal features.

*  The class of the categorical attributes in the dataset are defined as follows:
  - Status of existing checking account
     - A11 :      ... <    0 DM
	- A12 : 0 <= ... <  200 DM
	- A13 :      ... >= 200 DM / salary assignments for at least 1 year
     - A14 : no checking account

 - Credit history
    - A30 : no credits taken/all credits paid back duly
    - A31 : all credits at this bank paid back duly
	- A32 : existing credits paid back duly till now
    - A33 : delay in paying off in the past
	- A34 : critical account/other credits existing (not at this bank)

  - Savings account
    - A61 :          ... <  100 DM
	- A62 :   100 <= ... <  500 DM
	- A63 :   500 <= ... < 1000 DM
	- A64 :          .. >= 1000 DM
    - A65 :   unknown/ no savings account

 - Employment Since
    - A71 : unemployed
    - A72 :       ... < 1 year
	- A73 : 1  <= ... < 4 years  
	- A74 : 4  <= ... < 7 years
	- A75 :       .. >= 7 years
 
 - Personal Status
    - A91 : male   : divorced/separated
	- A92 : female : divorced/separated/married
    - A93 : male   : single
	- A94 : male   : married/widowed
	- A95 : female : single

  - Property
     -  A121 : real estate
	- A122 : if not A121 : building society savings agreement/life insurance
    - A123 : if not A121/A122 : car or other, not in attribute 6
	- A124 : unknown / no property

 - OtherInstallPlans  
    - A141 : bank
	- A142 : stores
	- A143 : none

 - Housing
    -  A151 : rent
	 - A152 : own
	- A153 : for free
"""

#for col in train_df.select_dtypes('object'):
  #print(col, train_df[col].unique())

"""**6.1) Ordinal Features**"""

account_status_map        = {'A14': 0, 'A11':1,  'A12':2, 'A13':3}
train_df['AccountStatus'] = train_df['AccountStatus'].replace(account_status_map)
test_df['AccountStatus']  = test_df['AccountStatus'].replace(account_status_map)

saving_account_map          = {'A65': 0, 'A61':1,  'A62':2, 'A63':3, 'A64':4}
train_df['SavingsAccount'] = train_df['SavingsAccount'].replace(saving_account_map)
test_df['SavingsAccount']  = test_df['SavingsAccount'].replace(saving_account_map)

employt_since_map           = {'A71': 0, 'A73':1,  'A75':2, 'A74':3, 'A72':4 }
train_df['EmploymentSince'] = train_df['EmploymentSince'].replace(employt_since_map)
test_df['EmploymentSince'] = test_df['EmploymentSince'].replace(employt_since_map)

pers_status_map             = {'A93': 0, 'A91':1,  'A92':2, 'A94':3}
train_df['PersonalStatus'] = train_df['PersonalStatus'].replace(pers_status_map)
test_df['PersonalStatus']  = test_df['PersonalStatus'].replace(pers_status_map)

property_map                = {'A124': 0, 'A121':1,  'A122':2, 'A123':3}
train_df['Property']       = train_df['Property'].replace(property_map)
test_df['Property']        = test_df['Property'].replace(property_map)


#train_df = train_df.pop('PersonalStatus')
#test_df  = test_df.pop('PersonalStatus')

"""**6.2) Categorical Features**"""

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

columnTransformer = ColumnTransformer([('encoder', OneHotEncoder(), 
                                       ['CreditHistory','OtherInstallPlans', 'Housing'])],                                        
                                       remainder='passthrough')
train_df = pd.DataFrame(columnTransformer.fit_transform(train_df))
test_df  = pd.DataFrame(columnTransformer.transform(test_df))


columns = ['CreditHistory_a','CreditHistory_b','CreditHistory_c','CreditHistory_d','CreditHistory_e',
           'OtherInstallPlans_a','OtherInstallPlans_b','OtherInstallPlans_c',
           'Housing_a','Housing_b','Housing_c',
           'AccountStatus','Duration','CreditAmount','SavingsAccount',
           'EmploymentSince','PercentOfIncome','PersonalStatus', 'Property', 'Age']

train_df.columns = columns
test_df.columns = columns

train_df

"""**7) Build a k-NN classifier on training data and perform models selection using 5 fold cross validation**

* Initialize k-NN classifiers with k= 5, 10, 15.
* Calculate the cross validation scores using cross_al_score method, number of folds is 5.

"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from statistics import mean

# k values
kVals = [5, 10, 15]

# Save the accuracies of each value of kVal in [accuracies] variable
accuracies = []

# Loop over values of k for the k-Nearest Neighbor classifier
for k in kVals:
  # Initialize a k-NN classifier with k neighbors
  knn = KNeighborsClassifier(n_neighbors=k)

  # Calculate the 5 fold cross validation scores using cross_val_score
  # cv parameter: number of folds, in our case it must be 5
  scores = cross_val_score(knn, train_df, train_label, cv = 5)

  # Stores the average accuracies of the scores in accuracies variable,
  # you can use mean method
  accuracies.append(scores.mean())

for i in range(len(kVals)):
  print("For k = ", kVals[i], "average accuracy on training data set is", accuracies[i], "\n")

"""**8) Retrain using all training data and test on test set**

* Train a classifier with the chosen k value of the best classifier using **all training data**. 
"""

from sklearn.metrics import accuracy_score
import numpy as np

# Train the best classifier using all training set
best_tree = KNeighborsClassifier(n_neighbors = kVals[np.argmax(accuracies)])
best_tree.fit(train_df, train_label)
# Estimate the prediction of the test data
pred = best_tree.predict(test_df)

# Print accuracy of test data
accuracy = accuracy_score(pred, test_label)
print('Accuracy for the best model:', accuracy, " with k = ", kVals[np.argmax(accuracies)])

"""**9) Bonus**"""

#copying train and test data
train_new = train_df
test_new  = test_df

#min-max normalization
#train_new = (train_df - train_df.min())/(train_df.max() - train_df.min())
#test_new  = (test_df - test_df.min())/(test_df.max() - test_df.min())

#first improvement
train_new = train_new.drop('Age',  axis = 1)
test_new  = test_new.drop('Age', axis = 1 )

# second improvement = write n_neighbors = 22

# Train the best classifier using all training set
best_tree = KNeighborsClassifier(n_neighbors=kVals[np.argmax(accuracies)])
best_tree.fit(train_new,train_label)
pred_new  = best_tree.predict(test_new)

# Print accuracy of test data
accuracy_new = accuracy_score(pred_new, test_label)
print('After normalization accuracy for the best model:', accuracy_new, " with k = ",
      kVals[np.argmax(accuracies)])

"""**10) Notebook & Report** 

In this homework, it is aimed to form a Machine Learning model that can classify people as bad or good risks for the German Credit dataset by using a k-NN algorithm. The data set consists of 1000 examples and each example had 20 features (i.e. columns). However, in this model, only 12 of them were used. Training data set composed of 800 instances whereas test data set composed of 200 instances. At the beginning of the algoritm NaN values are checked. Then we saw that Housing has some missing values. 10 percent of the data was missing and they are filled with the mode value of House column. After that categorical and ordinal features are transformed because they need to be compatible to modelling. Firstly, ordinal features are transformed by using simple mapping algoritm. Then for the remaining features which could be infered as categorical was transformed by using Column Transformer and One Hot Encoder. After that, k-NN algorithm was implemented with 5 fold cross-validation. Given k value count was initially 3. In my final running, model had best value on k = 10. This k was chosen and used for train set, the developed model with best k has tested on the test set, and obtained accuracy is 0.675.

However, as I worked on the training data set and done some tests on them, I found another k values which I found to be more succesfull. For example for k = 22 obtained accuracy becomes 0.68. ın addition to that we can also make some removal operations. For the bes k obtained in the training data set, I dropped age column from training data set and run the model again. Accuracy increased to 0.68. However, making k = 22, and dropping age column at same time did not affect much and accuracy stayed at 0.68. Thus making k = 22, or dropping age column is my only solutions to increment accuracy more.
"""
