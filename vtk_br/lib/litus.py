import os
import requests

API_KEY = os.getenv("API_KEY")


def create_company(company_name):
    data = {
        "key": API_KEY,
        "company": company_name,
    }
    r = requests.post("https://vtk.be/api/br/add-company", data)
    if r.status_code == 200:
        return get_company_id(company_name)
    else:
        return None


def get_company_id(company_name):
    data = {"key": API_KEY, "company": company_name}
    r = requests.post("https://vtk.be/api/br/get-company-id", data)
    if r.status_code == 200:
        return r.json()["id"]
    else:
        return None


def create_contact(name, email, company_id):
    data = {
        "key": API_KEY,
        "user_name": name.lower().replace(" ", ""),
        "first_name": name,
        "last_name": "",
        "sex": "",
        "email": email,
        "company": company_id,
    }
    r = requests.post("https://vtk.be/api/br/add-user", data)
    if r.status_code == 200:
        return r.json()["id"]
    else:
        return r.content


def send_activation(user_id):
    data = {"key": API_KEY, "user": user_id}
    r = requests.post("https://vtk.be/api/br/send-activation", data)
    if r.status_code == 200:
        return True
    else:
        return False


def rename_company(company_id, new_company_name):
    data = {
        "key": API_KEY,
        "company_id": company_id,
        "new_name": new_company_name,
    }
    r = requests.post("https://vtk.be/api/br/edit-company-name", data)
    if r.status_code == 200:
        return True
    else:
        return False

    """
    Year must be formatted in: "xxxx-yyyy" format (eg. 2022-2023)

    """


def add_cv_book(company_name, year):
    data = {
        "key": API_KEY,
        "company": company_name,
        "year": year,
    }
    r = requests.post("https://vtk.be/api/br/add-cv-book", data)
    if r.status_code == 200:
        return True
    else:
        return False


def add_page_visible(company_name):
    data = {
        "key": API_KEY,
        "company": company_name,
    }
    r = requests.post("https://vtk.be/api/br/add-page-visible", data)
    if r.status_code == 200:
        return True
    else:
        return False
