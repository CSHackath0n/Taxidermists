import requests

def download_articles(url):
    r = requests.get(url)
    return r.text

def parse_article(article_txt, line_sep):
    parts = article_txt.strip().split(line_sep)
    article_dict = {
        part.split(':',1)[0].replace('####','').strip(): part.split(':',1)[1].strip()
        for part in parts
    }
    return format_article_dict(article_dict)

def format_article_dict(article_dict):
    article_dict['seqNo'] = int(article_dict['seqNo'])
    article_dict['topics'] = [
        t.strip()
        for t in article_dict['topics'].replace('"','').split(',')
    ]
    article_dict['topicsDescription'] = [
        t.strip()
        for t in article_dict['topicsDescription'].replace('"','').split(',')
    ]
    return article_dict

def parse_articles(articles_txt, line_sep):
    articles_txt_list = articles_txt.split(line_sep + line_sep)
    articles_dict_list = [
        parse_article(article_txt, line_sep=line_sep)
        for article_txt in articles_txt_list
    ]
    return articles_dict_list

def parse_articles_from_url(url, line_sep='\r\n'):
    articles_txt = download_articles(url)
    return parse_articles(articles_txt, line_sep)

def parse_articles_from_file(file_path, line_sep='\n'):
    with open(file_path, 'r') as f:
        articles_txt = f.read()
    return parse_articles(articles_txt, line_sep)


print(parse_articles_from_file('Data/News300.txt'))
# print(parse_articles_from_url('https://hackathon17.mope.ml/HackathonSite/News300.txt'))
