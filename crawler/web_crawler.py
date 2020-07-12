from bs4 import BeautifulSoup
import urllib.request
import ssl
import requests
import json
import csv

context = ssl._create_unverified_context()


def get_new_feed():
    url = 'https://ncov.moh.gov.vn/web/guest/trang-chu'
    # page = urllib.request.urlopen(url, context=context)
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')
    new_feed = soup.find(class_='journal-content-article')
    print(new_feed)
    return new_feed

def to_soup(html):
    return BeautifulSoup(html, 'html.parser')

def get_journey():
    url = 'https://ncov.moh.gov.vn/dong-thoi-gian'
    page = requests.get(url, verify=False)
    soup = to_soup(page.text)
    journey = soup.find_all("div",class_='timeline')[:5]

    print(len(journey))

    dt_arr= []
    cnt_arr = []

    for j in journey:
        print(j.find("h3").text)
        dt_arr.append(j.find("h3").text)
        print(j.find("p").text)
        cnt_arr.append(j.find("p").text)


    return dt_arr,cnt_arr

def get_hotline(all=False):
    if all:
        url = 'https://ncov.moh.gov.vn/documents/20182/6848000/Duongdaynong/'
    else:
        url = 'Đường dây nóng: 19009095 / 19003228'
    return url

def get_video(video_id=0):
    video_list = {
        # Khuyen cao chung
        0:"https://ncov.moh.gov.vn/documents/20182/6863405/video003/",
        # Dieu khien phuong tien
        1:"https://ncov.moh.gov.vn/documents/20182/6863405/video002/",
        # Cach ly tai nha
        2:"https://ncov.moh.gov.vn/documents/20182/6863405/c%C3%A1ch+ly+01/",
        # Nhugn ai can cach ly
        3:"https://ncov.moh.gov.vn/documents/20182/6863405/C%C3%A1ch+ly+t%E1%BA%A1i+nh%C3%A0/",
        # Huong dan cach ly
        4:"https://ncov.moh.gov.vn/documents/20182/6863405/H%C6%B0%E1%BB%9Bng+d%E1%BA%ABn+c%C3%A1ch+ly+tai+nh%C3%A0%281%29/"
    }
    return video_list[video_id]

def get_symptom():
    symptom_txt = """"""
    return symptom_txt

def get_summary():
    url = 'https://suckhoetoandan.vn/'
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')

    main_row = soup.find_all("div",class_ ="box-heading")[1:]


    print(main_row)

    all_of_it = "SỐ LIỆU LŨY KẾ ĐẾN HIỆN TẠI:\n"
    all_of_it += "Toàn cầu:\n"

    number = main_row[0].find_all("span",class_ = "box-total")
    all_of_it += "Số người bị nhiễm: " + number[0].text + "\n"
    all_of_it += "Số người tử vong: " + number[2].text+ "\n"
    all_of_it += "Số người bình phục: " + number[4].text+ "\n"

    all_of_it += "Việt Nam:\n"

    number = main_row[0].find_all("span", class_="box-total")
    all_of_it += "Số người bị nhiễm: " + number[1].text + "\n"
    all_of_it += "Số người tử vong: " + number[3].text + "\n"
    all_of_it += "Số người bình phục: " + number[5].text + "\n"

    all_of_it += "SỐ LƯỢNG TĂNG TRONG NGÀY:\n"
    all_of_it += "Toàn cầu:\n"

    number = main_row[1].find_all("span", class_="box-total")
    all_of_it += "Số người bị nhiễm: " + number[0].text + "\n"
    all_of_it += "Số người tử vong: " + number[2].text + "\n"
    all_of_it += "Số người bình phục: " + number[4].text + "\n"

    all_of_it += "Việt Nam:\n"

    number = main_row[1].find_all("span", class_="box-total")
    all_of_it += "Số người bị nhiễm: " + number[1].text + "\n"
    all_of_it += "Số người tử vong: " + number[3].text + "\n"
    all_of_it += "Số người bình phục: " + number[5].text + "\n"

    print(all_of_it)

def sort_by_year(d):
    '''
    helper function for sorting a list of dictionaries'''
    return d.get('ma', None)

def get_detail_domestic():
    url = 'https://ncov.moh.gov.vn/web/guest/trang-chu'
    page = requests.get(url, verify=False)

    with open('data/info_citylist.txt', mode='r') as infile:
        reader = csv.reader(infile)
        mydict = {rows[0]: rows[1] for rows in reader}

    #print(mydict)
   # print(page.text)
    #28856
    #65976
    key = "function getInfoByMa(ma)"
    html = page.text
    start_domestic = html.index(key) + len(key)
    html = html[start_domestic:]
    key = "_congbothongke_WAR_coronadvcportlet_jsonData : '"
    start_domestic = html.index(key) + len(key)
    key = "}]'"
    end_domestic = html.index(key, start_domestic) + len(key) - 1;

    json_str = html[start_domestic:end_domestic]

    json_obj = json.loads(json_str)

    print(json_obj)

    all_of_it = "🛑CHI TIẾT TÌNH HÌNH COVID-19 TRONG NƯỚC"
    for row in sorted(json_obj, key=sort_by_year,reverse=True):
            if row['ma']!='' and row['ma']!='--Chọn địa phương--' and row['soCaNhiem']!='0':
                all_of_it += ("\n%s - Nhiễm: %s - Tử vong: %s - Nghi nhiễm: %s - Bình phục: %s" % (mydict[row['ma']].strip(), row['soCaNhiem'],row['tuVong'],row['nghiNhiem'],row['binhPhuc']))  # test

    print(all_of_it)


def get_news():
    url = 'https://suckhoetoandan.vn/'
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')

    main_row = soup.find("div",class_ ="list-new-left-type3").find_all("div", class_ ="item-new")

    message_str = """{
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    [CONTENT]
                ]
            }
        }
    }"""

    inside_cnt_template = """{
                        "title": "[TITLE]",
                        "image_url": "[IMG]",
                        "subtitle": "[SUBTITLE]",
                        "default_action": {
                            "type": "web_url",
                            "url": "[URL]",
                            "webview_height_ratio": "full"
                        },
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": "[URL]",
                                "title": "Xem tin ngay"
                            }
                        ]
                    },"""
    inside_cnt =""
    for row in main_row:
        tmp = inside_cnt_template.replace("[TITLE]",row.find('a').get('title'))
        tmp = tmp.replace("[URL]",row.find('a').get('href'))
        if row.find('img').get('src')[:4] == "http":
            tmp = tmp.replace("[IMG]",row.find('img').get('src'))
        else:
            tmp = tmp.replace("[IMG]", url+row.find('img').get('src'))

        tmp = tmp.replace("[SUBTITLE]",row.find('a').get('title'))
        inside_cnt += tmp

    message_str = message_str.replace("[CONTENT]",inside_cnt[:-1])

    message = json.loads(message_str)

    print(message)


def get_new_source():
    url = 'https://beta.dantri.com.vn/suc-khoe/nua-dem-bo-y-te-cong-bo-cung-luc-9-ca-mac-covid-19-moi-20200319211303006.htm'
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')

    main_row = soup.find("div", class_="dantri-widget dantri-widget--corona")

    print(main_row)



get_new_source()