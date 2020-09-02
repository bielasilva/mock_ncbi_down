#!/usr/bin/env python3

import csv, random, os, argparse
from pathlib import Path

random.seed(1)

# Entry arguments
parser = argparse.ArgumentParser()

parser.add_argument("-d","--directory_download", type=str, help="Directory to save downloads", required=True)
parser.add_argument("-c", "--databases", type=str, nargs='+', choices=["archaea", "bacteria", "fungi", "protozoa", "viral"], help="Databases", required=True)

args = vars(parser.parse_args())

download_directory = str(Path(args["directory_download"]).resolve())
databases = sorted(args["databases"])

# in_file = "/home/gabrielasilva/Documents/projetos/mock_ncbi_down/assembly_summary_fungi.txt"
# download_directory = "/home/gabrielasilva/Documents/projetos/mock_ncbi_down/download"
# out_file = "/home/gabrielasilva/Documents/projetos/mock_ncbi_down/mock_downloaded.tsv"
first = True

def random_refseq (seq_number, database):
    # Assembly_summary Download
    try:
        os.makedirs(f"{download_directory}/{database}/refseq")
    except FileExistsError:
        pass
    ftp_link = f"ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/{database}"
    os.system(f"wget -O {download_directory}/{database}/refseq/assembly_summary_refseq_{database}.txt -c {ftp_link}/assembly_summary.txt")
    in_file = f"{download_directory}/{database}/refseq/assembly_summary_refseq_{database}.txt"
    # Genomes Download
    out_file = f"{download_directory}/mock_downloaded.tsv"
    with open(in_file) as i_file, open(out_file,"a+") as o_file:
        csv_read = csv.reader(i_file, delimiter="\t")
        next(csv_read)
        complete_entries = []
        for row in csv_read:
            if row[11] == "Complete Genome":
                complete_entries.append(row)
        rand_choice = random.choices(complete_entries, k=seq_number)
        downloaded = []
        header = ["category", "assembly_accession", "organism_name", "infraspecific_name", "ftp_path"]
        csv_write = csv.DictWriter(o_file, fieldnames=header, delimiter="\t")
        global first
        if first:
            csv_write.writeheader()
            first = False
        for item in rand_choice:
            csv_write.writerow({
                "category": database,
                "assembly_accession": item[0],
                "organism_name": item[7],
                "infraspecific_name": item[8],
                "ftp_path": item[19],
            })
            genome_link = item[19] + "/" + item[19].split("/")[-1] + "_genomic.fna.gz"
            os.system(f"wget -P {download_directory}/{database}/refseq/ -c {genome_link} ")

def genbank_download(seq_number, database, category):
    try:
        os.makedirs(f"{download_directory}/{category}/genbank")
    except FileExistsError:
        pass
    
for db in databases:
    if db == "archaea":
        random_refseq(2, db)
    elif db == "bacteria":
        random_refseq(2, db)
    elif db == "fungi":
        random_refseq(2, db)
    elif db == "protozoa":
        random_refseq(2, db)
    elif db == "viral":
        random_refseq(2, db)
    else:
        print(f"{db} Categoria inválida")
