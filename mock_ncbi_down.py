#!/usr/bin/env python3

import csv, random, os, argparse
from pathlib import Path

random.seed(1)

# Argumentos de entrada
parser = argparse.ArgumentParser()

parser.add_argument("-d","--directory_download", type=str, help="Diretório destido do download", required=True)
parser.add_argument("-c", "--categories", type=str, nargs='+', choices=["archaea", "bacteria", "fungi", "protozoa", "viral"], help="Categorias", required=True)

args = vars(parser.parse_args())

download_directory = str(Path(args["directory_download"]).resolve())
categories = args["categories"]

# in_file = "/home/gabrielasilva/Documents/projetos/mock_ncbi_down/assembly_summary_fungi.txt"
# download_directory = "/home/gabrielasilva/Documents/projetos/mock_ncbi_down/download"
# out_file = "/home/gabrielasilva/Documents/projetos/mock_ncbi_down/mock_downloaded.tsv"

def random_refseq (seq_number, database, category):
    # Download Assembly_summary
    try:
        os.mkdir(f"{download_directory}/{category}")
    except OSError as error:
        print(error)
    ftp_link = f"ftp://ftp.ncbi.nlm.nih.gov/genomes/{database}/{category}"
    os.system(f"wget -O {download_directory}/{category}/assembly_summary_{category}.txt -c {ftp_link}/assembly_summary.txt")
    in_file = f"{download_directory}/{category}/assembly_summary_{category}.txt"
    # Download Genomas
    out_file = f"{download_directory}/mock_downloaded.tsv"
    with open(in_file) as i_file, open(out_file,"w+") as o_file:
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
        csv_write.writeheader()
        for item in rand_choice:
            csv_write.writerow({
                "category": category,
                "assembly_accession": item[0],
                "organism_name": item[7],
                "infraspecific_name": item[8],
                "ftp_path": item[19],
            })
            genome_link = item[19] + "/" + item[19].split("/")[-1] + "_genomic.fna.gz"
            os.system(f"wget -P {download_directory}/{category} -c {genome_link} ")

for cat in categories:
    if cat == "archaea":
        random_refseq(2, "refseq", cat)
    elif cat == "bacteria":
        random_refseq(2, "refseq", cat)
    elif cat == "fungi":
        random_refseq(2, "refseq", cat)
    elif cat == "protozoa":
        random_refseq(2, "refseq", cat)
    elif cat == "viral":
        random_refseq(2, "refseq", cat)
    else:
        print(f"{cat} Categoria inválida")
