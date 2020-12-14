

import requests
import re
import json

def get_categorylist(index_url):
    data = re.findall("应用分类(.*?)</ul></div> <div class=", requests.get(index_url).text)
    data = data[0].split("游戏应用")
    list1 = re.findall("<a  href=\"/category/(.*?)</a></li>", data[0])
    list2 = re.findall("<a  href=\"/category/(.*?)</a></li>", data[1])
    list = []
    for l in list1:
        l = l.split("\">")
        list.append(l)
    for l in list2:
        l = l.split("\">")
        list.append(l)
    for i in list:
        print(i)
    return list

def get_category(selected_url_category,page_begin, page_end):
    app_details_list = []
    for page in range(int(page_begin)-1, int(page_end)):
        print("正在爬取第"+str(page)+"页, 共"+page_end+"页")
        url = selected_url_category+"&page="+str(page)
        data = requests.get(url).text
        #print(data)
        data1 = json.loads(data)
        for data in data1["data"]:
            app_details_list.append([data["displayName"], data["packageName"]])
            #print(data["displayName"], data["packageName"])
    #print(app_details_list)
    return app_details_list

def get_download_link(url_details, app_details_list):
    download_link_list = []
    for app in app_details_list:
        url = url_details+app[1]
        data = re.findall("<div class=\"app-info-down\"> <a href=\"(.*?)\" class=\"download\">", requests.get(url).text)
        download_link_list.append("https://app.mi.com"+data[0])
        print(app[0]+" https://app.mi.com/details?id="+app[1])
    return download_link_list


if __name__ == '__main__':
    url = "https://app.mi.com/"
    url_category_api ="https://app.mi.com/categotyAllListApi?"
    # https://app.mi.com/categotyAllListApi?page=0&categoryId=20
    url_details = "https://app.mi.com/details?id="
    # https: // app.mi.com / details?id = com.joym.legendhero.mi


    category_list = get_categorylist(url)
    print("==========================================")
    category_selected = input("请输入要爬取的app类型编号：")
    print("请输入要爬取的页码")
    page_begin = input("开始页码：")
    page_end = input("结束页码：")
    print(">>>>>>>开始爬取>>>>>>>>>>>>>>>>")
    app_details_list = get_category(url_category_api+"categoryId="+str(category_selected), page_begin, page_end)
    download_link_list = get_download_link(url_details, app_details_list)

    category_dict = {}
    for category in category_list:
        category_dict[category[0]] = category[1]


    file_name = category_dict[category_selected] + "--" + str(page_begin)+"--" + str(page_end) + ".txt"
    with open(file_name, 'w', encoding='utf-8') as f:
        for n in zip(app_details_list, download_link_list):
            f.write("https://app.mi.com/details?id="+m[1] + " " + n + "\n")
    print("===============爬取完毕=======================\n")
    print("本次爬取"+str(len(app_details_list))+"个\n")