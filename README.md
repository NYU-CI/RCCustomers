# RCCustomers

This repo provides `customers.json`, metadata on customers - for our publications model in our Rich Context Knowledge Graph. Metadata links publications to datasets from [`datasets.json`](https://github.com/NYU-CI/RCDatasets)

The dataset linkage (represented by `related_dataset` field - see more below) originates from our work with clients and partners who use our Data Stewardship Platform or our ADRF Computing environment.

### Required Fields
At a minimum, each record in the `customers.json` file must have
  * `name` -- name of the customer, e.g. the U.S. Department of Agriculture
  * `alt_name` -- list of alternate name(s) for customer, e.g. USDA.
  * `dataset` -- list of one or more `id` from [`datasets.json`](https://github.com/NYU-CI/RCDatasets/datasets.json)
  

### Additional fields
* `type` - could be 'governmentt agency', 'private client'

### Example
See `customers/pull_linkages_example` for example on how to generate publication-dataset linkages.
