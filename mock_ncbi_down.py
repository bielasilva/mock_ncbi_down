#!/usr/bin/env python3
import csv, random, os, argparse
from pathlib import Path

# random.seed(1)

# Entry arguments
parser = argparse.ArgumentParser()

parser.add_argument("-d", "--directory_download",
                    type=str,
                    help="Directory to save downloads", required=True)
parser.add_argument("-r", "--refseq_only",
                    action='store_true',
                    help="Directory to save downloads")
parser.add_argument("-c", "--databases",
                    type=str,
                    nargs='+',
                    choices=["archaea", "bacteria", "fungi", "protozoa", "viral"],
                    help="Databases", required=True)

args = vars(parser.parse_args())

download_directory = str(Path(args["directory_download"]).resolve())
databases = sorted(args["databases"])
refseq_only = args["refseq_only"]

first = True
def silva(): #! NOT IMPLEMENTED
    silva_file = "/home/gabrielasilva/Downloads/SSU/SILVA_138_SSU_tax_silva.fasta"
    global silva_species
    silva_species = []
    with open(silva_file) as inf:
        for row in inf:
            if row.startswith(">"):
                silva_specie = row.split(";")[-1].split(" ")
                silva_specie = " ".join(silva_specie[0:2]).replace("\n", "")
                silva_species.append(silva_specie)

def refseq_download(seq_number, database):
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
        global refseq_species
        refseq_species = []
        # Filter complete genomes
        for row in refseq_read:
            if row[11] == "Complete Genome":
                refseq_entries.append(row)
                refseq_specie = row[7].split(" ")
                refseq_specie = " ".join(refseq_specie[0:2])
                if refseq_specie not in refseq_species:
                    refseq_species.append(refseq_specie)
        # # Randomly chooses the genomes
        random_choices = []
        global species
        species = []
        while len(random_choices) != seq_number:
            choice = random.choices(refseq_entries)[0]
            specie = choice[7].split(" ") # Change to 1 in case of different gender
            specie = " ".join(specie[0:2])
            if specie not in species:
                random_choices.append(choice)
                species.append(specie)
        # Downloads the genomes and crates the tsv file
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
        # Filter genomes
        gb_entries = []
        for row in gb_read:
            if row[11] == "Complete Genome" and row[17] == "na" and row[20] == "":
                gb_entries.append(row)
        # Randomly chooses the genomes
        random_choices = []
        global species
        while len(random_choices) != seq_number:
            choice = random.choices(gb_entries)[0]
            specie = choice[7].split(" ")
            specie = " ".join(specie[0:2]) # Change to 1 in case of different gender
            if specie not in species and specie not in refseq_species:
                random_choices.append(choice)
                species.append(specie)
        # Downloads the genomes and appends the tsv file
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
            os.system(f"wget -P {download_directory}/{database}/genbank/ -c {genome_link} ")

for db in databases:
    if db == "archaea":
        refseq_download(15, db)
        if not refseq_only:
            genbank_download(2, db)
    elif db == "bacteria":
        refseq_download(15, db)
        if not refseq_only:
            genbank_download(5, db)
    elif db == "fungi":
        refseq_download(5, db)
        if not refseq_only:
            genbank_download(5, db)
    elif db == "protozoa":
        refseq_download(2, db)
        if not refseq_only:
            genbank_download(1, db)
    elif db == "viral":
        refseq_download(10, db)
        if not refseq_only:
            genbank_download(10, db)
    else:
        print(f"{db} Categoria inválida")

# For testing
# for db in databases:
#     if db == "archaea":
#         refseq_download(1, db)
#         if not refseq_only:
#             genbank_download(1, db)
#     elif db == "bacteria":
#         refseq_download(1, db)
#         if not refseq_only:
#             genbank_download(1, db)
#     elif db == "fungi":
#         refseq_download(1, db)
#         if not refseq_only:
#             genbank_download(1, db)
#     elif db == "protozoa":
#         refseq_download(1, db)
#         if not refseq_only:
#             genbank_download(1, db)
#     elif db == "viral":
#         refseq_download(1, db)
#         if not refseq_only:
#             genbank_download(1, db)
#     else:
#         print(f"{db} Categoria inválida")