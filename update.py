import requests
import json
import os
from datetime import date
import time
import shutil
from collections import OrderedDict 

from bs4 import BeautifulSoup
from unidecode import unidecode
import Levenshtein
import pymongo

url = 'http://apl.utfpr.edu.br/extensao/certificados/listaPublica/'
url_search = 'http://apl.utfpr.edu.br/extensao/certificados/listaCertificadosPublicos/'



def update_db():
    #   CT -> 1   AP -> 2    CM -> 3    DV -> 4    FB -> 5    GP -> 6   LD -> 7
    #   MD -> 8   PB -> 9    PG -> 10   SH -> 11   TD -> 12   CP -> 13
    campus_code = '13'

    year = str(date.today().year)

    events = []
    owners = []

    events = find_only_events(campus_code, year)
    events = get_qty_certs(events)
    events = events_diff(events, year)

# Find only the events, not the certificates
# Only one campus and one year by time
def find_only_events(campus_code, year):
    events = []

    results_raw = requests.post(url, data = {'txtCampus': campus_code, 'txtAno': year}).text

    results = BeautifulSoup(results_raw, 'html.parser')

    campus_name = results.find(attrs={'name': 'txtCampus'}).find(attrs={'selected': True}).get_text()

    for one_event in results.find(attrs={"name": "txtEvento"}).find_all('option'):
        if one_event['value'] != '':
            events.append({
                'name': one_event.get_text(),
                'name_search': unidecode(one_event.get_text().upper()),
                'code': one_event['value'],
                'year': year,
                'campus': {'code': campus_code, 'name': campus_name},
                'qty_certs': 0,
                'certs': []
            })

    return events

def get_qty_certs(events):

    for one_event in events:
        url_id = 0
        count_certs = 0

        aux_event = one_event

        while True:

            results_raw = requests.post(url_search + str(url_id), data = {'txtEvento': one_event['code']}).text

            results = BeautifulSoup(results_raw, 'html.parser')

            all_tr = results.find(id='data_table').find_all('tr', id = True)

            if len(all_tr) == 0:
                break

            count_certs += len(all_tr)

            url_id += 15

        one_event['qty_certs'] = count_certs

    return events

def events_diff(events, year):

    events_old = json.loads(open('data/test/events.json').read())
    events_old = [one_event for one_event in events_old if one_event['year'] == year]
    
    events_diff = []

    for one_event in events:
        one_event_old = next((one_event_old for one_event_old in events_old if one_event_old['code'] == one_event['code']), None)

        if one_event_old != None:
            if one_event_old['qty_certs'] != one_event['qty_certs']:
                print(f'Name: {one_event_old["name"]}')
                print(f'Old Qty: {one_event_old["qty_certs"]} - New Qty: {one_event["qty_certs"]}\n\n')
                events_diff.append(one_event_old)
                
        else:
            print(f'Name: {one_event["name"]} - Qty: {one_event["qty_certs"]}')
            events_diff.append(one_event)

    return events_diff



def main1():

    """ 
    init_all

    update_one_year -> Every Day
    - campus_codes
    - year

    update_all_years -> Every Week
    - campus_codes

    verify_one_year -> Every Month
    - campus_codes
    - year

    verify_all_years -> Every trimester
    - campus_codes

    """
    option = 'update'

    if option == 'init':
        init_db()

    elif option == 'update':
        update_db()

############################################################
############################################################
############################################################
############################################################

if __name__ == '__main__':
    main()