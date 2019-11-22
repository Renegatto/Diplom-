import requests

def data_money():
    url = 'http://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
    m = requests.get(url).json()
    return m