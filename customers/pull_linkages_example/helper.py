import json


def import_datasets():
    ds_list = '/Users/sophierand/RCDatasets/datasets.json'
    with open(ds_list) as json_file:
        datasets = json.load(json_file)
    return datasets


def import_customers():
    cust_list = '/Users/sophierand/RCCustomers/customers.json'
    with open(cust_list) as json_file:
        customers = json.load(json_file)
    return customers