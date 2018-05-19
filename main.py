import pandas as pd
import requests
import re
from lxml import html

def save_from_viko_to_csv(urls):
    for k in range(len(urls)):
        data = pd.read_html(urls[k])
        data[0].to_csv('destytojai.csv', header=0, index=False, encoding='UTF-8', mode='a')
        print ('Destytoju duomenys atnaujinti:', urls[k])


def read_teacher_data_image_urls_from_viko(url):
    pageContent = requests.get(url)
    tree = html.fromstring(pageContent.content)
    photosUrl = tree.xpath('//td/a[1]/@href')
    photosUrl.pop()
    photosUrl.pop()
    return photosUrl

def read_viko_contacts_paga(url):
    teacher_logo = '<img src="https://i1.wp.com/eif.viko.lt/media/uploads/sites/5/2018/04/no_photo.png?fit=150%2C150&ssl=1" align="left" height="400px">'
    teacher_div_ul = '<div class="element-item transition metal" data-category="transition">'
    teacher_div_ul_close = '</ul></div>'
    teacher_li = '<li class="list-group-item">'
    p = requests.get(url)
    tree = html.fromstring(p.content)
    pareigos = tree.xpath('//p/strong[1]/text()')
    vardas = tree.xpath('//p/strong[2]/text()')
    telefonas = tree.xpath('//p/strong[3]/following::text()[1]')
    kab_nr = tree.xpath('//p/strong[5]/following::text()[1]')
    for i in range(len(pareigos)):
        print(teacher_div_ul + teacher_logo + '<ul  class="list-group">')
        print(teacher_li + vardas[i] + ' ,pareigos:' + pareigos[i] + '</li>')
        print(teacher_li + 'Tel.' + telefonas[i] + '</li>')
        print(teacher_li + kab_nr[i] +' kab.' + '</li>')
        print(teacher_div_ul_close)
        #print(address[i] + vardas[i])


if __name__ == '__main__':

    #read_viko_contacts_paga('https://eif.viko.lt/kontaktai/')

    domain = 'https://eif.viko.lt/fakultetas/katedros/'
    viko_urls = [domain + "programines-irangos-katedra/programines-irangos-katedros-destytojai/",
                 domain + "elektronikos-katedra/elektronikos-katedros-destytojai/",
                 domain + "kompiuteriu-technikos-ir-telekomunikaciju-katedra/kompiuteriu-sistemu-ir-telekomunikaciju-katedros-destytojai/",
                 domain + "informaciniu-sistemu-katedra/informaciniu-sistemu-katedros-destytojai/"]
    pd.set_option('display.max_colwidth', 500)

    teacher_img_src = []
    for i in range(len(viko_urls)):
        for j in range(len(read_teacher_data_image_urls_from_viko(viko_urls[i]))):
            teacher_img_src.append(read_teacher_data_image_urls_from_viko(viko_urls[i])[j])
    print(teacher_img_src)
    open('destytojai.csv', 'w').close() #pasalinti failo duomenis
    save_from_viko_to_csv(viko_urls)

    index = 0
    teacher_logo = '<img src="https://i1.wp.com/eif.viko.lt/media/uploads/sites/5/2018/04/no_photo.png?fit=150%2C150&ssl=1" align="left" height="400px">'
    teacher_div_ul = '<div class="element-item transition metal" data-category="transition">'
    teacher_div_ul_close = '</ul></div>'
    teacher_li = '<li class="list-group-item">'

    # print(test)
    # str(teacher_img_src[index]).replace("mailto:")

    for line in open('destytojai.csv'):
        if index < len(teacher_img_src):
            listWords = line.split(" ")
            konsultacijos = line.split(",")[1]
            if index == 49:
                teacher_img_src.insert(index, 'https://i1.wp.com/eif.viko.lt/media/uploads/sites/5/2018/04/no_photo.png?fit=150%2C150&amp;ssl=1')
                teacher_img_src[index] = re.sub(r'^mailto:([a-zA-Z0-9._@]*)',
                                                'https://i1.wp.com/eif.viko.lt/media/uploads/sites/5/2018/04/no_photo.png?fit=150%2C150&amp;ssl=1',
                                                teacher_img_src[index])
            else:
                teacher_img_src[index] = re.sub(r'^mailto:([a-zA-Z0-9._@]*)',
                                            'https://i1.wp.com/eif.viko.lt/media/uploads/sites/5/2018/04/no_photo.png?fit=150%2C150&amp;ssl=1',
                                            teacher_img_src[index])
            if listWords[0].lower() == "dr." or listWords[0] == '"Dr.' or listWords[0] == "dr. ":
                print(teacher_div_ul + ' <img src="' + teacher_img_src[
                    index] + '" align="left" height="400px">' + '<ul class="list-group">')
                print(teacher_li + listWords[0] + ' ' + listWords[1] + ' ' + listWords[2] + '</li>')
                print(teacher_li + listWords[3] + ' ' + listWords[4] + '</li>')
                print(teacher_li + konsultacijos + '</li>')
                print(teacher_div_ul_close)
            else:
                print(teacher_div_ul + ' <img src="' + teacher_img_src[
                    index] + '" align="left" height="400px">' + '<ul  class="list-group">')
                print(teacher_li + listWords[0] + ' ' + listWords[1] + '</li>')
                if index == 49:
                    print(teacher_li + 'Dabar:' + ' ' + 'Atostogos' + '</li>')
                else:
                    print(teacher_li + listWords[2] + ' ' + listWords[3] + '</li>')

                print(teacher_li + konsultacijos + '</li>')
                print(teacher_div_ul_close)
        index += 1
