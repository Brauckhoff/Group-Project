import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed


# based on https://erilu.github.io/python-fastq-downloader/#downloading-fastq-files-using-the-sra-toolkit

def get_sra(arg):
    """
    Function to download SRA-files and extract fastq from NCBI
    :param arg: SRR-ID(s) (space separated)
    :return: .sra and fastq.gz files <- that's what we want
    """

    # this will download the .sra files to ./arg
    print("Currently downloading: " + arg)
    prefetch = "prefetch " + arg
    print("The command used was: " + prefetch)
    subprocess.call(prefetch, shell=True)

    # this will extract the .sra files from above into a folder named 'fastq'
    print("Generating fastq for: " + arg)
    fastq_dump = "fastq-dump --outdir fastq -e 20 -p --gzip ./" + arg + "/" + arg + ".sra"
    print("The command used was: " + fastq_dump)
    subprocess.call(fastq_dump, shell=True)

def main(sra_ids, n_jobs=4):
    """
    Run get_sra in parallel
    :param sra_ids:
    :param n_jobs:
    :return:
    """
    with ProcessPoolExecutor(max_workers=n_jobs) as ex:
        tasks = [ex.submit(get_sra, sra) for sra in sra_ids]

        for task in as_completed(tasks):
            print(f"Completed: {task.result()}")

if __name__ == "__main__":
    # get all arguments after script
    sra_ids = sys.argv[1:]
    main(sra_ids, n_jobs=8)