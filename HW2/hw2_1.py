# -*- coding: utf-8 -*-

import requests, sys, json, re

def get_ensembl(ids: list):
    url = "https://rest.ensembl.org/lookup/id"
    https_args = {"Content-Type" : "application/json", "Accept" : "application/json"}
    json_ids = json.dumps({"ids": ids})
    https_function = requests.post(url, headers=https_args, data=json_ids)
    return https_function

def parse_response_ensembl(response: dict):
    resp = response.json()
    output = {}
    for val in resp:
        display_name = resp[val]['display_name']
        species = resp[val]['species']
        description = resp[val]['description']
        output[val] = {'gene':display_name, 'organism':species, 'geneInfo':description}
    return output

def get_uniprot(ids: list):
    accessions = ','.join(ids)
    url = "https://rest.uniprot.org/uniprotkb/accessions"
    http_function = requests.get
    http_args = {'params': {'accessions': accessions}}
    return http_function(url, **http_args)

def parse_response_uniprot(resp: dict):
    resp = resp.json()
    resp = resp["results"]
    output = {}
    for val in resp:
        acc = val['primaryAccession']
        species = val['organism']['scientificName']
        gene = val['genes'][0]['geneName']['value']
        seq = val['sequence']['length']
        output[acc] = {'organism':species, 'gene':gene, 'lenght':seq, 'type': 'protein'}
    return output

def process_ids(db_ids):

    uniprot_pattern = r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}"
    ensembl_pattern = r"^ENS(|[A-Z]{3,4})(E|FM|G|GT|P|R|T)[0-9]{11}"
    id_0 = db_ids[0]

    if re.match(uniprot_pattern, id_0):
        response = get_uniprot(db_ids)
        output = parse_response_uniprot(response)

    elif re.match(ensembl_pattern, id_0):
        response = get_ensembl(db_ids)
        output = parse_response_ensembl(response)

    else:
        output = "Error: input pattern doesn't match uniport or ensembl pattern"

    return output


id_list_1 = ["ENSMUSG00000041147", "ENSG00000139618"]
id_list_2 = ['P11473', 'Q91XI3']
print(process_ids(id_list_1))
print(process_ids(id_list_2))

