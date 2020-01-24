#### parsing functions
from collections import OrderedDict
from richcontext import scholapi as rc_scholapi
import sys
import datetime
import json
import re

def get_xml_node_value (root, name):
        """
        return the named value from an XML node, if it exists
        """
        node = root.find(name)

        if not node:
            return None
        elif len(node.text) < 1:
            return None
        else:
            return node.text.strip()

def parse_oa (results):
    meta_list = []
    for result in results:
        if result.find("instancetype")["classname"] in ["Other literature type", "Article"]:
            meta = OrderedDict()
            result_title = get_xml_node_value(result, "title")
            meta["title"] = result_title
            if get_xml_node_value(result, "journal"):
                meta["journal"] = get_xml_node_value(result, "journal")
            meta["url"] = get_xml_node_value(result, "url")
            meta["open"] = len(result.find_all("bestaccessright",  {"classid": "OPEN"})) > 0
            meta["api"] = "openaire"
            meta_list.append(meta)
        else:
            pass
    if len(meta_list) > 0:
        return meta_list
    elif meta_list == []:
        return None

        
def parse_dimensions(results):
    meta_list = []
    for result in results:
        if result["type"] in ["article","preprint"]:
            meta = OrderedDict()
            meta["title"] = result["title"]
            meta["api"] = "dimensions"
            try:
                meta["journal"] = result["journal"]["title"]
            except:
                pass
            try:
                meta["doi"] = result["doi"]
            except:
                pass
            meta_list.append(meta)
        else:
            pass
    if len(meta_list) > 0:
        return meta_list
    elif meta_list == []:
        return None
        
def parse_pubmed(result):
    article_meta = result["MedlineCitation"]["Article"]
    meta = OrderedDict()
    meta["title"] = article_meta["ArticleTitle"]
    meta["journal"] = article_meta["Journal"]["Title"]
    meta["api"] = "pubmed"
    try:
        pid_list = article_meta["ELocationID"]    
        if isinstance(pid_list,list):
                doi_test = [d["#text"] for d in pid_list if d["@EIdType"] == "doi"]
                if len(doi_test) > 0:
                    meta["doi"] = doi_test[0]
        if isinstance(pid_list,dict):
            if pid_list["@EIdType"] == "doi":
                meta["doi"] = pid_list["#text"]
    except:
        pass
    return meta



def main(search_term,limit,dataset_id):
    schol = rc_scholapi.ScholInfraAPI(config_file="rc.cfg", logger=None)
    api_meta_list = []
    for api in [schol.openaire, schol.dimensions]:
        results = api.full_text_search(search_term = search_term,limit = limit)
        if api == schol.openaire:
            meta = parse_oa(results)
        if api == schol.dimensions:
            meta = parse_dimensions(results)
        if meta:
            [m.update({"search_term":search_term,"datasets":dataset_id}) for m in meta]
            api_meta_list.extend(meta)
        # if dataset_id:
        #     [m.update({"datasets":dataset_id}) for m in meta]
    if len(api_meta_list) > 0:
        return api_meta_list
    if api_meta_list == []:
        print('No results for that search term')
        return None
    
def export(meta_list):
    file_name = "{}_{}_linkages.json".format(datetime.date.today().strftime("%Y%m%d"),re.sub(" ","_",search_term))
    print('Writing {} results from 2 APIs to {}'.format(len(meta_list),file_name))
    with open(file_name, 'w') as outfile:
        json.dump(meta_list, outfile,indent = 2)
    
    
if __name__ == "__main__":
    """
    This script takes a search term and runs a full text search through various
    apis and writes the json results to a given location
    :1st param: search_term
    :2nd param: limit (# of results). defaults to 20
    :3rd param: associated dataset id
    :return: None - prints message if there were no results for a given search term.
    Example with limit python federated_fulltext_searches.py NHANES 10 dataset-123
    Example without limit python federated_fulltext_searches.py NHANES dataset-123
    """
    # if len(sys.argv) in [2,3]:
    dataset_id = [d for d in sys.argv if 'dataset-' in d]
    if dataset_id == []:
        raise ValueError("Please provide an associated dataset-id.")
    if len(dataset_id) > 0 and len(sys.argv) == 3:
        search_term = sys.argv[1]
        limit = 20
    if len(dataset_id) > 0 and len(sys.argv) == 4:
        search_term = sys.argv[1]
        limit = int(sys.argv[2])
    print('\nRunning full text searches for\nSearch Term: {}\nAssociated dataset: {}\nResult Limit:{}\n'.format(search_term,dataset_id,limit))
    search_results = main(search_term = search_term, limit = limit, dataset_id = dataset_id)
    export(search_results)