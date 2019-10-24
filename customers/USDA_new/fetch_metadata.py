
import json
import networkx as nx
import os
import rdflib
import sys
import tempfile


# TTL_PREAMBLE = """
# @prefix cito:	<http://purl.org/spar/cito/> .
# @prefix dct:	<http://purl.org/dc/terms/> .
# @prefix foaf:	<http://xmlns.com/foaf/0.1/> .
# @prefix rdf:	<http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
# @prefix xsd:	<http://www.w3.org/2001/XMLSchema#> .
# """


TTL_PREAMBLE  = """
@base <https://github.com/Coleridge-Initiative/adrf-onto/wiki/Vocabulary> .
@prefix cito:<http://purl.org/spar/cito/> .
@prefix dct:<http://purl.org/dc/terms/> .
@prefix foaf:<http://xmlns.com/foaf/0.1/> .
@prefix rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd:<http://www.w3.org/2001/XMLSchema#> .
"""
def wrap_token (t):
    if t.startswith("http"):
        return "<{}>".format(t)
    else:
        return "\"{}\"".format(t)


def write_triple (f, s, p, o):
    line = "{} {} {} .\n".format(wrap_token(s), wrap_token(p), wrap_token(o))
    f.write(line.encode("utf-8"))


def get_metadata(file_name, dataset_id):
    filename = file_name
    term = dataset_id

    ## load the JSON-LD context
    with open("vocab.json", "r") as f:
        context = json.load(f)

    ## write TTL results to a temporary file, for JSON-LD conversion later
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(TTL_PREAMBLE.encode("utf-8"))

    # load the graph, collected triples related to the search term
    graph = rdflib.Graph().parse(filename, format="n3")

    for s, p, o in graph:
        if s.endswith(term):
            write_triple(f, s, p, o)

        elif o.endswith(term):
            write_triple(f, s, p, o)

    f.close()

    # serialize the graph as JSON-LD
    graph = rdflib.Graph().parse(f.name, format="n3")
    os.unlink(f.name)

    response = graph.serialize(format="json-ld", context=context, indent=None)
    return response
