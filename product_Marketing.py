from model import User
from model import connect_to_db, db
import json


def get_chart_data(score_list):
    

    data_dict = {
        "labels": ["1", "2", "3", "4", "5"],
        "datasets": [{
            "label": "Buyer Ratings",
            "data": score_list,
            "backgroundColor": 'rgba(96, 4, 122, 0.6)',
            "hoverBackgroundColor": 'rgba(96, 4, 122, 1)',
            "borderWidth": 5
        }]
    }

    return data_dict

def format_reviews_to_dicts(reviews, user_id):
    
    favorite_review_ids = set()

    if user_id:
        user = User.query.get(user_id)
        favorite_review_ids = user.get_favorite_review_ids()

    rev_dict_list = []

    for review_id, review, asin, score, summary, time, _, _ in reviews:
        rev_dict = {}
        rev_dict["review_id"] = review_id
        rev_dict["review"] = review
        rev_dict["summary"] = summary
        rev_dict["score"] = score
        rev_dict["time"] = time
        rev_dict["user"] = user_id       
        rev_dict["favorite"] = review_id in favorite_review_ids   
        rev_dict_list.append(rev_dict)

    return rev_dict_list
