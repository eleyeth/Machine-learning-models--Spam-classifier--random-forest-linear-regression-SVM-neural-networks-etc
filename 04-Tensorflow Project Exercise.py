
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# # Tensorflow Project Exercise
# Let's wrap up this Deep Learning by taking a a quick look at the effectiveness of Neural Nets!
# 
# We'll use the [Bank Authentication Data Set](https://archive.ics.uci.edu/ml/datasets/banknote+authentication) from the UCI repository.
# 
# The data consists of 5 columns:
# 
# * variance of Wavelet Transformed image (continuous)
# * skewness of Wavelet Transformed image (continuous)
# * curtosis of Wavelet Transformed image (continuous)
# * entropy of image (continuous)
# * class (integer)
# 
# Where class indicates whether or not a Bank Note was authentic.
# 
# This sort of task is perfectly suited for Neural Networks and Deep Learning! Just follow the instructions below to get started!

# ## Get the Data
# 
# ** Use pandas to read in the bank_note_data.csv file **

# In[2]:


import pandas as pd
import numpy as np
df = pd.read_csv('bank_note_data.csv')


# ** Check the head of the Data **

# In[3]:


df.head()


# ## EDA
# 
# We'll just do a few quick plots of the data.
# 
# ** Import seaborn and set matplolib inline for viewing **

# In[4]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# ** Create a Countplot of the Classes (Authentic 1 vs Fake 0) **

# In[6]:


sns.countplot(x='Class',data=df)


# ** Create a PairPlot of the Data with Seaborn, set Hue to Class **

# In[8]:


sns.pairplot(df,hue='Class')


# ## Data Preparation 
# 
# When using Neural Network and Deep Learning based systems, it is usually a good idea to Standardize your data, this step isn't actually necessary for our particular data set, but let's run through it for practice!
# 
# ### Standard Scaling
# 
# 

# In[9]:


from sklearn.preprocessing import StandardScaler


# **Create a StandardScaler() object called scaler.**

# In[10]:


scaler = StandardScaler()


# **Fit scaler to the features.**

# In[12]:


scaler.fit(df.drop('Class',axis=1))


# **Use the .transform() method to transform the features to a scaled version.**

# In[14]:


scaled_features = scaler.fit_transform(df.drop('Class',axis=1))


# **Convert the scaled features to a dataframe and check the head of this dataframe to make sure the scaling worked.**

# In[22]:


df_feat = pd.DataFrame(scaled_features,columns=df.columns[:-1])
df_feat.head()


# ## Train Test Split
# 
# ** Create two objects X and y which are the scaled feature values and labels respectively.**

# In[24]:


X = df_feat


# In[25]:


y = df['Class']


# ** Use SciKit Learn to create training and testing sets of the data as we've done in previous lectures:**

# In[27]:


from sklearn.model_selection import train_test_split


# In[28]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# # Tensorflow

# In[29]:


import tensorflow as tf


# ** Create a list of feature column objects using tf.feature.numeric_column() as we did in the lecture**

# In[30]:


df_feat.columns


# In[31]:


image_var = tf.feature_column.numeric_column("Image.Var")
image_skew = tf.feature_column.numeric_column('Image.Skew')
image_curt = tf.feature_column.numeric_column('Image.Curt')
entropy =tf.feature_column.numeric_column('Entropy')


# In[32]:


feat_cols = [image_var,image_skew,image_curt,entropy]


# ** Create an object called classifier which is a DNNClassifier from learn. Set it to have 2 classes and a [10,20,10] hidden unit layer structure:**

# In[33]:


classifier = tf.estimator.DNNClassifier(hidden_units=[10, 20, 10], n_classes=2,feature_columns=feat_cols)


# ** Now create a tf.estimator.pandas_input_fn that takes in your X_train, y_train, batch_size and set shuffle=True. You can play around with the batch_size parameter if you want, but let's start by setting it to 20 since our data isn't very big. **

# In[35]:


input_func = tf.estimator.inputs.pandas_input_fn(x=X_train,y=y_train,batch_size=40,shuffle=True)


# ** Now train classifier to the input function. Use steps=500. You can play around with these values if you want!**
# 
# *Note: Ignore any warnings you get, they won't effect your output*

# In[36]:


classifier.train(input_fn=input_func,steps=700)


# ## Model Evaluation

# ** Create another pandas_input_fn that takes in the X_test data for x. Remember this one won't need any y_test info since we will be using this for the network to create its own predictions. Set shuffle=False since we don't need to shuffle for predictions.**

# In[42]:


pred_fn = tf.estimator.inputs.pandas_input_fn(x=X_test,batch_size=len(X_test),shuffle=False)


# ** Use the predict method from the classifier model to create predictions from X_test **

# In[43]:


note_predictions = list(classifier.predict(input_fn=pred_fn))


# In[44]:


note_predictions[0]


# In[45]:


final_preds  = []
for pred in note_predictions:
    final_preds.append(pred['class_ids'][0])


# ** Now create a classification report and a Confusion Matrix. Does anything stand out to you?**

# In[46]:


from sklearn.metrics import classification_report,confusion_matrix


# In[47]:


print(confusion_matrix(y_test,final_preds))


# In[48]:


print(classification_report(y_test,final_preds))


# ## Optional Comparison
# 
# ** You should have noticed extremely accurate results from the DNN model. Let's compare this to a Random Forest Classifier for a reality check!**
# 
# **Use SciKit Learn to Create a Random Forest Classifier and compare the confusion matrix and classification report to the DNN model**

# In[49]:


from sklearn.ensemble import RandomForestClassifier


# In[50]:


rfc = RandomForestClassifier(n_estimators=200)


# In[51]:


rfc.fit(X_train,y_train)


# In[52]:


rfc_preds = rfc.predict(X_test)


# In[53]:


print(classification_report(y_test,rfc_preds))


# In[54]:


print(confusion_matrix(y_test,rfc_preds))


# ** It should have also done very well, possibly perfect! Hopefully you have seen the power of DNN! **

# # Great Job!
