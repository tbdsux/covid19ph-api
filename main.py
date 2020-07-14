from crawler import Crawler
from datetime import datetime
from typing import Optional
from enum import Enum
from fastapi import FastAPI, Header

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(api_router, prefix="/v1")


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


crawler = Crawler()
data = crawler.get_all()


@app.get("/")
async def root():
    return {"Info": "PH CoVid-19 Data", "message": "Hello Developer. Have a nice day!"}


summary = {
    "country": "Philippines",
    "country_code": "PH",
    "current_time": datetime.now(),
    "cases": data,
    "api_info": "This is just a simple API on the Summary of Cases of COVID-19 in the Philippines.",
}


@app.get("/cases/{case_name}")
async def read_case(case_name: str):
    if case_name == DataModel.confirmed:
        return {
            "Info": "PH CoVid-19 Data",
            "Confirmed_Cases": {"total": data["confirmed"]},
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.active:
        return {
            "Info": "PH CoVid-19 Data",
            "Active_Cases": {"total": data["active"]},
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.suspected:
        return {
            "Info": "PH CoVid-19 Data",
            "Suspected_Cases": {"total": data["suspected"]},
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.severe:
        return {
            "Info": "PH CoVid-19 Data",
            "Severe_Cases": {"total": data["severe"]},
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.critical:
        return {
            "Info": "PH CoVid-19 Data",
            "Critical_Cases": {"total": data["critical"]},
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.recovered:
        return {
            "Info": "PH CoVid-19 Data",
            "Recovered_Cases": {"total": data["recovered"]},
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.deaths:
        return {
            "Info": "PH CoVid-19 Data",
            "Deaths_Cases": {"total": data["deaths"]},
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.fatality_rate:
        return {
            "Info": "PH CoVid-19 Data",
            "Fatality_Rate": {"total": data["fatality_rate"]},
            "current_time": datetime.now(),
        }

    elif case_name == DataModel.total:
        return summary

    return {"Info": "No Data Found"}


@app.get("/api")
async def api_info():
    return {
        "api_info": "This is just a simple API on the Summary of Cases of COVID-19 in the Philippines."
    }


@app.get("/api/headers")
async def header(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
