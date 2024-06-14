! pip install biopython
! pip install -q condacolab
import condacolab
condacolab.install()
! conda install -c bioconda seqkit

import requests, sys, json, re, subprocess
from Bio import SeqIO


# Function for seqkit call

def seqkit_call(path):
    seqkit = subprocess.run(("seqkit", "stats", path, "-a"), capture_output=True, text=True)
    if seqkit.stdout:
        seqkit_out = seqkit.stdout.strip().split('\n')
        file_type = seqkit_out[1].split()[2]
        prop_names = seqkit_out[0].split()[1:]
        prop_vals = seqkit_out[1].split()[1:]
        seq_result = dict(zip(prop_names, prop_vals))
        return seq_result, file_type
    else:
        return seqkit.stderr, None


# Biopython parser

def biopython_parser(path, file_type):
    sequences = SeqIO.parse(path, 'fasta')
    ids = []
    info = []
    for sequence in sequences:
        seq = sequence.seq
        # print(seq)
        desc = sequence.description
        # print(desc)
        info.append([desc, seq])
        if file_type == "DNA":
            id = re.search(r"^ENS(|[A-Z]{3,4})(E|FM|G|GT|P|R|T)[0-9]{11}", desc)
            ids.append(id.group())
        elif file_type == "Protein":
                id = re.search(r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}", desc)
                ids.append(id.group())
    return info, ids


# Modified utility functions from HW2_1

def get_ensembl(ids: list):
    url = "https://rest.ensembl.org/lookup/id"
    https_args = {"Content-Type" : "application/json", "Accept" : "application/json"}
    json_ids = json.dumps({"ids": ids})
    https_function = requests.post(url, headers=https_args, data=json_ids)
    return https_function

def parse_response_ensembl(response: dict):
    resp = response.json()
    return resp

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

def process_ids(ids, file_type):
    if file_type == "DNA":
        response = get_ensembl(ids)
        output = parse_response_ensembl(response)
        database = 'ENSEMBL'
    elif file_type == "Protein":
        response = get_uniprot(ids)
        output = parse_response_uniprot(response)
        database = "Uniprot"
    return output, database


# Function for final output

def results_print(fasta_file):
    print(f'_____________ File "{fasta_file}"_____________\n')
    seqkit_output, file_type = seqkit_call(fasta_file)
    if file_type:
        info, ids = biopython_parser(fasta_file, file_type)
        output, database = process_ids(ids, file_type)
        print(f"Seqkit stats:\n{json.dumps(seqkit_output, indent=2)}\n\n"
              f"File type: {file_type}\n\n\n"
              f"Sequences information\n")
        for sublist in info:
            print(f"Description: {sublist[0]}")
            print(f"Full sequence: {sublist[1]}")
            print("----")
        print(f"Info from {database} for all sequences:\n{json.dumps(output, indent=2)}\n\n")
    else:
        print(f"{seqkit_output}")


# Testing the script

[results_print(fasta_file) for fasta_file in ["hw_file1.fasta", "hw_file2.fasta", "hw_file3.fasta"]]

ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIP61Ns7xN7H6y86JEaHD0hbLNBg0v+xV2mP5GryJr5Sb admd@omk-latitude-3490

