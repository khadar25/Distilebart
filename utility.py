from summarizer import Summarizer
import textwrap
import os
import pandas as pd

class TextSumarization():
    def Summarizer(articles,model='distilbert-base-uncased'):
        try:
            model = Summarizer(model) # @param:distilbert
            summary_ls=[]
            for article in articles:
                output_text = model(article,min_length=60)
                summary_text = ''.join(output_text)
                summary_ls.append(summary_text)
                #wrapper = textwrap.TextWrapper(width=80)
                #print(wrapper.fill(summary_text))
            return summary_ls
        except Exception as e:
            raise RuntimeError("Invalid path specified :",e, exc_info=True)


    def article_preprocessor(filepath):
        file_types=('csv','json','txt')
        try:
            file_ext  = os.path.split(filepath)[-1].split(".")[-1]
            if file_ext in file_types:
                if file_ext == "csv":
                   news_df= pd.read_csv(filepath)
                   articles = list(news_df.Description)
                   type(articles)
                   return articles
                elif file_ext == "json":
                    news_df = pd.read_json(filepath)
                    articles = news_df.Description
                    return articles
                elif file_ext == "txt":
                    articles = open(filepath,'r')
                    return articles

            else:
                raise RuntimeError("Invalid Exe:", exc_info=True)

        except Exception as e:
            raise RuntimeError("Invalid path specified :",e, exc_info=True)

    def model_selection(model):
        models =['bert-base-uncased','xlnet-base-cased','distilbert-base-uncased','albert-base-v1']
        if model in models:
            return True
        else:
            raise RuntimeError("Select models only in this {} model list".format(models))
