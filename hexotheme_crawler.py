from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import OrderedDict


# 利用python爬取github中hexo theme的stars排名
def hexotheme_craw(max_pages):
    theme_dict = {}
    page = 1

    while page <= max_pages:
        # 在http://github.com中搜索'hexo theme'
        url = 'https://github.com/search?p=' + str(page) + '&q=hexo+theme&type=Repositories&utf8=%E2%9C%93'

        response = urlopen(url)
        plain_text = response.read()

        page_soup = BeautifulSoup(plain_text, 'html.parser')

        containers = page_soup.find_all("div", class_="repo-list-item")

        for container in containers:
            href = 'https://github.com/' + container.div.h3.a["href"]
            theme_dict[href] = container.find("a", class_="muted-link").get_text().strip()

        page += 1

    return OrderedDict(sorted(theme_dict.items(),
                              key=lambda t: compare(t[1]), reverse=True))


# 比较依据，将4.4k转为4400
def compare(val):
    if val[-1].lower() == 'k':
        return int(float(val[:-1]) * 1000)
    return int(val)


if __name__ == '__main__':
    result = hexotheme_craw(5)
    print(len(result))
    for k, v in result.items():
        print(k, v)



