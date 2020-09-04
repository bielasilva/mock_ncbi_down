# Mock Genomes NCBI Download

Usage
    `mock_ncbi_down.py [-h] -d DIRECTORY_DOWNLOAD -c {archaea,bacteria,fungi,protozoa,viral}`
    * -d/--directory_download -> Directory where the files will be saved
    * -c/--databases -> Databases to be downloaded

    This script randomly selects genomes from RefSeq and Genbank based on the following criteria:
    1. RefSeq
        * It is a Complete Genome;
        * It has not already been downloaded.
    2. GenBank
        * It is a Complete Genome;
        * Its specie is not on RefSeq;
        * It was not rejected from RefSeq;
        * It has not already been downloaded;
    
    It's gonna be downloaded the following number of genomes:
|          | RefSeq | Genbank |
|----------|--------|---------|
| Archaea  |   15   |    5    |
| Bacteria |   15   |    5    |
| Fungi    |    5   |    5    |
| Protozoa |    2   |    2    |
| viral    |   10   |    10   |
