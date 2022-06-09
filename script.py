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

###############################################
################## Init #######################
###############################################

def init_db():
    #   CT -> 1   AP -> 2    CM -> 3    DV -> 4    FB -> 5    GP -> 6   LD -> 7
    #   MD -> 8   PB -> 9    PG -> 10   SH -> 11   TD -> 12   CP -> 13
    campus = '13'

    #   2013 -> 2014 -> 2015 -> 2016 -> 2017 -> 2018 -> 2019 -> 2020 -> 2021 -> 2022
    year = '2018'

    events = []
    owners = []

    events = find_events_year(campus, url, year)
    events, owners = find_owners(events, url_search)
    save_json(events, owners, year)

def find_events_all(campus_, url_):
    events_ = []

    results_raw = requests.post(url_, data = {'txtCampus': campus_}).text

    results = BeautifulSoup(results_raw, 'html.parser')

    campus_name = results.find(attrs={'name': 'txtCampus'}).find(attrs={'selected': True}).get_text()

    for one_year in results.find(attrs={"name": "txtAno"}).find_all('option'):

        if one_year['value'] != '':
            result_one_year_raw = requests.post(url_, data = {'txtCampus': campus_, 'txtAno': one_year['value']}).text

            result_one_year = BeautifulSoup(result_one_year_raw, 'html.parser')

            for one_event in result_one_year.find(attrs={"name": "txtEvento"}).find_all('option'):
                if one_event['value'] != '':
                    events_.append({
                        'name': one_event.get_text(),
                        'name_search': unidecode(one_event.get_text().upper()),
                        'code': one_event['value'],
                        'year': one_year['value'],
                        'campus': {'code': campus_, 'name': campus_name},
                        'qty_certs': 0,
                        'certs': []
                    })

    return events_

def find_events_year(campus_, url_, year_):
    events_ = []

    results_raw = requests.post(url_, data = {'txtCampus': campus_, 'txtAno': year_}).text

    results = BeautifulSoup(results_raw, 'html.parser')

    campus_name = results.find(attrs={'name': 'txtCampus'}).find(attrs={'selected': True}).get_text()

    for one_event in results.find(attrs={"name": "txtEvento"}).find_all('option'):
        if one_event['value'] != '':
            events_.append({
                'name': one_event.get_text(),
                'name_search': unidecode(one_event.get_text().upper()),
                'code': one_event['value'],
                'year': year_,
                'campus': {'code': campus_, 'name': campus_name},
                'qty_certs': 0,
                'certs': []
            })

    return events_

def find_owners(events_, url_search_):
    owners_ = {}
    new_events = []

    for one_event in events_:
        url_id = 0

        aux_event = one_event

        while True:

            results_raw = requests.post(url_search_ + str(url_id), data = {'txtEvento': one_event['code']}).text

            results = BeautifulSoup(results_raw, 'html.parser')

            all_tr = results.find(id='data_table').find_all('tr', id = True)

            if len(all_tr) > 0:  

                for row in all_tr:

                    try:
                        one_person = row.find_all('td')

                        aux_name = unidecode(one_person[0].get_text().upper())
                        aux_name = aux_name.rstrip('*.- \'" ')
                        aux_name = aux_name.lstrip('*.- \'" ')

                        aux_code = one_person[2].a.get('href').split('validar/')[1]
                        
                        while True:
                            if aux_name.find('  ') != -1:
                                aux_name = aux_name.replace('  ', ' ')
                            else:
                                break

                        aux_event['certs'].append({
                            'code': aux_code,
                            'owner': aux_name
                        })

                        if aux_name in owners_:

                            owners_[aux_name]['certs'].append({
                                'code': aux_code,
                                'year': one_event['year'],
                                'event_code': one_event['code'],
                                'event_name': one_event['name']
                            })

                        else:
                            owners_[aux_name] = {
                                'name': aux_name,
                                'certs': [{
                                    'code': aux_code,
                                    'year': one_event['year'],
                                    'event_code': one_event['code'],
                                    'event_name': one_event['name']
                                }]
                            }
                    
                    except:
                        print('error')

                url_id += 15

            else:
                break

        aux_event['qty_certs'] = len(aux_event['certs'])

        new_events.append(aux_event)

    return new_events, owners_

def save_json(events_, owners_, year_ = ''):

    path = 'new_output'

    try:
        os.mkdir(path)
    except:
        #shutil.rmtree(path)
        #os.mkdir(path)
        print('\a')

    open(path + '/events_' + year_ +'.json', 'wt').write(json.dumps(events_))
    open(path + '/owners_ ' + year_ + '.json', 'wt').write(json.dumps(owners_))


###############################################
################# Update ######################
###############################################


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