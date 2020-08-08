import pandas as pd
import numpy as np
import sys
import os
import transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import warnings
# from summarizer import Summarizer
from application_logging.logger import App_Logger
warnings.filterwarnings("ignore")


class SummarizerModel:
    
    def __init__(self,filepath,model):
        self.logger_object = App_Logger()
        self.general_logs = open("Logs/generallogs.txt",'+a')
        self.success_file = open("Logs/successlogs.txt",'+a')
        self.error_file = open("Logs/errorlogs.txt",'+a')
        self.filepath = filepath
        self.model = model

    def getdata(self):
        file_types=('csv','json','txt')
        self.logger_object.log(self.general_logs,"Entering getdata Method !")
        try:
            self.logger_object.log(self.success_file,"Entered get data method loading the dataset now !")
            file_ext  = os.path.split(self.filepath)[-1].split(".")[-1]
            if file_ext in file_types:
                if file_ext == "csv":
                   news_df= pd.read_csv(self.filepath)
                   articles = list(news_df.Description)
                   return articles
                elif file_ext == "json":
                    news_df = pd.read_json(self.filepath)
                    articles = news_df.Description
                    return articles
                elif file_ext == "txt":
                    articles = open(self.filepath,'r')
                    return articles
            self.logger_object.log(self.success_file,"Successfully read the data !")
        except Exception as e:
            self.logger_object.log(self.error_file,"Failed to load data INVALID file type provided :" + str(e))
            raise e

    def getdataframe(self,filepath):
        file_types=('csv','json','txt')
        self.logger_object.log(self.general_logs,"Entering getdataframe Method !")
        try:
            self.logger_object.log(self.success_file,"Entered get data method loading the dataset now !")
            file_ext  = os.path.split(self.filepath)[-1].split(".")[-1]
            if file_ext in file_types:
                if file_ext == "csv":
                    news_df= pd.read_csv(self.filepath)
                    news_df = news_df[['Description']]
                    return news_df
                elif file_ext == "json":
                    news_df = pd.read_json(self.filepath)
                    news_df = news_df[['Description']]
                    return news_df
                elif file_ext == "txt":
                    articles = open(self.filepath,'r')
                    # return articles
            self.logger_object.log(self.success_file,"Successfully read the data !")
        except Exception as e:
            self.logger_object.log(self.error_file,"Failed to load data INVALID file type provided :" + str(e))
            raise e


    def loadmodel(self):
        self.logger_object.log(self.general_logs,"Entering loadmodel method !")
        try:
            self.logger_object.log(self.general_logs,"Checking the model name entered by user!")
            if self.model == 'Text-to-Text':
                Model = T5ForConditionalGeneration.from_pretrained('t5-small')
                tokenizer = T5Tokenizer.from_pretrained('t5-small')
            else:
                Model = Summarizer(self.model)
            self.logger_object.log(self.success_file,"Successfully loaded the model !")
        except Exception as e:
            self.logger_object.log(self.error_file,"Failed to load the model :" + str(e))
            raise e
        return Model,tokenizer 

    
    def getsummary(self):
        summaries = []
        self.logger_object.log(self.general_logs,"Entered getsummary method ")
        try:
            self.logger_object.log(self.general_logs,"Trying to load model,articles,tokenizer !")
            self.articles = self.getdata()
            self.Model,self.tokenizer = self.loadmodel()
            self.logger_object.log(self.success_file,"Successfully loaded the model,articles and tokenizer !")
        except Exception as e:
            self.logger_object.log(self.error_file,"Failed to get the model, articles and tokenizer !")
            raise e

        self.logger_object.log(self.general_logs,"Entered step of extracting summaries !")
        try:
            self.logger_object.log(self.general_logs,"Generating summaries now !")
            if self.model == 'Text-to-Text':
                for i in self.articles:
                    preprocess_text = i.strip().replace("\n","")
                    t5_prepared_Text = "summarize: "+preprocess_text
                    tokenized_text = self.tokenizer.encode(t5_prepared_Text, return_tensors="pt")
                    summary_ids = self.Model.generate(tokenized_text,
                                                        num_beams=4,
                                                        no_repeat_ngram_size=2,
                                                        min_length=60,
                                                        max_length=400,
                                                        early_stopping=True)

                    summary_text = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                    summaries.append(summary_text)
            else:
                for i in self.articles:
                    output_text = self.Model(i,min_length=60)
                    summary_text = ''.join(output_text)
                    summaries.append(summary_text)
            self.logger_object.log(self.success_file,"Successfully generated summaries !")

        except Exception as e:
            self.logger_object.log(self.error_file,"Failed to generate summaries !" + str(e))
            raise e
        return summaries
