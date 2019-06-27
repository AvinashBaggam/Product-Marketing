import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from sklearn.feature_extraction import text
from random import sample


PG_STOP_WORDS = ["great", "good", "bad", "awful", "excellent", "terrible",
                 "amazing", "worst", "perfect", "horrible", "best"]


def get_keywords_from_naive_bayes(product, new_stop_words, validation=False):
    

    
    labels = []

    
    reviews = []

    for rev in product.reviews:
        

        if rev.score < 3:
            labels.append("negative")
            reviews.append(rev.review)

        elif rev.score > 3:
            labels.append("positive")
            reviews.append(rev.review)

    
    new_stop_words.extend(PG_STOP_WORDS)
    stop_words = text.ENGLISH_STOP_WORDS.union(new_stop_words)

    
    vectorizer = CountVectorizer(stop_words=stop_words)

    
    X = vectorizer.fit_transform(reviews)
    y = np.array(labels)

    
    nb = MultinomialNB()
    nb.fit(X, y)

    
    pos_probs = nb.feature_log_prob_[1] - nb.feature_log_prob_[0]

    
    neg_probs = nb.feature_log_prob_[0] - nb.feature_log_prob_[1]

    
    features = vectorizer.get_feature_names()

    
    pos_probs_and_words = sorted(zip(pos_probs, features), reverse=True)[:10]
    neg_probs_and_words = sorted(zip(neg_probs, features), reverse=True)[:10]

    pos_words = [tup[1] for tup in pos_probs_and_words]
    neg_words = [tup[1] for tup in neg_probs_and_words]

    if validation:
        
        precision, recall = cross_validate(nb, X, y)
        return (precision, recall)

    else:

        return (pos_words, neg_words)


def cross_validate(nb, X, y):
    

    
    skf = StratifiedKFold(n_splits=5)

    
    cm = np.zeros((2, 2))

    precision = []
    recall = []

    for train, test in skf.split(X, y):
        
        X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]

        
        nb.fit(X_train, y_train)

        
        y_hat = nb.predict(X_test)

        
        cm += confusion_matrix(y_test, y_hat, labels=['positive', 'negative'])

        
        p, r, fscore, support = precision_recall_fscore_support(y_test, y_hat)
        if len(p) > 1:
            precision.append(p[1])
            recall.append(r[1])

        avg_precision = sum(precision)/float(len(precision))
        avg_recall = sum(recall)/float(len(recall))

    return (avg_precision, avg_recall)



if __name__ == "__main__":

    

    from model import Product, connect_to_db
    from server import app

   
    connect_to_db(app)

    
    products = Product.query.filter(Product.n_scores > 20).all()

    print len(products)

    
    validation_set = sample(range(0, len(products) - 1), 50)

    
    precision = []
    recall = []

    for idx in validation_set:
        product = products[idx]

        print "Validating product"

        
        more_stop_words = product.title.split(' ')
        more_stop_words = [w.lower() for w in more_stop_words]

        p, r = get_keywords_from_naive_bayes(product,
                                             more_stop_words,
                                             True)
        precision.append(p)
        recall.append(r)

    print precision
    print "Average precision over 200 products is: {}".format(
        sum(precision)/float(len(precision)))

    print recall
    print "Average recall over 200 products is: {}".format(
        sum(recall)/float(len(recall)))
