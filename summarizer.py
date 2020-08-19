import pandas as pd
import numpy as np
import sys
import os
import datetime 
import logging
import glob
import os
import transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import warnings
# from summarizer import Summarizer
from application_logging.logger import App_Logger
warnings.filterwarnings("ignore")

class SummarizerModel(App_Logger):
    
    def __init__(self,filepath,model):

        App_Logger.__init__(self)
        self.CODE_DIR = os.getcwd()
        self.success_logpath= self.CODE_DIR + '/logs/success/*'
        self.list_of_success_files = glob.glob(self.success_logpath) 
        self.latest_success_file = max(self.list_of_success_files, key=os.path.getctime)
        # print(self.latest_success_file)
        self.failure_logpath = self.CODE_DIR + '/logs/failure/*'
        self.list_of_failure_files = glob.glob(self.failure_logpath) 
        self.latest_error_file = max(self.list_of_failure_files, key=os.path.getctime)
        # print(self.latest_error_file)

        self.success_logger = self.create_success_logger(self.latest_success_file)
        self.failure_logger = self.create_failure_logger(self.latest_error_file)
        self.filepath = filepath
        self.model = model

    def getdata(self):
        file_types=('csv','json','txt')
        try:
            self.success_logger.info("Entered get data method loading the dataset now !")
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
            self.success_logger.info("Successfully read the data !")
        except Exception as e:
            self.failure_logger.error("Failed to load data INVALID file type provided :" + str(e))
            raise e

    def getdataframe(self,filepath): # this function loads the dataset for making final summary dataset
        file_types=('csv','json','txt')
        try:
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
        except Exception as e:
            raise e


    def loadmodel(self):
        self.success_logger.info("Entering loadmodel method !")
        try:
            if self.model == 'Text-to-Text':
                Model = T5ForConditionalGeneration.from_pretrained('t5-small')
                tokenizer = T5Tokenizer.from_pretrained('t5-small')
            else:
                Model = Summarizer(self.model)
            self.success_logger.info("Successfully loaded the model !")
        except Exception as e:
            self.failure_logger.error("Failed to load the model :" + str(e))
            raise e
        return Model,tokenizer 

    
    def getsummary(self):
        summaries = []
        self.success_logger.info("Entered getsummary method")
        try:
            self.success_logger.info("Trying to load model,articles,tokenizer !")
            self.articles = self.getdata()
            self.Model,self.tokenizer = self.loadmodel()
            self.success_logger.info("Successfully loaded the model,articles and tokenizer !")
        except Exception as e:
            self.failure_logger.error("Failed to get the model, articles and tokenizer !" + str(e))
            raise e

        try:
            self.success_logger.info("Generating summaries now !")
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
            self.success_logger.info("Successfully generated Summaries !")

        except Exception as e:
            self.failure_logger.error("Failed to generate summaries !" + str(e))
            raise e
        return summaries
