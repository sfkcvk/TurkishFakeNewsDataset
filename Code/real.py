from lxml import html
import requests
import io
import time
from datetime import timedelta, date
import os
import random

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2019, 5, 4)
end_date = date(2019, 5, 20)

for single_date in daterange(start_date, end_date):
    try:
        print(single_date.strftime("%Y%m%d"))
        paging = requests.get('http://www.hurriyet.com.tr/index/?d=' + single_date.strftime("%Y%m%d"))
        pagingTree = html.fromstring(paging.content)

        pageIndeces = pagingTree.xpath('//div[@class="paging"]/a/text()')
        pageIndeces.remove('›')

        print(pageIndeces)
        for pageIndex in pageIndeces:
            try:
                print(pageIndex)
                # http://www.hurriyet.com.tr/index/?d=20190522&p=2
                url = 'http://www.hurriyet.com.tr/index/?d=' + single_date.strftime("%Y%m%d")
                if pageIndex != '1':
                    url += '&p=' + pageIndex.strip()
                page = requests.get(url)
                pageTree = html.fromstring(page.content)

                table = pageTree.xpath('//div[@class="news"]//h3/a/@href')
                print(table)
                time.sleep(random.randint(0, 5))

                for link in table:
                    try:
                        print(link)
                        id = link[link.rfind('-') + 1:]

                        if not os.path.isfile("./Data/Real/" + id + ".txt"):
                            # http://www.hurriyet.com.tr/gundem/akil-almaz-olay-elini-beline-goturdu-ve-41069985
                            haber = requests.get('http://www.hurriyet.com.tr' + link.strip())
                            haberTree = html.fromstring(haber.content)


                            title1 = haberTree.xpath('//h1[@class="rhd-article-title"]/text()')
                            title2 = haberTree.xpath('//h1[@class="rhd-article-title-type-2"]/text()')
                            title3 = haberTree.xpath('//h1[@class="video-title"]/text()')
                            title4 = haberTree.xpath('//h1[@class="news-detail-title*"]/text()')

                            spot1 = haberTree.xpath('//h2[@class="rhd-article-spot"]/text()')
                            spot2 = haberTree.xpath('//h2[@class="rhd-article-spot-type-2"]/text()')
                            spot3 = haberTree.xpath('//h2[@class="news-detail-spot"]/text()')

                            detail1 = haberTree.xpath('//div[@class="rhd-all-article-detail"]/p/text()')
                            detail2 = haberTree.xpath('//div[@class="rhd-all-article-detail-type-2"]/p/text()')
                            detail3 = haberTree.xpath('//div[@class="video-description"]/text()')
                            detail4 = haberTree.xpath('//h2[@class="description"]/text()')

                            content = " ".join(title1) + " ".join(title2) + " ".join(title3) + " ".join(title4) + " " + " ".join(spot1) + " ".join(spot2) + " " + " ".join(detail1) + " ".join(detail2) + " ".join(detail3) + " ".join(detail4)
                            if content.strip() != "":
                                # ./Data/Real/41221359.txt
                                with io.open("./Data/Real/" + id + ".txt", 'w', encoding='utf8') as f:
                                    f.write(content.strip())

                            time.sleep(random.randint(0, 5))
                    except:
                        print("hata oldu")
            except:
                print("hata oldu")
    except:
        print("hata oldu")