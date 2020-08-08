import pandas as pd
from utility import TextSumarization
import argparse
from application_logging.logger import App_Logger
import time

logger_object = App_Logger()
general_logs = open("Logs/generallogs.txt",'+a')
success_file = open("Logs/successlogs.txt",'+a')
error_file = open("Logs/errorlogs.txt",'+a')


def run():
    parser = argparse.ArgumentParser(description='Summarization of TextData using pretrained models')
    parser.add_argument('-path', dest='path', default='Final_news.csv', help='File path')
    parser.add_argument('-model', dest='model', default='bert-base-uncased', help='[xlnet-base-cased,distilbert-base-uncased,albert-base-v1]')
    args = parser.parse_args()
    try:
        logger_object.log(general_logs,"Entered the runner file --> Running the script now !")
        if not args.path:
            raise RuntimeError("Must supply text path.")
        logger_object.log(general_logs,"Validation of the model is in Process !")
        TextSumarization.model_selection(args.model)
        articles =TextSumarization.article_preprocessor(args.path)
        try:
            summaried_text = TextSumarization.Summarizer(articles,model=args.model)
            summary_df = pd.DataFrame({"Before Summarization":articles,"After Summarization":summaried_text})
            summary_df.to_csv('Summary_{}.csv'.format(args.model),index=False)
        except Exception as e:
            logger_object.log(error_file,"Failed to write summaries to a text file " + str(e))
        return args.model
    except Exception as e:
        logger_object.log(error_file,"Failed to run the runner script " + str(e))
        return False

if __name__ == '__main__':
    start = time.process_time()
    model = run()
    if model == False:
       logger_object.log(general_logs,"Flow Exist abnormally please look errorlogs for more info !")
    else:
        end_time =time.process_time() - start
        logger_object.log(general_logs,"Process completed Successfully !")
        logger_object.log(success_file,"Successfully summarized the text & Exist the flow of the code with Time:{} in seconds using {} model".format(end_time,model))





