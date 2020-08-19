from summarizer import SummarizerModel
import pandas as pd
import numpy as np
import sys
import os
import transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import warnings
# from summarizer import Summarizer
from application_logging.logger import App_Logger
import datetime 
import logging
import os
import glob
import argparse

warnings.filterwarnings("ignore")

from Rss_Feed import RssScrapper
scrapper=RssScrapper() # create the object of RssScrapper
scrapper.get_all("test_file")


models = {'bert':'bert-base-uncased',
            'xlnet':'xlnet-base-cased',
            'distilbert':'distilbert-base-uncased',
            'albert':'albert-base-v1',
            'textT5':'Text-to-Text'}

def run(modelname):
    filepath = "Output/Final_news.csv"
    try:        
        model_to_use = models.get(modelname)
        model = SummarizerModel(filepath,model_to_use)
        data = model.getdataframe(filepath)
        print(model_to_use)
        Summary = model.getsummary()
        try:
            data['Summary'] = Summary 
            data.to_csv("Summary.csv",index=None)
        except Exception as e:
            raise e
    except Exception as e:
        raise e



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ModelName",help="choose model for summarization",type=str)
    args = parser.parse_args()
    modelname = args.ModelName
   
    run(modelname)


