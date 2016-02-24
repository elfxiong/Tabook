import json
from django.http import JsonResponse

def get_restaurnt(request):
    pass

def get_customer(request):
    pass

def get_table_status(request):
    pass


#search by location, price, category, restaurant name
def search_restaurant(request):

    pass


#generate recommendations nearby you
def get_recommendations(request):
    pass


#get all tables by restaurant, date, time
def get_all_tables(request):
    pass


def get_current_date(request):
    pass


def get_reviews(request):
    pass


#get details (for the mouseover pop-up)
def get_table_details(request):
    pass


#might not need this one for project 3
def get_shopping_cart(request):
    pass


#might not need this one for project 3
#logged in or not; customer or restaurant
def get_user_status(request):
    pass



#might not need this one for project 3
def get_background_image(request):
    pass

#sort the search results by user's pref (distance, price etc), into a specific order
#might not need this one for project 3
def sort_by_preference(request):
    pass


