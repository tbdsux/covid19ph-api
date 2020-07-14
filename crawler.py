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
            "suspected",
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
        str_table = str(self.table)

        f = str_table.replace(
            """<tr><th colspan="2" style="text-align:center;font-size:125%;font-weight:bold;background:#FFCCCB">COVID-19 pandemic in the Philippines</th></tr><tr><td colspan="2" style="text-align:center;border-bottom:#aaa 1px solid;"><a class="image" href="/wiki/File:COVID-19_pandemic_cases_in_the_Philippines.svg"><img alt="COVID-19 pandemic cases in the Philippines.svg" data-file-height="6105" data-file-width="4200" decoding="async" height="320" src="//upload.wikimedia.org/wikipedia/commons/thumb/8/84/COVID-19_pandemic_cases_in_the_Philippines.svg/220px-COVID-19_pandemic_cases_in_the_Philippines.svg.png" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/8/84/COVID-19_pandemic_cases_in_the_Philippines.svg/330px-COVID-19_pandemic_cases_in_the_Philippines.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/8/84/COVID-19_pandemic_cases_in_the_Philippines.svg/440px-COVID-19_pandemic_cases_in_the_Philippines.svg.png 2x" width="220"/></a><div style="text-align:left;"><div class="center" style="width:auto; margin-left:auto; margin-right:auto;">Map of provinces (including Metro Manila) with confirmed COVID-19 cases (as of July 4)</div>
<div class="legend" style="-webkit-column-break-inside: avoid;page-break-inside: avoid;break-inside: avoid-column"> ≥5000 confirmed</div>
<div class="legend" style="-webkit-column-break-inside: avoid;page-break-inside: avoid;break-inside: avoid-column"> 1000–4999 confirmed</div>
<div class="legend" style="-webkit-column-break-inside: avoid;page-break-inside: avoid;break-inside: avoid-column"> 500–999 confirmed</div>
<div class="legend" style="-webkit-column-break-inside: avoid;page-break-inside: avoid;break-inside: avoid-column"> 100–499 confirmed</div>
<div class="legend" style="-webkit-column-break-inside: avoid;page-break-inside: avoid;break-inside: avoid-column"> 10–99 confirmed</div>
<div class="legend" style="-webkit-column-break-inside: avoid;page-break-inside: avoid;break-inside: avoid-column"> 1–9 confirmed</div></div>
</td></tr><tr><td colspan="2" style="text-align:center;border-bottom:#aaa 1px solid;"><a class="image" href="/wiki/File:COVID-19_pandemic_cases_in_the_Philippines_(primary_LGUs_breakdown).svg"><img alt="COVID-19 pandemic cases in the Philippines (primary LGUs breakdown).svg" data-file-height="6105" data-file-width="4200" decoding="async" height="320" src="//upload.wikimedia.org/wikipedia/commons/thumb/8/8d/COVID-19_pandemic_cases_in_the_Philippines_%28primary_LGUs_breakdown%29.svg/220px-COVID-19_pandemic_cases_in_the_Philippines_%28primary_LGUs_breakdown%29.svg.png" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/8/8d/COVID-19_pandemic_cases_in_the_Philippines_%28primary_LGUs_breakdown%29.svg/330px-COVID-19_pandemic_cases_in_the_Philippines_%28primary_LGUs_breakdown%29.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/8/8d/COVID-19_pandemic_cases_in_the_Philippines_%28primary_LGUs_breakdown%29.svg/440px-COVID-19_pandemic_cases_in_the_Philippines_%28primary_LGUs_breakdown%29.svg.png 2x" width="220"/></a><div style="text-align:left;">Map of provinces (including independent cities) with confirmed COVID-19 cases (as of July 4)
<div class="legend" style="-webkit-column-break-inside: avoid;page-break-inside: avoid;break-inside: avoid-column"> ≥1000 confirmed</div>
<div class="legend" style="-webkit-column-break-inside: avoid;page-break-inside: avoid;break-inside: avoid-column"> 500–999 confirmed</div>
<div class="legend" style="-webkit-column-break-inside: avoid;page-break-inside: avoid;break-inside: avoid-column"> 100–499 confirmed</div>
<div class="legend" style="-webkit-column-break-inside: avoid;page-break-inside: avoid;break-inside: avoid-column"> 10–99 confirmed</div>
<div class="legend" style="-webkit-column-break-inside: avoid;page-break-inside: avoid;break-inside: avoid-column"> 1–9 confirmed</div></div>
</td></tr><tr><th scope="row">Disease</th><td><a class="mw-redirect" href="/wiki/COVID-19" title="COVID-19">COVID-19</a></td></tr><tr><th scope="row">Virus strain</th><td><a class="mw-redirect" href="/wiki/SARS-CoV-2" title="SARS-CoV-2">SARS-CoV-2</a></td></tr><tr><th scope="row">Location</th><td>Philippines</td></tr><tr><th scope="row">First outbreak</th><td><a href="/wiki/Wuhan" title="Wuhan">Wuhan</a>, Hubei, China</td></tr><tr><th scope="row"><a href="/wiki/Index_case" title="Index case">Index case</a></th><td><a href="/wiki/Manila" title="Manila">Manila</a></td></tr><tr><th scope="row">Arrival date</th><td>January 30, 2020<br/>(5 months and 2 weeks)</td></tr>""",
            "",
        ).replace(
            '<tr><th colspan="2" style="text-align:center;background:#eee;">Government website</th></tr><tr><td colspan="2" style="text-align:center"><div class="plainlist"><ul><li></li><li></li></ul></div></td></tr><tr><td colspan="2" style="text-align:center;text-align:left; border-top:#aaa 1px solid;"><i>Suspected cases have not been confirmed as being due to this strain by laboratory tests, although some other strains may have been ruled out.</i></td></tr>',
            "",
        )

        # convert [table > list > dataframe]
        df = pd.DataFrame(pd.read_html(f)[0])

        # get the datas only (list & convert each value to int / float)
        vals = [self.format_data(float(i.strip("%"))) for i in list(df.iloc[:, 1])]

        # return the output
        return dict(zip(self.__keys, vals))

    # reconvert numbers with no decimal to int
    def format_data(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num
