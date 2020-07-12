# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
from bs4 import BeautifulSoup
import csv
import urllib.request
import ssl
import json
import requests
import os
import html
import random
import pathlib
from typing import Any, Text, Dict, List
#
from rasa_sdk.events import FollowupAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
import mysql.connector
from mysql.connector import Error, errorcode
import gc

# MySQL param
MYSQL_HOST = 'localhost'
MYSQL_DB = 'chatbotdb'
MYSQL_USER = 'somethinghere'
MYSQL_PASS = 'somethinghere'

more_text = "Bạn có cần thêm gì về COVID-19 như: số ca nhiễm mới nhất, diễn biến, hotline cần thiết, khai báo y tế, tình hình thế giới... không?"



def load_faq():
    q_list = []
    a_list = []

    filepath = str(pathlib.Path().absolute()) + '/crawler/data/info_faq.txt'.replace('/', os.sep)
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            # Process
            print("Process line ", line)
            q_list.append( line.split("|")[0].replace("\n",""))
            a_list.append( line.split("|")[1].replace("\n",""))
            line = fp.readline()
            cnt += 1
    return q_list,a_list

q_list,a_list=load_faq()
print("Loaded", len(q_list))

def load_suggest():
    temp_button_lst = []

    temp_button_lst.append({
        "type": "postback",
        "title": "❗Số ca nhiễm mới nhất",
        "payload": "Số ca nhiễm mới nhất"
    })
    temp_button_lst.append({
        "type": "postback",
        "title": "📣Diễn biến mới nhất",
        "payload": "Diễn biến"
    })
    temp_button_lst.append({
        "type": "postback",
        "title": "✍Khai báo y tế",
        "payload": "tờ khai y tế"
    })
    temp_button_lst.append({
        "type": "postback",
        "title": "😰Triệu chứng COVID-19",
        "payload": "triệu chứng"
    })
    temp_button_lst.append({
        "type": "postback",
        "title": "🦠COVID-19 là gì?",
        "payload": "covid19"
    })
    temp_button_lst.append({
        "type": "postback",
        "title": "📞Đường dây nóng",
        "payload": "hotline"
    })
    temp_button_lst.append({
        "type": "postback",
        "title": "😷Đeo khẩu trang đúng",
        "payload": "khẩu trang"
    })
    temp_button_lst.append({
        "type": "postback",
        "title": "👏Rửa tay đúng cách",
        "payload": "rửa tay"
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "📨Khuyến cáo của Bộ",
        "payload": "khuyến cáo"
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "❓Ai đang chat đó?",
        "payload": "bạn là ai"
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "😱Tôi cảm thấy lo lắng",
        "payload": "tôi lo lắng"
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "🇻🇳Tình hình các tỉnh thành",
        "payload": "số liệu tỉnh thành"
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "🌐Tình hình thế giới",
        "payload": "thế giới thế nào"
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "📰Tin tức trên báo",
        "payload": "tin mới"
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "🔔Đăng ký nhận tin",
        "payload": "regnotify",
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "🔬Tự kiểm tra y tế",
        "payload": "trắc nghiệm y tế",
    })

    temp_button_lst.append({
        "type": "postback",
        "title": "🛌Tình trạng bệnh nhân",
        "payload": "tình trạng bệnh nhân",
    })

    return temp_button_lst

button_lst = load_suggest()
button_share = {
        "type": "web_url",
        "url": "https://note.miai.vn/covid19/share.html",
        "title": "💓Chia sẻ người thân",
        "webview_height_ratio": "full",
        "messenger_extensions": "true",
        "fallback_url": "https://note.miai.vn/covid19/share.html"
    }

def suggest():
    global button_lst
    return random.sample(button_lst, k=2)


class act_greeting(Action):

    def name(self) -> Text:
        return "act_greeting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Open a file: file
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        button = {
            "type": "postback",
            "title": "❗Số ca nhiễm mới nhất",
            "payload": "Số ca nhiễm mới nhất"
        }
        button1 = {
            "type": "postback",
            "title": "📣Diễn biến mới nhất",
            "payload": "Diễn biến",
        }
        button2 = {
            "type": "postback",
            "title": "✍Khai báo y tế",
            "payload": "tờ khai y tế",
        }
        ret_text = "Xin chào! Tôi là trợ lý ảo được vận hành bởi Mì AI Blog (https://miai.vn). Tôi ở đây để cung cấp cho bạn tất cả các thông tin về COVID-19 theo thông tin từ website chính thức của Bộ Y Tế. Bạn có thể hỏi tôi về: \n- Triệu chứng bệnh\n- Diễn biến mới nhất\n- Số ca nhiễm hiện tại\n- Hotline cần thiết\n- ...\n"
        dispatcher.utter_message(text=ret_text, buttons=[button, button1, button2])
        print('[%s] -> %s' % (self.name(), ret_text))

        del ret_text, button, button1, button2
        gc.collect()


        return []

def get_faq():
    idx =random.randint(0,len(q_list)-1)
    ret_text = "🎁Quà tặng kiến thức cho bạn:\n"
    ret_text += "🔸Hỏi: " + q_list[idx] + "\n"
    ret_text += "🔸Đáp:️ " + a_list[idx] + "\n"
    ret_text += "Nguồn: bit.ly/100FAQPeter"

    return ret_text



class act_needmore(Action):

    def name(self) -> Text:
        return "act_needmore"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Open a file: file

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text="Bạn có cần thêm gì về COVID-19 như: triệu chứng, diễn biến, hotline cần thiết, khai báo y tế... không?"
            , buttons=temp_button_lst)

        del temp_button_lst
        gc.collect()

        return []


class act_unknown(Action):

    def name(self) -> Text:
        return "act_unknown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Open a file: file
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        dispatcher.utter_message(
            text="Xin lỗi bạn vì hiện tại tôi chưa hiểu bạn muốn gì! Bạn hãy bấm vào đây để tôi nhờ chị Google giải đáp nhé: https://www.google.com.vn/search?q='" +
                 tracker.latest_message['text'].replace(" ", "%20") + "'")
        button = {
            "type": "postback",
            "title": "❗Số ca nhiễm mới nhất",
            "payload": "Số ca nhiễm mới nhất"
        }
        button1 = {
            "type": "postback",
            "title": "📣Diễn biến mới nhất",
            "payload": "Diễn biến",
        }
        button2 = {
            "type": "postback",
            "title": "✍Khai báo y tế",
            "payload": "tờ khai y tế",
        }
        dispatcher.utter_message(
            text="Xin chào! Tôi là trợ lý ảo được vận hành bởi Mì AI Blog (https://miai.vn). Tôi ở đây để cung cấp cho bạn tất cả các thông tin về COVID-19 . Bạn có thể hỏi tôi về: triệu chứng, diễn biến, hotline cần thiết...\n"
            , buttons=[button, button1, button2])

        del button, button1, button2
        gc.collect()

        return []


def sort_by_year(d):
    '''
    helper function for sorting a list of dictionaries'''
    return d.get('ma', None)


class act_hotline(Action):

    def name(self) -> Text:
        return "act_hotline"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Open a file: file
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        file = open(str(pathlib.Path().absolute()) + '/crawler/data/info_hotlines.txt'.replace('/', os.sep), mode='r',
                    encoding="utf-8")

        # read all lines at once
        all_of_it = file.read()

        # close the file
        file.close()

        button = {
            "type": "phone_number",
            "title": "📞Gọi 1900.9095",
            "payload": "19009095",
        }
        button1 = {
            "type": "phone_number",
            "title": "📞Gọi 1900.3228",
            "payload": "19003228",
        }

        dispatcher.utter_message(text=all_of_it)
        dispatcher.utter_message(
            text="Hoặc có thể liên hệ hotline Bộ Y Tế: 1900.9095 hoặc 1900.3228 (Nguồn tin: Bộ Y Tế (https://moh.gov.vn/)",
            buttons=[button, button1])

        del button1, button, all_of_it

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []


class act_covid_info(Action):

    def name(self) -> Text:
        return "act_covid_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Open a file: file
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        file = open(str(pathlib.Path().absolute()) + '/crawler/data/info_covid19.txt'.replace('/', os.sep), mode='r',
                    encoding="utf-8")

        # read all lines at once
        all_of_it = file.read()

        # close the file
        file.close()

        dispatcher.utter_message(text=all_of_it,
                                 image="https://raw.githubusercontent.com/thangnch/photos/master/covid.jpg")
        print(all_of_it)
        del all_of_it

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []


class act_symptom(Action):

    def name(self) -> Text:
        return "act_symptom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Open a file: file
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        file = open(str(pathlib.Path().absolute()) + '/crawler/data/info_symptom.html'.replace('/', os.sep), mode='r',
                    encoding="utf-8")

        # read all lines at once
        all_of_it = file.read()

        # close the file
        file.close()

        dispatcher.utter_message(text=all_of_it)
        del all_of_it

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []


class act_journey(Action):

    def name(self) -> Text:
        return "act_journey"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        # Send typing first

        url = 'https://ncov.moh.gov.vn/dong-thoi-gian'
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')
        journey = soup.find_all("div", class_='timeline')[:5]

        dt_arr = []
        cnt_arr = []

        for j in reversed(journey):
            dt_arr.append(j.find("h3").text)
            cnt_arr.append(j.find("p").text)

        all_of_it = "DIỄN BIẾN MỚI NHẤT CỦA DỊCH COVID 19 \n"

        for idx in range(len(cnt_arr)):
            all_of_it += "🛑" + dt_arr[idx] + "\n" + cnt_arr[idx] + "\n\n"
        all_of_it += "Nguồn tin: Bộ Y Tế (https://moh.gov.vn/)"
        dispatcher.utter_message(text=all_of_it)

        button = {
            "type": "postback",
            "title": "🔔Đăng ký nhận tin",
            "payload": "regnotify",
        }
        dispatcher.utter_message(
            "Nếu bạn muốn đăng ký nhận các tin mới nhất về dịch COVID-19 hãy bấm nút bên dưới nhé:",
            buttons=[button])

        del button, all_of_it, dt_arr, cnt_arr, url, page, soup,journey

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []


class act_numbers(Action):

    def name(self) -> Text:
        return "act_numbers"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        url = 'https://suckhoetoandan.vn/'
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')

        try:

            main_row = soup.find_all("div", class_="box-heading")[1:]

            all_of_it = "🛑SỐ LIỆU LŨY KẾ CẬP NHẬT ĐẾN HIỆN TẠI:\n"
            all_of_it += "🌐Toàn cầu:\n"

            number = main_row[0].find_all("span", class_="box-total")
            all_of_it += "▪Số người bị nhiễm: " + number[0].text + "\n"
            all_of_it += "▪Số người tử vong: " + number[2].text + "\n"
            all_of_it += "▪Số người bình phục: " + number[4].text + "\n"

            all_of_it += "🇻🇳Việt Nam:\n"

            number = main_row[0].find_all("span", class_="box-total")
            all_of_it += "▪Số người bị nhiễm: " + number[1].text + "\n"
            all_of_it += "▪Số người tử vong: " + number[3].text + "\n"
            all_of_it += "▪Số người bình phục: " + number[5].text + "\n"

            all_of_it += "\n\n🛑SỐ LƯỢNG TĂNG THÊM TRONG NGÀY HÔM NAY:\n"
            all_of_it += "🌐Toàn cầu:\n"

            number = main_row[1].find_all("span", class_="box-total")
            all_of_it += "▪Số người bị nhiễm: " + number[0].text + "\n"
            all_of_it += "▪Số người tử vong: " + number[2].text + "\n"
            all_of_it += "▪Số người bình phục: " + number[4].text + "\n"

            all_of_it += "🇻🇳Việt Nam:\n"

            number = main_row[1].find_all("span", class_="box-total")
            all_of_it += "▪Số người bị nhiễm: " + number[1].text + "\n"
            all_of_it += "▪Số người tử vong: " + number[3].text + "\n"
            all_of_it += "▪Số người bình phục: " + number[5].text + "\n"

            all_of_it += "Nguồn tin: Sức khỏe toàn dân (http://suckhoetoandan.vn/)"
            print(all_of_it)

            del  main_row, number
        except:
            all_of_it = "Dịch vụ xin tạm ngưng để bảo trì. Xin cảm ơn!"
            del  main_row, number

        dispatcher.utter_message(text=all_of_it)

        button = {
            "type": "postback",
            "title": "🔔Đăng ký nhận tin",
            "payload": "regnotify",
        }
        dispatcher.utter_message(
            "Nếu bạn muốn đăng ký nhận các tin mới nhất về dịch COVID-19 hãy bấm nút bên dưới nhé:",
            buttons=[button])
        del button, url, page,soup, all_of_it

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []


class act_selfcare(Action):

    def name(self) -> Text:
        return "act_selfcare"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        url = 'https://note.miai.vn/covid19'

        dispatcher.utter_message(
            text="Bạn hãy tự kiểm tra y tế với liên kết bên dưới nhé. Chú ý: Thông tin trắc nghiệm chỉ mang tính chất tham khảo, hãy liên hệ các cơ quan Y tế để nhận thông tin tư vấn cuối cùng.")  # ,buttons=[button])

        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Tự kiểm tra Y tế",
                            "image_url": "https://img.giaoduc.net.vn/w1050/Uploaded/2020/zreyxqnexq/2016_10_27/thi_trac_nghiem.jpg",
                            "subtitle": "Tự kiểm tra tình trạng Y tế của bạn",
                            "default_action": {
                                "type": "web_url",
                                "url": url,
                                "webview_height_ratio": "full",
                                "messenger_extensions": "true",
                                "fallback_url": url

                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": url,
                                    "title": "🔬Kiểm tra luôn",
                                    "webview_height_ratio": "full",
                                    "messenger_extensions": "true",
                                    "fallback_url": url
                                }
                            ]
                        }
                    ]
                }
            }
        }
        dispatcher.utter_message(json_message=message)

        del url, message

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()
        return []


class act_declare(Action):

    def name(self) -> Text:
        return "act_declare"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        url = 'https://tokhaiyte.vn/'
        '''button = {
            "type": "web_url",
            "title": "Khai báo y tế",
            "url": url,
            "webview_height_ratio": "full",
            "messenger_extensions": "true",
            "fallback_url":url
        }
        print(button)
        '''
        dispatcher.utter_message(
            text="Bạn hãy truy cập trang web khai báo y tế chính thức của Bộ Y Tế (chú ý chọn tờ khai cho người nhập cảnh/khách nội địa):")  # ,buttons=[button])

        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Khai báo y tế!",
                            "image_url": "https://tokhaiyte.vn/upload/2001432/Image/banner_vi.png",
                            "subtitle": "Trang web khai báo y tế chính thức của Bộ Y Tế.",
                            "default_action": {
                                "type": "web_url",
                                "url": url,
                                "webview_height_ratio": "full",
                                "messenger_extensions": "true",
                                "fallback_url": url

                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": url,
                                    "title": "✍Khai báo luôn",
                                    "webview_height_ratio": "full",
                                    "messenger_extensions": "true",
                                    "fallback_url": url
                                }
                            ]
                        }
                    ]
                }
            }
        }
        dispatcher.utter_message(json_message=message)

        del url, message

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []


class act_patient(Action):

    def name(self) -> Text:
        return "act_patient"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        url = 'https://note.miai.vn/covid19/patient.html'

        '''button = {
            "type": "web_url",
            "title": "Tình trạng các bệnh nhân",
            "url": url,
            "webview_height_ratio": "full",
            "messenger_extensions": "true",
            "fallback_url":url
        }
        print(button)
        '''
        dispatcher.utter_message(
            text="Bạn hãy truy cập trang web dưới để cập nhật tình trạng các bệnh nhân nhé (nguồn tin: Bộ Y Tế):")  # ,buttons=[button])

        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Tình trạng các bệnh nhân",
                            "image_url": "https://ncov.moh.gov.vn/corona-home-theme/images/logo_byt.png",
                            "subtitle": "Trang web cập nhật tình trạng các bệnh nhân",
                            "default_action": {
                                "type": "web_url",
                                "url": url,
                                "webview_height_ratio": "full",
                                "messenger_extensions": "true",
                                "fallback_url": url

                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": url,
                                    "title": "🔎Xem luôn",
                                    "webview_height_ratio": "full",
                                    "messenger_extensions": "true",
                                    "fallback_url": url
                                }
                            ]
                        }
                    ]
                }
            }
        }
        dispatcher.utter_message(json_message=message)

        del url, message

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []


class act_washhand(Action):

    def name(self) -> Text:
        return "act_washhand"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        # print(button)
        dispatcher.utter_message(text="Bạn hãy tham khảo cách rửa tay cung cấp bởi WHO sau đây:",
                                 image="https://raw.githubusercontent.com/thangnch/photos/master/ruatay.jpg")
        # print(all_of_it)
        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []


class act_wearmask(Action):

    def name(self) -> Text:
        return "act_wearmask"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        # print(button)
        dispatcher.utter_message(text="Bạn hãy tham khảo cách đeo khẩu trang đúng cách sau đây để phòng COVID-19 nhé:",
                                 image="https://raw.githubusercontent.com/thangnch/photos/master/khautrang.jpg")
        # print(all_of_it)
        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []


class act_recommend(Action):

    def name(self) -> Text:
        return "act_recommend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        url = 'https://youtu.be/9JA4aDSrbFE'

        dispatcher.utter_message(text="Bạn tham khảo clip khuyến cáo của Bộ Y Tế tại đây: ")  # + url)

        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Khuyến cáo của Bộ Y tế",
                            "image_url": "http://i3.ytimg.com/vi/9JA4aDSrbFE/maxresdefault.jpg",
                            "subtitle": "Khuyến cáo chính thức về phòng và chống dịch COVID-19",
                            "default_action": {
                                "type": "web_url",
                                "url": url,
                                "webview_height_ratio": "full"
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": url,
                                    "title": "🔎Xem khuyến cáo"
                                }
                            ]
                        }
                    ]
                }
            }
        }
        dispatcher.utter_message(json_message=message)

        del url, message

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []


class act_sad(Action):

    def name(self) -> Text:
        return "act_sad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        ret_text = "💗Bạn đừng quá hoảng sợ và lo lắng. Hãy thực hiện đúng khuyến cáo, hướng dẫn phòng bệnh, chống bệnh COVID-19 của Bộ Y Tế. Hãy tỉnh táo, mạnh mẽ và đoàn kết để chiến thắng dịch bệnh. Truy cập trang web chính thức của Bộ (http://ncov.moh.gov.vn) hoặc gọi hotline 19009095 / 19003228 để được trợ giúp."

        dispatcher.utter_message(
            text=ret_text)  # , image="https://scontent.fhan7-1.fna.fbcdn.net/v/t1.0-9/84290840_10206825015860351_4696366899305381888_o.jpg?_nc_cat=107&_nc_sid=825194&_nc_ohc=7XN19V5cbx0AX9aEmXb&_nc_ht=scontent.fhan7-1.fna&oh=2558af85df74a93e04dad0dc6d860d8f&oe=5E94536B")
        # print(all_of_it)

        url = 'https://www.youtube.com/watch?v=BtulL3oArQw'
        dispatcher.utter_message(
            text="Hãy thư giãn cùng video clip rửa tay Ghen Covy nhé:")  # + url           )
        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Video clip Ghen Co Vy",
                            "image_url": "http://i3.ytimg.com/vi/BtulL3oArQw/maxresdefault.jpg",
                            "subtitle": "Hướng dẫn phòng chống dịch COVID-19",
                            "default_action": {
                                "type": "web_url",
                                "url": url,
                                "webview_height_ratio": "full",
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": url,
                                    "title": "🔎Xem clip"
                                }
                            ]
                        }
                    ]
                }
            }
        }
        dispatcher.utter_message(json_message=message)

        del url , message, ret_text

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []


class act_number_domestic(Action):

    def name(self) -> Text:
        return "act_number_domestic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        url = 'https://ncov.moh.gov.vn/web/guest/trang-chu'
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')
        #mydict = None

        try:

            domestic = soup.find_all("table", id='sailorTable')[0].find_all("tr")

            # print(domestic)
            all_of_it = "🇻🇳CHI TIẾT TÌNH HÌNH COVID-19 TRONG NƯỚC"

            data = None
            for d_row in domestic:
                print("--")
                d_col = d_row.find_all("td")
                data = []
                for el in d_col:
                    # print(el.text)
                    data.append(str(el.text))
                # print(data[0])
                if len(data) >= 5:
                    print(data[0])
                    all_of_it += ("\n▪ %s - Nhiễm: %s - Điều trị: %s - Khỏi: %s - Tử vong: %s" % (
                        data[0], data[1], data[2], data[3], data[4]))  # test

            all_of_it += "\nNguồn tin: Bộ Y Tế(https://moh.gov.vn/)"

            print(all_of_it)

            del domestic, data

        except:
            all_of_it = "Dịch vụ xin tạm ngưng để bảo trì. Xin cảm ơn!"

        del url, page, soup

        dispatcher.utter_message(
            text=all_of_it
        )

        button = {
            "type": "postback",
            "title": "🔔Đăng ký nhận tin",
            "payload": "regnotify",
        }
        dispatcher.utter_message(
            "Nếu bạn muốn đăng ký nhận các tin mới nhất về dịch COVID-19 hãy bấm nút bên dưới nhé:",
            buttons=[button])

        del button, all_of_it

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []

class act_number_inter(Action):

    def name(self) -> Text:
        return "act_number_inter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        url = 'https://www.worldometers.info/coronavirus/'
        page = requests.get(url, verify=False)
        soup = BeautifulSoup(page.text, 'html.parser')

        try:
            inter = soup.find_all("table", id='main_table_countries_today')[0].find_all("tr")[9:29]

            all_of_it = "🌐TOP 20 QUỐC GIA NHIỄM NHIỀU NHẤT TRÊN THẾ GIỚI"

            data = None
            for d_row in inter:
                print("--")
                data = d_row.find_all("td")
                # data = []
                # for el in d_col:
                #    #print(el.text)
                #    data.append(str(el.text))
                # print(data[0])
                if len(data) >= 5:
                    # print(data[0])
                    all_of_it += ("\n▪ %s - Nhiễm: %s - Tử vong: %s - Khỏi: %s" % (
                        data[0].text, data[1].text, data[3].text, data[5].text))  # test

            print(all_of_it)

            all_of_it += "\nNguồn tin: https://www.worldometers.info"

            del inter
            print(all_of_it)
        except:
            all_of_it = "Dịch vụ xin tạm ngưng để bảo trì. Xin cảm ơn!"
        dispatcher.utter_message(
            text=all_of_it
        )
        button = {
            "type": "postback",
            "title": "🔔Đăng ký nhận tin",
            "payload": "regnotify",
        }
        dispatcher.utter_message(
            "Nếu bạn muốn đăng ký nhận các tin mới nhất về dịch COVID-19 hãy bấm nút bên dưới nhé:",
            buttons=[button])

        del button, all_of_it, page, soup

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []

class act_cachly(Action):

    def name(self) -> Text:
        return "act_cachly"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        ret_text = "⚠Bạn tham khảo khuyến cáo về Cách ly của Bộ Y Tế sau đây nhé:"

        dispatcher.utter_message(
            text=ret_text)  # , image="https://scontent.fhan7-1.fna.fbcdn.net/v/t1.0-9/84290840_10206825015860351_4696366899305381888_o.jpg?_nc_cat=107&_nc_sid=825194&_nc_ohc=7XN19V5cbx0AX9aEmXb&_nc_ht=scontent.fhan7-1.fna&oh=2558af85df74a93e04dad0dc6d860d8f&oe=5E94536B")
        # print(all_of_it)

        url = 'https://youtu.be/wo-R5-wqEV8'
        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Khuyến cáo cách ly tại nhà",
                            "image_url": "http://i3.ytimg.com/vi/wo-R5-wqEV8/maxresdefault.jpg",
                            "subtitle": "Hướng dẫn chi tiết phương pháp cách ly tại nhà",
                            "default_action": {
                                "type": "web_url",
                                "url": url,
                                "webview_height_ratio": "full",
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": url,
                                    "title": "🔎Xem clip"
                                }
                            ]
                        }
                    ]
                }
            }
        }
        dispatcher.utter_message(json_message=message)

        url = 'https://youtu.be/brDo1Yc-0Gk'
        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Những ai cần cách ly?",
                            "image_url": "http://i3.ytimg.com/vi/brDo1Yc-0Gk/maxresdefault.jpg",
                            "subtitle": "Những đối tượng cần phải cách ly theo khuyến cáo",
                            "default_action": {
                                "type": "web_url",
                                "url": url,
                                "webview_height_ratio": "full",
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": url,
                                    "title": "🔎Xem clip"
                                }
                            ]
                        }
                    ]
                }
            }
        }
        dispatcher.utter_message(json_message=message)

        del url, message

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()
        return []


class act_news(Action):

    def name(self) -> Text:
        return "act_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))

        try:
            ret_text = "📰Bạn tham khảo các tin tức mới nhất về COVID-19 nhé (Nguồn tin: https://suckhoetoandan.vn/):"

            dispatcher.utter_message(
                text=ret_text)  # , image="https://scontent.fhan7-1.fna.fbcdn.net/v/t1.0-9/84290840_10206825015860351_4696366899305381888_o.jpg?_nc_cat=107&_nc_sid=825194&_nc_ohc=7XN19V5cbx0AX9aEmXb&_nc_ht=scontent.fhan7-1.fna&oh=2558af85df74a93e04dad0dc6d860d8f&oe=5E94536B")

            url = 'https://suckhoetoandan.vn/'
            page = requests.get(url, verify=False)
            soup = BeautifulSoup(page.text, 'html.parser')

            main_row = soup.find("div", class_="list-new-left-type3").find_all("div", class_="item-new")

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
                                            "title": "🔎Xem tin ngay"
                                        }
                                    ]
                                },"""
            inside_cnt = ""
            for row in main_row:
                tmp = inside_cnt_template.replace("[TITLE]", html.escape(row.find('a').get('title')))
                tmp = tmp.replace("[URL]", row.find('a').get('href'))
                if row.find('img').get('src')[:4] == "http":
                    tmp = tmp.replace("[IMG]", row.find('img').get('src'))
                else:
                    tmp = tmp.replace("[IMG]", url + row.find('img').get('src'))

                tmp = tmp.replace("[SUBTITLE]", html.escape(row.find('a').get('title')))
                inside_cnt += tmp

            message_str = message_str.replace("[CONTENT]", inside_cnt[:-1])

            # print(message_str)

            message = json.loads(message_str)

            # print(message)

            dispatcher.utter_message(json_message=message)
            del message, main_row, soup, page, url, ret_text
        except:
            all_of_it = "Dịch vụ xin tạm ngưng để bảo trì. Xin cảm ơn!"
            dispatcher.utter_message(
                text=all_of_it)
            del all_of_it


        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []

def send_typing(dispatcher, conversation_id=""):

    dispatcher.utter_message(
        text="Bạn vui lòng đợi trong giây lát..."
    )
    return

class ActionTellID(Action):
    """Informs the user about the conversation ID."""

    def name(self) -> Text:
        return "action_tell_id"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        conversation_id = tracker.sender_id

        # Response with Typing
        send_typing(dispatcher,conversation_id)

        return [FollowupAction("action_tell_id_1")]


class ActionTellID_1(Action):
    """Informs the user about the conversation ID."""

    def name(self) -> Text:
        return "action_tell_id_1"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        #conversation_id = tracker.sender_id


        dispatcher.utter_message(
            text="Hi everybody"
        )


        return []


class act_reg_notify(Action):
    """Informs the user that a plant needs water."""

    def name(self) -> Text:
        return "act_reg_notify"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Insert to DB
        connection = None
        chat_id = tracker.sender_id
        try:
            connection = mysql.connector.connect(host=MYSQL_HOST, database=MYSQL_DB, user=MYSQL_USER,
                                                 password=MYSQL_PASS)

            mysql_insert_query = "INSERT INTO tblChatID(chat_id) " \
                                 " VALUES ('" + chat_id + "')"

            cursor = connection.cursor()
            cursor.execute(mysql_insert_query)
            connection.commit()
            cursor.close()

            del cursor, mysql_insert_query


        except mysql.connector.Error as error:
            print("Failed update info {}".format(error))
        finally:
            if connection is not None:
                connection.close()
                del connection

        dispatcher.utter_message(
            "Cảm ơn bạn đã đăng ký nhận tin. Tôi sẽ gửi đến bạn các diễn biến mới nhất về dịch COVID-19!")

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()


        return []


class act_cancel_notify(Action):
    """Informs the user that a plant needs water."""

    def name(self) -> Text:
        return "act_cancel_notify"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Insert to DB
        connection = None
        chat_id = tracker.sender_id
        try:
            connection = mysql.connector.connect(host=MYSQL_HOST, database=MYSQL_DB, user=MYSQL_USER,
                                                 password=MYSQL_PASS)

            mysql_insert_query = "DELETE FROM tblChatID " \
                                 " WHERE chat_id= '" + chat_id + "'"

            cursor = connection.cursor()
            cursor.execute(mysql_insert_query)
            connection.commit()
            cursor.close()
            del cursor


        except mysql.connector.Error as error:
            print("Failed delete info {}".format(error))
        finally:
            if connection is not None:
                connection.close()
                del connection

        button = {
            "type": "postback",
            "title": "🔔Đăng ký nhận tin",
            "payload": "regnotify",
        }
        dispatcher.utter_message("Đã hủy nhận tin thành công. Nếu bạn muốn đăng ký nhận tin hãy bấm nút bên dưới nhé:",
                                 buttons=[button])

        del button

        gift_cnt = get_faq()
        dispatcher.utter_message(
            text=gift_cnt)

        temp_button_lst = suggest()
        temp_button_lst.append(button_share)
        dispatcher.utter_message(
            text=more_text
            , buttons=temp_button_lst)

        del gift_cnt, temp_button_lst
        gc.collect()

        return []
