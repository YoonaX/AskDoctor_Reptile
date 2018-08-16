import json

with open("F:\\Ask_Information\\保健养生\\戒烟戒酒\\其它\\https_$$www.120ask.com$question$60000678.htm.json", encoding= \
        'UTF-8') as load_f:
    load_dict = json.load(load_f)
    print("title: " + load_dict["title"])
    print("sex_age" + load_dict["sex_age"])
    print("ask_time" + load_dict["ask_time"])
    print("description" + load_dict["description"])
    print("helper:" + load_dict["helper:"])
    print("")
    for item in load_dict["ask_reply"]:
        print("doctor_detail:" + item["doctor_detail"])
        print("doctor_url:" + item["doctor_url"])
        for reply in item["doctor_reply"]:
            print("doctor_reply" + reply)
        print("")
