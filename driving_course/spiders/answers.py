import scrapy
import csv
from ast import literal_eval
import json


class AnswersSpider(scrapy.Spider):
    name = "answers"

    def start_requests(self):
        with open('answers.csv', 'w') as outcsv:
            writer = csv.DictWriter(
                outcsv, fieldnames=['uid', 'type',
                                    'texte', 'explication', 'bonne_reponse',
                                    'image', 'sys_language_uid', 'l10n_parent', ])
            writer.writeheader()
        with open('questions_eng.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                responses = literal_eval(row["choix_reponse"])
                for response in responses:
                    url = "https://saaq.gouv.qc.ca/fileadmin/application_testdeconnaissances/json/reponses/" + \
                        str(response) + ".json"
                    yield scrapy.Request(url=url, callback=self.parse)
        with open('questions_fr.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                responses = literal_eval(row["choix_reponse"])
                for response in responses:
                    url = "https://saaq.gouv.qc.ca/fileadmin/application_testdeconnaissances/json/reponses/" + \
                        str(response) + ".json"
                    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.url)
        if response.status == 404:
            print('Funciona')
        else:
            json_data = json.loads(response.body)
            fields = ['uid', 'type',
                      'texte', 'explication', 'bonne_reponse',
                      'image', 'sys_language_uid', 'l10n_parent', ]
            try:
                with open("answers.csv", "a") as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    row = {}
                    for field in fields:
                        row[field] = json_data[field]
                    writer.writerow(row)
            except:
                print("ERROR EN EL JSON CON ID: " + json_data["uid"])
