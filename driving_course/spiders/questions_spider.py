import scrapy
import json
import csv


class QuestionsSpider(scrapy.Spider):
    name = "questions"

    def start_requests(self):
        with open('questions_eng.csv', 'w') as outcsveng:
            writer = csv.DictWriter(
                outcsveng, fieldnames=['bonneReponseId', 'bonneReponseExplication',
                                       'uid', 'sys_language_uid', 'l10n_parent',
                                       'code', 'question', 'choix_reponse', 'image'])
            writer.writeheader()
        with open('questions_fr.csv', 'w') as outcsvfr:
            writer = csv.DictWriter(
                outcsvfr, fieldnames=["bonneReponseId", "bonneReponseExplication",
                                      "uid", "sys_language_uid", "l10n_parent",
                                      "code", "question", "choix_reponse", "image"])
            writer.writeheader()
        urls = [
            'https://saaq.gouv.qc.ca/fileadmin/application_testdeconnaissances/json/reponses/2575.json',
            'https://saaq.gouv.qc.ca/fileadmin/application_testdeconnaissances/json/questions/1000.json',
            'https://saaq.gouv.qc.ca/fileadmin/application_testdeconnaissances/json/questions/1.json',
        ]
        i = 1
        while i < 3000:
            url = 'https://saaq.gouv.qc.ca/fileadmin/application_testdeconnaissances/json/questions/' + \
                str(i) + '.json'
            i += 1
            yield scrapy.Request(url=url, callback=self.parse)
            #request.meta['proxy'] = "proxy.sld.cu:3128"
            # yield request

    def parse(self, response):
        print(response.url)
        if response.status == 404:
            print('Funciona')
        else:
            url = response.url
            key = ""
            for i in url[-6:0:-1]:
                if i != "/":
                    key += i
                else:
                    break
            key = key[::-1]
            json_data = json.loads(response.body)
            french_data = json_data[key][0]
            english_data = json_data[key][1]
            fields = ['bonneReponseId', 'bonneReponseExplication',
                      'uid', 'sys_language_uid', 'l10n_parent',
                      'code', 'question', 'choix_reponse', 'image']
            try:
                with open("questions_eng.csv", "a") as eng:
                    with open("questions_fr.csv", "a") as fr:
                        writer_eng = csv.DictWriter(eng, fieldnames=fields)
                        writer_fr = csv.DictWriter(fr, fieldnames=fields)
                        row_eng, row_fr = {}, {}
                        for field in fields:
                            row_eng[field] = english_data[field]
                            row_fr[field] = french_data[field]
                        writer_eng.writerow(row_eng)
                        writer_fr.writerow(row_fr)
            except:
                print("ERROR EN EL JSON CON ID: " + key)

    def error_handler(self, response):
        print("Tu no eres yegua de aqui")
