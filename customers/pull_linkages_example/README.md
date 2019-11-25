### Prerequisites:

* Python 3.x
* richcontext-scholapi
* Beautiful Soup
* Dimensions CLI
* Requests
* Selenium

To access the RichContext API library, install from 
[repo](https://github.com/NYU-CI/RCApi)
or [PyPi](https://pypi.org/project/richcontext-scholapi/) with 
`pip install richcontext.scholapi` 

`gen_datasets_list.ipynb` creates `datasets_list.json`, a subset of [`datasets.json`](https://github.com/NYU-CI/RCDatasets/blob/master/datasets.json) for a specific client or partner of Coleridge. 

`gen_linkages.ipynb` generates possible dataset-publications linkages using the Dimensions API and exports the linkages to subfolders within [RichContextMetadata](https://github.com/NYU-CI/RichContextMetadata/tree/master/metadata).