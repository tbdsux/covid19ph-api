from .crawler import Crawler
from datetime import datetime
import pytz
from enum import Enum
from fastapi import FastAPI, Header, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# import the database handler
from .db import DB

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class DataModel(str, Enum):
    confirmed = "confirmed"
    active = "active"
    suspected = "suspected"
    severe = "severe"
    critical = "critical"
    recovered = "recovered"
    deaths = "deaths"
    fatality_rate = "fatality_rate"
    total = "all"


# crawl the website: 
async def get_data():
    crawler = Crawler()
    return await crawler.get_all()


@app.get("/")
async def root(request: Request):
    data = await DB.get_data()
    return templates.TemplateResponse("index.html", {"request": request, "data": data["data"], "datetime": data["crawl_time"]})


@app.get("/api/cases/{case_name}")
async def read_case(case_name: str):
    data = await DB.get_data()
    if case_name == DataModel.confirmed:
        return {
            "Info": "PH CoVid-19 Data",
            "Confirmed_Cases": {"total": data["data"]["confirmed"]},
            "as_of": data["crawl_time"],
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.active:
        return {
            "Info": "PH CoVid-19 Data",
            "Active_Cases": {"total": data["data"]["active"]},
            "as_of": data["crawl_time"],
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.suspected:
        return {
            "Info": "PH CoVid-19 Data",
            "Suspected_Cases": {"total": data["data"]["suspected"]},
            "as_of": data["crawl_time"],
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.severe:
        return {
            "Info": "PH CoVid-19 Data",
            "Severe_Cases": {"total": data["data"]["severe"]},
            "as_of": data["crawl_time"],
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.critical:
        return {
            "Info": "PH CoVid-19 Data",
            "Critical_Cases": {"total": data["data"]["critical"]},
            "as_of": data["crawl_time"],
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.recovered:
        return {
            "Info": "PH CoVid-19 Data",
            "Recovered_Cases": {"total": data["data"]["recovered"]},
            "as_of": data["crawl_time"],
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.deaths:
        return {
            "Info": "PH CoVid-19 Data",
            "Deaths_Cases": {"total": data["data"]["deaths"]},
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.fatality_rate:
        return {
            "Info": "PH CoVid-19 Data",
            "Fatality_Rate": {"total": data["data"]["fatality_rate"]},
            "as_of": data["crawl_time"],
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.total:
        return {
            "country": "Philippines",
            "country_code": "PH",
            "current_time": datetime.now(),
            "as_of": data["crawl_time"],
            "cases": data["data"],
            "api_info": "This is just a simple API on the Summary of Cases of COVID-19 in the Philippines.",
        }

    return {"Info": "No Data Found"}


@app.get("/api")
async def api_info():
    return {
        "api_info": "This is just a simple API on the Summary of Cases of COVID-19 in the Philippines."
    }

@app.get("/crawler")
async def crawl_data():
    data = await get_data()

    # initialize the content to be stored in the database
    content = {}
    content['data'] = data
    content['crawl_time'] = datetime.now(tz=pytz.timezone('Asia/Manila'))

    store = await DB.store_data(content)

    # if the return is true, return a success message
    if store:
        return {"Crawl Info": "The crawler was successful and the was stored to the database successfully."}
    
    # this is the default return message
    return {"Crawl Info": "There was a problem with storing the data to the database!"}