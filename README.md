## TextSumarization_DistilBertModel

# How to use it?
Open terminal and run
python runner.py 

# files are Resposible:
* summarizer.py
* runner.py
# you can choose models:
models = {'bert':'bert-base-uncased',
           'xlnet':'xlnet-base-cased',
           'distilbert':'distilbert-base-uncased',
           'albert':'albert-base-v1',
           'textT5':'Text-to-Text'}
           
enter model name like textT5 etc. 

# Works for pretrainedModel of Bart:
* BertModel('bert-base-uncased','bert-large-uncased')
* XLNetModel('xlnet-base-cased')
* XLMModel('xlm-mlm-enfr-1024')
* DistilBertModel('distilbert-base-uncased')
* AlbertModel('albert-base-v1','albert-large-v1')

# input:
* .csv file with Description header.
# output
* a csv file is created containing two columns first of description second of summary !

# Note: 
This Repo is under Development by the Ineuron intern batch 

# License
© 2020 This repository is licensed under the MIT license. See LICENSE for details.
