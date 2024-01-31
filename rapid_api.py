import requests
from decouple import config
from random import choices

from classes import User

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': config('rapid_api')
}


def get_destination_id(city: str) -> str:
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city, "locale": "ru_RU", "currency": "RUB"}
    return requests.get(
        url, headers=headers, params=querystring).json()['suggestions'][0]['entities'][0]['destinationId']


def get_hotels(user_obj: User) -> list:
    url = "https://hotels4.p.rapidapi.com/properties/list"
    hotels_lst = requests.get(
        url, headers=headers, params=set_querystring(user_obj)).json()['data']['body']['searchResults']['results']
    result = list()
    for i_hotel in hotels_lst:
        hotel = dict()
        hotel['name'] = i_hotel['name']
        hotel['address'] = f"{i_hotel['address']['locality']}, " \
                           f"{i_hotel['address'].get('streetAddress')} {i_hotel['address'].get('extendedAddress')}"
        hotel['price'] = i_hotel['ratePlan']['price']['current']
        hotel['total_price'] = i_hotel['ratePlan']['price'].get('fullyBundledPricePerStay')
        hotel_id = i_hotel['id']
        hotel['url'] = f'https://hotels.com/ho{hotel_id}?q-check-in={user_obj.settings.check_in}' \
                       f'&q-check-out={user_obj.settings.check_out}' \
                       f'&q-rooms=1&q-room-0-adults=1&q-room-0-children=0'
        if user_obj.answers.get('load_pictures'):
            hotel['images'] = get_images_by_hotel_id(hotel_id, user_obj.answers['number_of_pictures'])
        if user_obj.answers['sort_by'] == 'DISTANCE_FROM_LANDMARK':
            if str_to_float(i_hotel['landmarks'][0]['distance'].split()[0]) \
                    > str_to_float(user_obj.answers['max_distance']):
                continue
        result.append(hotel)
    return result


def str_to_float(string: str) -> float:
    return float(string.replace(',', '.'))


def get_images_by_hotel_id(hotel_id: str, img_count: str) -> list:
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    req = requests.get(url, headers=headers, params={'id': hotel_id}).json()['hotelImages'][:]
    rand_photos = choices(req, k=int(img_count))
    return [i_img['baseUrl'].replace('{size}', 'w') for i_img in rand_photos]


def set_querystring(user_obj: User) -> dict:
    destination_id = get_destination_id(user_obj.answers['city'])
    querystring = {
        "destinationId": destination_id,
        "pageNumber": "1",
        "pageSize": user_obj.answers['number_of_hotels'],
        "checkIn": user_obj.settings.check_in,
        "checkOut": user_obj.settings.check_out,
        "adults1": "1",
        "sortOrder": user_obj.answers['sort_by'],
        "locale": "ru_RU",
        "currency": "RUB"
    }
    if user_obj.answers['sort_by'] == 'DISTANCE_FROM_LANDMARK':
        querystring.update(
            {
                "priceMin": user_obj.answers['price_min'],
                "priceMax": user_obj.answers['price_max'],
                "sortLid": destination_id
            }
        )
    return querystring
