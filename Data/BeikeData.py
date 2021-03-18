import requests
from lxml import etree
import pandas as pd
# If you want to use this, you have to install requests, lxml and pandas in you computer
# You can just used "pip install xxx" in the terminal

urls = []
# This is used to page turning, and you can change the number "60" to set the size of the pages.
for i in range(1, 60+1):
    # This program can be used to get the data from Lianjia and Beike, just change the url to get data from the other.
    url_temp = 'https://bj.zu.ke.com/zufang/tongzhou/pg{}/#contentList'.format(i)
    urls.append(url_temp)

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}

data = []

for url in urls:
    resp = requests.get(url=url, headers=header)

    html = etree.HTML(resp.text)

    divs = html.xpath("/html/body/div[3]/div[1]/div[5]/div[1]/div[1]/div")
    for div in divs:
        house = []

        house_code = div.xpath("./@data-house_code")[0]

        house.append(house_code)

        title = div.xpath("./a/@title")[0]
        house.append(title)

        # location[0]: district; location[1]:community; location[2]: housing estate
        location = div.xpath("./div/p[2]/a/text()")
        if location:
            district = location[0]
            community = location[1]
            housing_estate = location[2]
        else:
            district = "0"
            community = "0"
            housing_estate = "0"

        house.append(district)
        house.append(community)
        house.append(housing_estate)

        # info[4]: size; info[5]: orientation; info[6]:house type
        info = div.xpath('./div/p[2]/text()')
        if len(info) >6:
            size = info[4].strip()
            orientation = info[5].strip()
            house_type = info[6].strip()
        elif len(info) == 6:
            size = info[3].strip()
            orientation = info[4].strip()
            house_type = info[5].strip()
        elif len(info) == 5:
            size = info[2].strip()
            orientation = info[3].strip()
            house_type = info[4].strip()
        elif len(info) == 4:
            size = info[1].strip()
            orientation = info[2].strip()
            house_type = info[3].strip()
        elif len(info) == 3:
            size = info[0].strip()
            orientation = info[1].strip()
            house_type = info[2].strip()
        else:
            size = "0"
            orientation = "0"
            house_type = "0"

        house.append(size)
        house.append(orientation)
        house.append(house_type)

        # floor[1]: floor
        floor = div.xpath("./div/p[2]/span/text()")
        if len(floor) >1:
            floor = floor[1].strip()
            floor = ''.join(floor.split())
        else:
            floor = "0"
        house.append(floor)

        price = div.xpath("./div/span/em/text()")[0]
        house.append(price)

        data.append(house)
        # print(floor)

resp.close()

# write the data into a .csv file
name = ['house_code', 'title', 'district', 'community', 'housing_estate', 'size',
        'orientation', 'house_type', 'floor', 'price']
test = pd.DataFrame(columns=name, data=data)

# In the "()" is the path of your document, if there is it will rewrite that, else it will creat one.
test.to_csv('C:/Users/11098/Desktop/BeikeData/tongzhou4000+.csv', encoding='gb18030')

print(test)