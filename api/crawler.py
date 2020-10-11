from bs4 import BeautifulSoup
import requests

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

    async def get_all(self):
        # remove some unnecessary tags
        for sup in self.table.find_all("sup"):
            sup.decompose()  # remove <sup></sup> tags
        for span in self.table.find_all("span"):
            span.decompose()  # remove <span></span> tags

        vals = []

        # get all the values from the <td>
        for i in self.table.find_all("td"):
            vals.append(i.get_text())

        # get only the necessary values
        data = [self.format_data(float(i.strip("%").replace(",", ""))) for i in self.check_data(vals[9:16])]

        return dict(zip(self.__keys, data))

    # reconvert numbers with no decimal to int
    def format_data(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    # check the data for parsing
    def check_data(self, data):
        return [i.split(" ")[0] for i in data]