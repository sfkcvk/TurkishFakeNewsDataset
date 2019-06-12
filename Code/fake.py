from lxml import html
import requests
import io
import time
import os
import random

# 1 den başla 218 dahil olmayaak şekilde 1 artır
    for pg in range(1, 218):
        try:
            print(pg)
            # https://www.zaytung.com/digerleri.asp?pg=1
            # https://www.zaytung.com/digerleri.asp?pg=217
            page = requests.get('https://www.zaytung.com/digerleri.asp?pg=' + str(pg))
            pageTree = html.fromstring(page.content)

            table = pageTree.xpath('//div[@id="mainContent"]//h3/a/@href')
            print(table)
            time.sleep(random.randint(0, 5))

            for link in table:
                try:
                    print(link)
                    id = link[link.rfind('=') + 1:]

                    if not os.path.isfile("./Data/Fake/" + id + ".txt"):
                        # https://www.zaytung.com/haberdetay.asp?newsid=348669
                        haber = requests.get('https://www.zaytung.com/' + link.strip())
                        haberTree = html.fromstring(haber.content)


                        title = haberTree.xpath('//div[@id="manset"]/div/h1/text()')
                        body = haberTree.xpath('//div[@id="manset"]/div/p/text()')
                        content = " ".join(title) + " " + " ".join(body)
                        if content.strip() != "":
                            # ./Data/Fake/348669.txt
                            with io.open("./Data/Fake/" + id + ".txt", 'w', encoding='utf8') as f:
                                f.write(content.strip())

                        time.sleep(random.randint(0, 5))
                except:
                    print("hata oldu")
        except:
            print("hata oldu")