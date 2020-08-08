## TextSumarization_DistilBertModel
It takes an 
[-path PATH] 
[-model MODEL]

# How to use it?
Open terminal and run
python TextSumarization.py [-h] [-path PATH] [-model MODEL]

# files are Resposible:
Textsumarization.py,
Utility.py
# Ex:
python TextSumarization.py -path "TextFilepath",-model "MODEL"
By default it uses DistilBertModel and the Test Data('Final_news.csv') with contain in this Repo


# Works for pretrainedModel of Bart:
* BertModel('bert-base-uncased','bert-large-uncased')
* XLNetModel('xlnet-base-cased')
* XLMModel('xlm-mlm-enfr-1024')
* DistilBertModel('distilbert-base-uncased')
* AlbertModel('albert-base-v1','albert-large-v1')

# Note: 
This Repo is under Development by the ineuron Intern batch 

# License
© 2020 

# This repository is licensed under the MIT license. See LICENSE for details.
