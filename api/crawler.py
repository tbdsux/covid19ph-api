from bs4 import BeautifulSoup
import requests
import pandas as pd
import json


class Crawler:
    def __init__(self, store_mode="NONE"):
        super(Crawler, self).__init__()
        self.store_mode = store_mode
        self.__base_url = (
            "https://en.wikipedia.org/wiki/COVID-19_pandemic_in_the_Philippines"
        )
        self.__keys = [
            "confirmed",
            "active",
            "severe",
            "critical",
            "recovered",
            "deaths",
            "fatality_rate",
        ]

        __tb_Name = "infobox"

        soup = BeautifulSoup(requests.get(self.__base_url).text, "html.parser")

        self.table = soup.find("table", attrs={"class": __tb_Name})

    def get_all(self):
        # remove some unnecessary tags
        for sup in self.table.find_all("sup"):
            sup.decompose()  # remove <sup></sup> tags
        for span in self.table.find_all("span"):
            span.decompose()  # remove <span></span> tags

        # remove other things maually
        f = str(self.table)

        # convert [table > list > dataframe]
        df = pd.DataFrame(pd.read_html(f)[0])

        # drop the unnecessary rows
        x = df.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 17])

        # get the datas only (list & convert each value to int / float)
        vals = [self.format_data(float(i.strip("%")))
                for i in list(x.iloc[:, 1])]

        # return the output
        return dict(zip(self.__keys, vals))

    # reconvert numbers with no decimal to int
    def format_data(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num
