#!/usr/bin/env python3

import csv, random, os
random.seed(5)

in_file = "/home/gabrielasilva/Documents/projetos/mock_ncbi_down/assembly_summary_fungi.txt"
down_directory = "/home/gabrielasilva/Documents/projetos/mock_ncbi_down/download"
out_file = "/home/gabrielasilva/Documents/projetos/mock_ncbi_down/mock_downloaded.tsv"

def random_refseq (seq_number, category):
    # Download Assembly summary
    os.mkdir(f"{down_directory}/{category}")
    ftp_link = "ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/"
    os.system(f"wget -O assembly_summary{category}.txt -P {down_directory}/{category} -c {ftp_link} ")
    with open(in_file) as i_file, open(out_file,"w+") as o_file:
        csv_read = csv.reader(i_file, delimiter="\t")
        next(csv_read)
        complete_entries = []
        for row in csv_read:
            if row[11] == "Complete Genome":
                complete_entries.append(row)
        rand_choice = random.choices(complete_entries, k=seq_number)
        downloaded = []
        header = ["assembly_accession", "organism_name", "infraspecific_name", "ftp_path"]
        csv_write = csv.DictWriter(o_file, fieldnames=header, delimiter="\t")
        csv_write.writeheader()
        for item in rand_choice:
            csv_write.writerow({
                "assembly_accession": item[0],
                "organism_name": item[7],
                "infraspecific_name": item[8],
                "ftp_path": item[19],
            })
            genome_link = item[19] + "/" + item[19].split("/")[-1] + "_genomic.fna.gz"
            os.system(f"wget -P {down_directory} -c {genome_link} ")

