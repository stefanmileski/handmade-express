from ShopApp.models import Review


def get_average_rating(items):
    for item in items:
        reviews = Review.objects.filter(product=item)
        total_ratings = sum(review.rating for review in reviews)
        average_rating = total_ratings / len(reviews) if len(reviews) > 0 else 0
        item.average_rating = average_rating

    return items
