import csv


place_contents = ""
parking_contents = ""
weather_contents = ""
restaurant_contents = ""
cafe_contents = ""
relation_contents = ""
popular_contents = ""

def make_doc():
    f = open('/home/ubuntu/festabot/option/tf_idf_option/category_sentence.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        make_list(line[0], line[1])
    f.close()

def make_list(category, text):
    global place_contents
    global parking_contents
    global weather_contents
    global restaurant_contents
    global cafe_contents
    global relation_contents
    global popular_contents

    if category == "주소":
        place_contents += text + " "
    elif category == "날씨":
        weather_contents += text + " "
    elif category == "주차장":
        parking_contents += text + " "
    elif category == "맛집":
        restaurant_contents += text+" "
    elif category == "카페":
        cafe_contents += text + " "
    elif category == "연관":
        relation_contents += text + " "
    elif category == "인기":
        popular_contents += text + " "

make_doc()
