# -*- coding: utf-8 -*-
"""final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T5Dgv69GPS3ha0eQ9lGWt3zPmZIGueMH
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

data=pd.read_csv('/content/drive/My Drive/majorproject/Reviews (1).csv')

data.head()

"""#**Droping unnecesarry columns**"""

data.drop(['Id','ProductId','UserId','ProfileName','Time','Text','HelpfulnessNumerator','HelpfulnessDenominator'],axis=1,inplace=True)

data.head()

data.Score.value_counts().plot(kind = "bar")
plt.title('Number of positive, Neutral & Negative Ratings')
plt.xlabel('Rating Scales')
plt.ylabel('Total ratings')
plt.show()

"""#Applying the sentiment based on scores
Based on the score provide by the customer , we provide the labels as Positive, Negative & Neutral . If Score > 3 we classify it as Positive , if Score < 3 we classify it as Negative . if Score = 3 then it is Neutral.
"""

data.dropna(axis=0,inplace=True)
data['Sentiment']=data['Score'].apply(lambda Score: 'Positive' if Score>3 else('Negative' if Score<3 else 'Neutral'))
index=data[data['Sentiment']=='Neutral'].index
data.drop(index=index,axis=0,inplace=True)
data.Sentiment.value_counts()

#Bar graph to present strength of positive & Negative Review
data['Sentiment'].value_counts().plot(kind ="bar")
plt.title("Analysis fo Positive & Negative reviews")
plt.ylabel("frequency of each comment") 
plt.show()

"""#**Handle Imbalanced Data**"""

data.head()

X=data.iloc[:,1]
y=data['Sentiment']
X.shape

y.shape

from nltk.corpus import stopwords

nltk.download('stopwords')

!pip install wordcloud

from wordcloud import WordCloud, STOPWORDS

stopwords = set(STOPWORDS)
def Mywordcloud(data, title = None):
  wordcloud = WordCloud(
      background_color = 'Black',
      stopwords = stopwords,
      max_words = 400,
      max_font_size = 40,
      scale = 3,
      random_state = 1
  ).generate(str(data))

  fig = plt.figure(1, figsize = (15,15))
  plt.axis('off')
  if title:
    fig.suptitle(title, fontsize=40)
    fig.subplots_adjust(top=2.3)

  plt.imshow(wordcloud)
  plt.show()


Mywordcloud(data['Summary'],'Summary WordCloud')

Mywordcloud(data[data['Sentiment']=='Positive'],'Positive Review')

Mywordcloud(data[data['Sentiment']=='Negative'],'Negative Review')

"""#Preparing The Model"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

xtrain,xtest,ytrain,ytest=train_test_split(X,y,test_size=0.3,random_state=0)

cv = CountVectorizer()
xtrain_tr = cv.fit_transform(xtrain)
xtest_tr= cv.transform(xtest)

from sklearn.linear_model import LogisticRegression
clf=LogisticRegression()
clf.fit(xtrain_tr,ytrain)

ypred=clf.predict(xtest_tr)
ypred

score=accuracy_score(ypred,ytest)
score

print(classification_report(ypred,ytest))

df= {'review':input('enter your reviev :')}
df=pd.DataFrame(df,index=[0])
to_pred=df.iloc[:,0]
result=clf.predict(cv.transform(to_pred))
print(str(result[0]))

confusion_matrix(ypred,ytest)

!pip install streamlit

!pip install pyngrok

from pyngrok import ngrok
ngrok.connect(port='8501')

# Commented out IPython magic to ensure Python compatibility.
# %%writefile ML_APP.py
# import streamlit as st
# from PIL import Image
# from sklearn.feature_extraction.text import CountVectorizer
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
# data=pd.read_csv('/content/drive/My Drive/majorproject/Reviews (1).csv')
# data.drop(['Id','ProductId','UserId','ProfileName','Time','Text','HelpfulnessNumerator','HelpfulnessDenominator'],axis=1,inplace=True)
# data.dropna(axis=0,inplace=True)
# data['Sentiment']=data['Score'].apply(lambda Score: 'Positive' if Score>3 else('Negative' if Score<3 else "Neutral"))
# index=data[data['Sentiment']==0].index
# data.drop(index=index,axis=0,inplace=True)
# X=data.iloc[:,1]
# y=data['Sentiment']
# xtrain,xtest,ytrain,ytest=train_test_split(X,y,test_size=0.3,random_state=0)
# cv = CountVectorizer()
# xtrain_tr = cv.fit_transform(xtrain)
# xtest_tr= cv.transform(xtest)
# from sklearn.linear_model import LogisticRegression
# clf=LogisticRegression()
# clf.fit(xtrain_tr,ytrain)
# 
# 
# 
# 
# 
# st.title("SENTIMENT ANALYSIS")
# image=Image.open('/content/drive/My Drive/majorproject/Screenshot (21).png')
# st.image(image,width=800)
# review=st.text_input('Enter your short review :')
# df= {'review':review}
# df=pd.DataFrame(df,index=[0])
# to_pred=df.iloc[:,0]
# result=clf.predict(cv.transform(to_pred))
# if(st.button('Predict')):
#     st.write(result[0])

!streamlit run ML_APP.py  

