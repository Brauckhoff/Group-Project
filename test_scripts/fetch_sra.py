import subprocess
import sys


# based on https://erilu.github.io/python-fastq-downloader/#downloading-fastq-files-using-the-sra-toolkit

def get_sra(*args):
    """
    Function to download SRA-files and extract fastq from NCBI
    :param args: SRR-ID(s) (space separated)
    :return: .sra and fastq.gz files <- that's what we want
    """
    for arg in args:

        # this will download the .sra files to ./arg
        print("Currently downloading: " + arg)
        prefetch = "prefetch " + arg
        print("The command used was: " + prefetch)
        subprocess.call(prefetch, shell=True)

        # this will extract the .sra files from above into a folder named 'fastq'
        print("Generating fastq for: " + arg)
        fastq_dump = "fastq-dump --outdir fastq --gzip ./" + arg + "/" + arg + ".sra"
        print("The command used was: " + fastq_dump)
        subprocess.call(fastq_dump, shell=True)

if __name__ == "__main__":
    # get all arguments after script
    get_sra(*sys.argv[1:])