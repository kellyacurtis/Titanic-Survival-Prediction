# -*- coding: utf-8 -*-
"""cse354_project_Group_30.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QGxBcrtHqkDOLKAdYTVPta5qRCfW71Fd
"""

# load the training data and assess
import pandas as pd

train_df = pd.read_csv('/content/train.csv')
train_df.head(50)

# view missing values in training data

missing_values = train_df.isnull().sum()
print(missing_values)

train_df.info()

# Clean the dataset, remove the outliers, before any data analysis.

# cleaning the train data
oldest_ages = train_df['Age'].sort_values(ascending=False).head(10)
print(oldest_ages)

# replacing NaN age with median
age_median = train_df['Age'].median()
train_df['Age'].fillna(age_median, inplace=True)

# replacing NaN cabin with the unknown
train_df['Cabin'].fillna('Unknown', inplace=True)

# replacing embarked NaN values with most common
train_df['Embarked'].fillna(train_df['Embarked'].mode()[0], inplace=True)

# checking if values are now all filled
missing_values = train_df.isnull().sum()
print(missing_values)
train_df.info()

"""1. Age(float): age has a significant amount of values missing. This can be replaced by the average age.
2. cabin(object): has a significant amount of NaN values.
"""

# making sure no ages are valued at zero
zero_age_entries = train_df[train_df['Age'] == 0]
zero_age_count = len(zero_age_entries)

print(f'Number of entries with age 0: {zero_age_count}')
print(zero_age_entries)

import seaborn as sns
import matplotlib.pyplot as plt

# plot relationship between sex and survival
plt.figure(figsize=(8, 6))
sns.barplot(x='Sex', y='Survived', data=train_df, hue='Sex', errorbar=None, palette= 'crest')
plt.title('Titanic Shipwreck Survival Rate by Sex')
plt.xlabel('Sex')
plt.ylabel('Survival Rate')
plt.show()
print()

# plot relationship between class and survival
sns.barplot(x='Pclass', y='Survived', data=train_df, hue='Pclass', errorbar=None, palette= 'crest')
plt.title('Titanic Shipwreck Survival Rate by Class')
plt.xlabel('Class')
plt.show()
print()

# plot relationship between age and survival
sns.histplot(data=train_df, x='Age', hue='Survived', multiple='stack', kde=True, palette= 'crest')
plt.title('Titanic Shipwreck Age Distribution by Survival')
plt.ylabel('Number of Passengers')
plt.show()
print()

# plot showing the amount of passengers by class and Gender
plt.figure(figsize=(14, 8))
sns.barplot(x='Pclass', y='Survived', hue='Sex', errorbar=None, data=train_df, palette='crest')
plt.title('Titanic Shipwreck Survival of Passengers by Class and Gender')
plt.xlabel('Class')
plt.ylabel('Survival Rate')
plt.ylim(0, 1)
plt.legend(title='Gender')
plt.show()
print()

# plot relationship between class and age
plt.figure(figsize=(10, 6))
sns.boxplot(x='Pclass', y='Age', data=train_df, hue='Pclass', palette= 'crest')
plt.title('Titanic Shipwreck Age Distribution by Class')
plt.xlabel('Class')
plt.show()
print()


# plot the relationship between survival and age by sex
train_df['AgeGroup'] = pd.cut(train_df['Age'], bins=range(0, 81, 10),labels = [
    '0-10',
    '10-20',
    '20-30',
    '30-40',
    '40-50',
    '50-60',
    '60-70',
    '70-80'
])

age_group_survival = train_df.groupby(['AgeGroup', 'Sex'])['Survived'].mean().reset_index()


plt.figure(figsize=(10, 8))
sns.barplot(data=age_group_survival, x='AgeGroup', y='Survived', hue='Sex', palette= 'crest')
plt.title('Titanic Shipwreck Survival Rate by Age Group and Class')
plt.xlabel('Age Group')
plt.ylabel('Survival Rate')
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.show()
print()

# plot relationship between age group and survival
train_df['AgeGroup'] = pd.cut(train_df['Age'], bins=range(0, 81, 15), labels=['0-14', '15-29', '30-44', '45-59', '60+'])

age_group_survival = train_df.groupby(['AgeGroup'])['Survived'].mean()

plt.figure(figsize=(10, 8))
sns.barplot(x=age_group_survival.index, y=age_group_survival.values, hue= age_group_survival.index, palette= 'crest')
plt.title('Titanic Shipwreck Survival Rate by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Survival Rate')
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.show()

# assess what features are most significant

features = ['Survived','Pclass', 'Sex', 'Age', ]
df_selected = train_df[features]

X_dummies = pd.get_dummies(df_selected)
X_dummies = X_dummies.astype(int)

# calc pearson correlation matrix
corr_matrix = X_dummies.corr()

# plot heat map of these correlations
plt.figure(figsize=(14, 8))
sns.heatmap(corr_matrix, annot=True, cmap='crest', center=0, vmin=-1, vmax=1)
plt.show()

# Prepare data more modeling
import pandas as pd
from sklearn.model_selection import train_test_split


# take the features with the most significance
features = ['Pclass', 'Sex', 'Age']
train_features = train_df[features]

# encode features
X_dummies = pd.get_dummies(train_features)
X_dummies = X_dummies.astype(int)

# entire target variable column "Survived"
y = train_df.Survived

# 80/20 split for train and test because test.csv doesn't have a survived column
X_train, X_test, y_train, y_test = train_test_split(X_dummies, y, test_size=0.20, random_state=16)
X_dummies.head()

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# logistic regression model fitting out training features to our target survived
logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)

# predicting the outcome survived on the test
y_pred_lr = logreg.predict(X_test)

print("Logistic Regression Model")
# assessing how well our predictions match our actual values for survived
print("Accuracy:", accuracy_score(y_test, y_pred_lr))
print("Classification Report:\n", classification_report(y_test, y_pred_lr))

from sklearn import metrics


cv_scores = cross_val_score(logreg, X_train, y_train, cv=10, scoring='accuracy')
print("Cross-Validation Accuracy Scores:", cv_scores)
print("Mean Cross-Validation Accuracy:", cv_scores.mean())

# confusion matric for Logistic Regression Model Predicting Survival

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


plt.figure(figsize=(7, 5))
cnf_matrix = confusion_matrix(y_test, y_pred_lr)
class_names=[0,1]
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="crest" ,fmt='g')
plt.title('Confusion Matrix for Logistic Regression Model Predicting Survival')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
plt.show()

from sklearn.tree import DecisionTreeClassifier

# DT model fitting out training features to our target survived
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

# predicting the outcome survived on the test
y_pred_dt = dt.predict(X_test)
print("Decison Tree Model")
# assessing how well our predictions match our actual values for survived
print()
print("Accuracy:", accuracy_score(y_test,y_pred_dt))
print("Classification Report:\n", classification_report(y_test, y_pred_dt))

cv_scores = cross_val_score(dt, X_train, y_train, cv=10, scoring='accuracy')
print("Cross-Validation Accuracy Scores:", cv_scores)
print("Mean Cross-Validation Accuracy:", cv_scores.mean())

# confusion matric for DT Model Predicting Survival

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

plt.figure(figsize=(7, 5))
cnf_matrix = confusion_matrix(y_test, y_pred_dt)
class_names = [0, 1]
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="crest", fmt='g')
plt.title('')
plt.tight_layout()
plt.title('Confusion Matrix for Decision Tree Model Predicting Survival')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
plt.show()

from sklearn.neighbors import KNeighborsClassifier

# KNN model fitting out training features to our target survived
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# predicting the outcome survived on the test
y_pred_knn = knn.predict(X_test)

print("KNN Model")
# assessing how well our predictions match our actual values for survived
print()
print(f'Accuracy: {accuracy_score(y_test, y_pred_knn)}')
print()
print(f'Classification Report:\n\n{classification_report(y_test, y_pred_knn)}')

cv_scores = cross_val_score(knn, X_train, y_train, cv=10, scoring='accuracy')
print("Cross-Validation Accuracy Scores:\n", cv_scores)
print("Mean Cross-Validation Accuracy:", cv_scores.mean())

# confusion matric for KNN Model Predicting Survival
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

plt.figure(figsize=(7, 5))
cnf_matrix = confusion_matrix(y_test, y_pred_knn)
class_names = [0, 1]
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="crest", fmt='g')
plt.title('Confusion Matrix for KNN Model Predicting Survival')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
plt.show()

"""2.
  1. Logistic Regression - This modeling method is considered to be one that finds the best fitting line that separates classes in a given training data set(in our case, survived or did not survive). Using the logistic function, or sigmoid function, to map variables between 0 and 1, we can give the probability of a given variable being a part of particular class(greater than 0.5 it is considered to be in class 1, less than 0.5 in class 0). Additionally, logistic regression attempts to learn the weight coefficients that minimize loss, with the loss function, between our predicted and actual results using gradient descent. This helps us find the best classification separator between binary classes.
  2. Decision Trees - This method of training is based on the use of a branching structure that classifies data into some category using decisionary rules. Our nodes in this structure consist of some feature comparision, like "is the input a female", and then based on this condition, we proceed to either the left or right child node consisting of potentially other decisionary conditions or to the final node. We make predictions by traversing this tree following these decisionary rules we've established.
  3. K-Nearest Neighbors - Modeling with KNN involves determining the class of a particular point based on using distance to find the class of its closest neighbors. Predictions on based on using a query point q, finding the distances between all other points, and taking the class label of the majority label amongst k-nearest neighbors.

3.
  1. Logistic Regression:           
    Accuracy: 0.7653631284916201

    About 76.5% of the model predictions were accurate at determining who would survive.
  2. Decision Tree:
    Accuracy: 0.7988826815642458

    About 79.9% of the model predictions were accurate at determining who would survive.

  3. KNN:
    Accuracy: 0.7597765363128491

    About 76.0% of the model predictions were accurate at determining who would survive.

  These predictions are fairly decent, but could potentially be improved if we introduce cross validation when splitting the data into our training and test sets.

  

4.One possible factor hindering our model's performance may be the inclusion of outliers in age, ages in the 70-80 range. In taking steps to remove or replace the outliers with more representative values, we could potentially improve our model performance. In viewing our dataset, it appears that younger males had a greater rate of survival while older females had a greater rate of survival; this, however, is with the exception of the 70-80 year age group. Consisting of only males, a survival rate that mirrors that of the 40-50 year age group appears in the 70-80 group, thus likely weakening the model's performance in predicting the survival of males.

5.
  1. Logistic Regression:

               precision    recall  f1-score   support

           0       0.77      0.86      0.81       107
           1       0.75      0.62      0.68        72
           
           Accuracy: 0.7653631284916201

    Accuracy overall is fairly high at 76.5%. The model is producing a higher recall and precision for 0, meaning that the model may be finding non-survivors better than survivors.
    
    High recall for 0 means our model is accurately identifying 88% of the non-survivors. Lower recall for 1 at 62% of survivors are accurately identifying who will survive by the model.
    
    Both precision scores were fairly close, where 77% of non-survivors were true non survivors and 75% of survivors were true as survivors.
    
  2. Decision Tree:

               precision    recall  f1-score   support

           0       0.79      0.90      0.84       107
           1       0.81      0.65      0.72        72

           Accuracy: 0.7988826815642458

    Accuracy overall is fairly high at 79.9%. The model is producing a higher recall and precision for 0, meaning that the model may be finding non-survivors better than survivors.

    High recall for 0 means our model is accurately identifying 90% of the non-survivors. Lower recall for 1 at 65% of survivors are accurately identifying who will survive by the model.
    
    Both precision scores were fairly close, where 79% of non-survivors were true non survivors and 81% of survivors were true as survivors.

  3. KNN:

              precision    recall  f1-score   support

           0       0.77      0.86      0.81       107
           1       0.75      0.61      0.67        72

           Accuracy: 0.7597765363128491

    While the accuracy for KNN is still fairly high, this model performed the worst amoung all of the classifiers with an accuracy of 76.0%. The model is producing a higher recall and precision for 0, meaning that the model may be finding non-survivors better than survivors.

    High recall for 0 means our model is accurately classified 86% of the non-survivors. Lower recall for 1 at 61% of survivors are accurately classified who will survive by the model.
    
    Both precision scores were fairly close, where 77% of non-survivors were true non survivors and 75% of survivors were true as survivors.
    
    
  Overall, the Decision Tree Model performed the best compared to other models with an accuracy of 70.9% and a cross validation accuracy at 81.6%. However, the recall measurement for survivors was lower than other measurements, meaning the model may have trouble classifying survivors.


6. The cross-validation accuracy for each model was higher than each model's accuracy. Our models are performing lower than the cross validation set, and this is means that splitting the training and test data using cross validation, or using 10 total splits in our case, gave a more accurate measure of each model performance.

Used Resources:

https://www.datacamp.com/tutorial/understanding-logistic-regression-python

Contributions:

Kelly: Data cleaning and preprocessing, modeling and getting model performance, started demo.
Joshua: Exploratory data analysis and finding relevant features, evaluating model performance, added to and completed demo powerpoint.
"""