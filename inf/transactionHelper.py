from .transactionDataClient import *


'''
Retrieve all the bias subtext (the word, and its respective bias reasoning), relating to an Article URL

Returns:
-------
    list(dict()): list of dictionaries from the Article_ArticleBias table, filtered by the Article URL.
    Each dictionary is a separate record in the database
    
    Returns None if the URL cannot be found, or there are no records relating to the URL.

'''
def retrieve_bias_keywords_by_url(tdc:transactionDataClient, url=str):
    related_article = tdc.query('Article', f"URL = '{url}' ORDER BY ID DESC")
    
    if len(related_article) == 0 or related_article is None:
        return None
    # URL should be unqiue, but this isn't enforced.
    if len(related_article) > 1:
        tdc.logMessage(messageStatus.WARN, 'There is more than one Article URL in the database. The first tuple in query is selected.')
    
    biasSubText = tdc.query('Article_ArticleBias', f'ID_Article = {related_article[0]["ID"]}')
    if len(biasSubText) == 0 or biasSubText is None:
        tdc.logMessage(messageStatus.WARN, f'There are not Bias subtext records for the related ArticleID ({related_article[0]["ID"]})')
        return None 
    
    return biasSubText

'''
Retrieve all the bias subtext (the word, and its respective bias reasoning), relating to an Article ID

Returns:
-------
    list(dict): list of dictionaries from the Article_ArticleBias table, filtered by the Article ID.
    Each dictionary is a separate record in the database.
    
    Returns None if the ID cannot be found, or there are no records relating to the ID

'''
def retrieve_bias_keywords_by_key(tdc=transactionDataClient, ID=int):
    biasSubText = tdc.query('Article_ArticleBias', f'ID_Article = {ID}')
    if len(biasSubText) == 0 or biasSubText is None:
        tdc.logMessage(messageStatus.WARN, f'There are not Bias subtext records for the related ArticleID ({ID})')
        return None 
    return biasSubText

'''
Inserts all the bias subtext into the related Article_ArticleBias
'''
def insert_bias_keywords(tdc=transactionDataClient, ID=int, keywords=dict()) -> None:
    pass

'''
Find all articles related to a Politician. Requires the ID of the Politician.
'''
def find_related_articles(tdc=transactionDataClient, ID_politician=int):
    query = f"""
    SELECT A.*
    FROM Article A
    INNER JOIN Politician_KeyTable PK ON PK.ID_Article = A.ID
    WHERE ID_Politician = {ID_politician} 
    """
    return tdc.query_special(query)
    
'''
Inserts all the bias subtext into the related Article_ArticleBias.
Expects the input to be a key-value pair with the biased phrase as the key, and the reasoning of the biased phrase as
its respective value. E.g.

    {
        'Devastating blaze': 'the term "devastating" indicates a tragice loss of life',
        'Terror Attack': 'The term "terror" is frightening and is used to emote panic'
    }

'''
def insert_bias_keywords(tdc=transactionDataClient, ID=int, biasSubtext=dict, inProduction=bool) -> None:
    for phrase, reason in biasSubtext.items():
        subTextClass = Article_ArticleBias(ID, phrase, reason, inProduction)
        tdc.insert(subTextClass)


'''
retrieves all comments relating to an article ID
'''
def retrieve_article_comments(tdc:transactionDataClient, ID_article:int) -> list:
    return tdc.query('Comments', f'ID_Article = {ID_article}')

'''
Persist a comment to the database.
'''
def create_comment(tdc:transactionDataClient, author:str, message:str, ID_Article:str):
    comment = Comments(ID_Article, author, message, 1)
    tdc.insert(comment)


'''
Increments the vote
'''
def increment_vote(tdc=transactionDataClient, ID=int, option=int):
    records = tdc.query('Polling', f'ID_Article = {ID}')
    record = records[0]

    if (option == 1):
        record.votesFirst += 1
    elif (option == 2):
        record.votesSecond += 1
    elif (option == 3):
        record.votesThird += 1
    elif (option == 4):
        record.votesFourth += 1
    else:            
        tdc.logMessage(messageStatus.WARN, f'This is not a valid vote option for related ArticleID ({ID})')

