#!/usr/bin/env python3
import csv, random, os, argparse
from pathlib import Path

# random.seed(1)

# Entry arguments
parser = argparse.ArgumentParser()

parser.add_argument("-d","--directory_download", type=str, help="Directory to save downloads", required=True)
parser.add_argument("-c", "--databases", type=str, nargs='+', choices=["archaea", "bacteria", "fungi", "protozoa", "viral"], help="Databases", required=True)

args = vars(parser.parse_args())

download_directory = str(Path(args["directory_download"]).resolve())
databases = sorted(args["databases"])

# in_file = "/home/gabrielasilva/Documents/projetos/mock_ncbi_down/assembly_summary_fungi.txt"
# download_directory = "/home/gabrielasilva/Documents/projetos/mock_ncbi_down/"
first = True

def refseq_download (seq_number, database):
    # Assembly_summary Download
    try:
        os.makedirs(f"{download_directory}/{database}/refseq")
    except FileExistsError:
        pass
    ftp_link = f"ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/{database}"
    os.system(f"wget -O {download_directory}/{database}/refseq/assembly_summary_refseq_{database}.txt -c {ftp_link}/assembly_summary.txt")
    in_file = f"{download_directory}/{database}/refseq/assembly_summary_refseq_{database}.txt"
    # Genomes Download
    out_file = f"{download_directory}/mock_download.tsv"
    with open(in_file) as i_file, open(out_file,"a+") as o_file:
        refseq_read = csv.reader(i_file, delimiter="\t")
        next(refseq_read)
        refseq_entries = []
        for row in refseq_read:
            if row[11] == "Complete Genome":
                refseq_entries.append(row)
        random_choices = []
        # global species
        global species
        species = []
        while len(random_choices) != seq_number:
            choice = random.choices(refseq_entries)[0]
            specie = choice[7].split(" ") # Change to 1 in case of different gender
            specie = " ".join(specie[0:2])
            if specie not in species:
                random_choices.append(choice)
                species.append(specie)
        downloaded = []
        header = ["category", "assembly_accession", "organism_name", "infraspecific_name", "ftp_path", "genome_path", "excluded_from_refseq"]
        refseq_write = csv.DictWriter(o_file, fieldnames=header, delimiter="\t")
        global first
        if first:
            refseq_write.writeheader()
            first = False
        for entry in random_choices:
            genome_link = entry[19] + "/" + entry[19].split("/")[-1] + "_genomic.fna.gz"
            refseq_write.writerow({
                "category": database,
                "assembly_accession": entry[0],
                "organism_name": entry[7],
                "infraspecific_name": entry[8],
                "ftp_path": entry[19],
                "genome_path": genome_link,
            })
            os.system(f"wget -P {download_directory}/{database}/refseq/ -c {genome_link} ")

def genbank_download(seq_number, database):
    try:
        os.makedirs(f"{download_directory}/{database}/genbank")
    except FileExistsError:
        pass
    ftp_link = f"ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/{database}"
    os.system(f"wget -O {download_directory}/{database}/genbank/assembly_summary_genbank_{database}.txt -c {ftp_link}/assembly_summary.txt")
    genbank_file = f"{download_directory}/{database}/genbank/assembly_summary_genbank_{database}.txt"
    # Create Download file
    out_file = f"{download_directory}/mock_download.tsv"
    with open(genbank_file) as gb_file, open(out_file, "a+") as o_file:
        gb_read = csv.reader(gb_file, delimiter="\t")
        next(gb_read)
        file_header = next(gb_read)
        gb_entries = []
        global species
        for row in gb_read:
            if row[11] == "Complete Genome" and row[17] == "na" and row[20] == "":
                gb_entries.append(row)
        random_choices = []
        while len(random_choices) != seq_number:
            choice = random.choices(gb_entries)[0]
            specie = choice[7].split(" ")
            specie = " ".join(specie[0:2]) # Change to 1 in case of different gender
            if specie not in species:
                random_choices.append(choice)
                species.append(specie)
        header = ["category", "assembly_accession", "organism_name", "infraspecific_name", "ftp_path", "genome_path", "excluded_from_refseq"]
        gb_write = csv.DictWriter(o_file, fieldnames=header, delimiter="\t")
        global first
        if first:
            gb_write.writeheader()
            first = False
        for entry in random_choices:
            genome_link = entry[19] + "/" + entry[19].split("/")[-1] + "_genomic.fna.gz"
            gb_write.writerow({
                "category": database,
                "assembly_accession": entry[0],
                "organism_name": entry[7],
                "infraspecific_name": entry[8],
                "ftp_path": entry[19],
                "genome_path": genome_link,
                "excluded_from_refseq": entry[20]
            })
            os.system(f"wget -P {download_directory}/{database}/refseq/ -c {genome_link} ")

for db in databases:
    if db == "archaea":
        refseq_download(15, db)
        genbank_download(5, db)
    elif db == "bacteria":
        refseq_download(15, db)
        genbank_download(5, db)
    elif db == "fungi":
        refseq_download(5, db)
        genbank_download(5, db)
    elif db == "protozoa":
        refseq_download(2, db)
        genbank_download(2, db)
    elif db == "viral":
        refseq_download(10, db)
        genbank_download(10, db)
    else:
        print(f"{db} Categoria inválida")
