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
import argparse
warnings.filterwarnings("ignore")

logger_object = App_Logger()
general_logs = open("Logs/generallogs.txt",'+a')
success_file = open("Logs/successlogs.txt",'+a')
error_file = open("Logs/errorlogs.txt",'+a')

models = {'bert':'bert-base-uncased',
            'xlnet':'xlnet-base-cased',
            'distilbert':'distilbert-base-uncased',
            'albert':'albert-base-v1',
            'textT5':'Text-to-Text'}

def run(filepath,modelname):
    try:
        logger_object.log(general_logs,"Entered the runner file --> Running the script now !")
        
        model_to_use = models.get(modelname)
        model = SummarizerModel(filepath,model_to_use)
        data = model.getdataframe(filepath)
        print(model_to_use)
        Summary = model.getsummary()
        logger_object.log(general_logs,"Writing summaries to a text file now !")
        try:
            data['Summary'] = Summary 
            data.to_csv("Summary.csv",index=None)
            # with open('summary.txt', 'w') as f:
            #     for item in Summary:
            #         f.write("%s\n\n" % item)
            logger_object.log(success_file,"Successfully wrote summaries to a csv file !")
        except Exception as e:
            logger_object.log(error_file,"Failed to write summaries to a csv file " + str(e))
            raise e
        logger_object.log(success_file,"Process completed Successfully !")
    except Exception as e:
        logger_object.log(error_file,"Failed to run the runner script " + str(e))
        raise e



if __name__=="__main__":
    # modelname = sys.argv[0]
    # filepath = sys.argv[1]
    # modelname = str(modelname)
    # filepath = str(filepath)
    modelname = str(input("model name : "))
    filepath = str(input("csv file name : "))
    
    run(filepath,modelname)


