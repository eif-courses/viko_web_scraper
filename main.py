import pandas as pd
import lxml.html as LH
import requests
import requests
from lxml import html

def read_teacher_data_from_viko(urls):
    for i in range(len(urls)):
        data = pd.read_html(urls[i])
        data[0].to_csv('destytojai.csv', header=0, index=False, encoding='UTF-8', mode='a')
        print ('Destytoju duomenys atnaujinti:', urls[i])

def read_teacher_data_image_urls_from_viko(urls):
    for i in range(len(urls)):
        pageContent = requests.get(urls[i])
        tree = html.fromstring(pageContent.content)
        photosUrl = tree.xpath('//td/a[1]/@href')
        photosUrl.pop()
        photosUrl.pop()
        print('\n', photosUrl[i])


if __name__ == '__main__':
    domain = 'https://eif.viko.lt/fakultetas/katedros/'
    urls = [domain+"programines-irangos-katedra/programines-irangos-katedros-destytojai/",
            domain+"elektronikos-katedra/elektronikos-katedros-destytojai/",
            domain+"kompiuteriu-technikos-ir-telekomunikaciju-katedra/kompiuteriu-sistemu-ir-telekomunikaciju-katedros-destytojai/",
            domain+"informaciniu-sistemu-katedra/informaciniu-sistemu-katedros-destytojai/"]
    pd.set_option('display.max_colwidth', 500)
    open('destytojai.csv', 'w').close() #pasalinti failo duomenis
    read_teacher_data_from_viko(urls)

    for line in open('destytojai.csv'):
        listWords = line.split(" ")
        if listWords[0].lower() == "dr." or listWords[0] == '"Dr.' or listWords[0] == "dr. ":
            print(listWords[0] + ' ' + listWords[1] + ' ' + listWords[2])
        else:
            print(listWords[0] + ' ' + listWords[1])
    # read_teacher_data_image_urls_from_viko(urls)



