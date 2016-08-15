import requests

NOMINATIM_URL = 'http://nominatim.openstreetmap.org/'
REVERSE_NOMINATIM_URL = '{}reverse'.format(NOMINATIM_URL)


def query_nominatim(query):
    try:
        data = requests.get(NOMINATIM_URL, {'q': query, 'addressdetails': '1', 'format': 'json', 'limit': '1'}).json()
    except Exception:
        raise ValueError
    if not len(data) or not data[0]['address']:
        raise ValueError
    return data[0]


def reverse_nominatim(lat, lon):
    try:
        data = requests.get(REVERSE_NOMINATIM_URL, {'lat': lat, 'lon': lon, 'format': 'json'}).json()
        return data['address']
    except KeyError:
        raise ValueError
