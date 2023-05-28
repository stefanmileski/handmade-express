from django import template

register = template.Library()


@register.filter
def calculate_average_rating(reviews):
    total_ratings = sum(review.rating for review in reviews)
    average_rating = total_ratings / len(reviews) if len(reviews) > 0 else 0
    return average_rating
