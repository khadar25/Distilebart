import pandas as pd
from utility import TextSumarization
import argparse
import logging
import time

#logging.basicConfig(filename='TEXT_Summary_Failure.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger1 = logging.getLogger('1')
logger1.addHandler(logging.FileHandler('logger1'))
logger2 = logging.getLogger('2')
logger2.addHandler(logging.FileHandler('logger2'))
def run():
    parser = argparse.ArgumentParser(description='Process and summarize lectures')
    parser.add_argument('-path', dest='path', default='Final_news.csv', help='File path')
    parser.add_argument('-model', dest='model', default='albert-base-v1', help='')
    args = parser.parse_args()
    try:
        if not args.path:
            raise RuntimeError("Must supply text path.")
    except Exception as e:
        logger1.error("Invaild path specified :",e, exc_info=True)

    articles =TextSumarization.article_preprocessor(args.path)
    try:
        summaried_text = TextSumarization.Summarizer(articles,model=args.model)
        summary_df = pd.DataFrame({"Before Summarization":articles,"After Summarization":summaried_text})
        #print("successfully written csv file ")
        summary_df.to_csv('Summary{}_.csv'.format(args.model),index=False)
    except Exception as e:
        logger1.error("Text model Exception occured :",e, exc_info=True)
    return args.model
if __name__ == '__main__':
    start = time.process_time()
    run()
    end_time =time.process_time() - start
    logger2.warning("Successfully summarized the text & Exist the flow of the code with Time:{} in seconds".format(end_time))

