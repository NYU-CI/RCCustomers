import os
import sys
import json


def read_datasets():
    dataset_path = "/Users/sophierand/RCDatasets/datasets.json"
    with open(dataset_path) as json_file:
        datasets = json.load(json_file)
    return datasets

def fetch_datasets(datasets,customer_name):
    cust_path = "/Users/sophierand/RCCustomers/customers.json"
    with open(cust_path) as json_file:
        customers = json.load(json_file)
    cust_ids = [c["datasets"] for c in customers if c['name'] == customer_name][0]
    cust_datasets = [d for d in datasets if d['id'] in cust_ids]
    dataset_path = "/Users/sophierand/RCCustomers/{}_datasets.json".format(customer_name)
    print('writing dataset list for customer {} to {}'.format(customer_name,dataset_path))
    with open(dataset_path, 'w') as outfile:
        json.dump(cust_datasets, outfile, indent=2)
    return cust_datasets
    

def read_partitions():
    pub_list = []
    partitions = [os.path.join('/Users/sophierand/RCPublications/partitions',f) for f in os.listdir('/Users/sophierand/RCPublications/partitions') if f.endswith('.json')]
    for p in partitions:
        with open(p) as json_file:
            partition = json.load(json_file)
            pub_list.extend(partition)
    return pub_list

def fetch_publications(pub_list,cust_datasets):
    customer_partitions = []
    cust_dataset_ids = [d["id"] for d in cust_datasets]
    for p in pub_list:
        try:
            used_dataset = list(set(p["datasets"]) & set(cust_dataset_ids))
            if len(used_dataset) > 0:
                customer_partitions.append(p)
        except:
            pass
    publication_path = "/Users/sophierand/RCCustomers/{}_publications.json".format(customer_name)
    print('writing publication list with {} publications for customer {} to {}'.format(len(customer_partitions),customer_name,publication_path))
    with open(publication_path, 'w') as outfile:
        json.dump(customer_partitions, outfile, indent=2)

if __name__ == "__main__":
    """
    exports dataset and pub list for a specific customer
    """
    
    if len(sys.argv) == 2:
        customer_name = sys.argv[1]
        datasets = read_datasets()
        cust_datasets = fetch_datasets(datasets = datasets, customer_name = customer_name)
        publications = read_partitions()
        fetch_publications(pub_list = publications,cust_datasets = cust_datasets)
    else:
        raise ValueError("Wrong number of arguments passed in.")
