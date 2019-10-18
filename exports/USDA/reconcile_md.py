def rec_doi(pub_md):
    doi_list = []
    for k,v in pub_md.items():
        if k == 'original':
            try:
                orig_doi = pub_md['original']['doi']
                doi_list.append(orig_doi)
            except:
                pass
        if k == 'dimensions':
            try:
                dimensions_doi = pub_md['dimensions']['doi']
                doi_list.append(dimensions_doi)
            except:
                pass
        if k == 'europepmc':
            try:
                epmc_doi = pub_md['europepmc']['doi']
                doi_list.append(epmc_doi)
            except:
                pass
    doi_list = list(set(doi_list))
    return doi_list