import argparse
import os


def get_path_from_args() -> str:
    """Read path to a folder with CVE files."""
    parser = argparse.ArgumentParser(
        prog='lesson6',
        description='path to CVEs directory.'
    )
    parser.add_argument('--path_to_cves', default="./cvelistV5/cves/", required=False)
    args = parser.parse_args()
    return args.path_to_cves


def get_cve_filenames(path: str) -> list:
    """Returns list of paths of CVE files."""
    
    files_list = []
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            for year_entry in os.scandir(entry.path):
                if year_entry.is_dir(follow_symlinks=True):
                    for code_entry in os.scandir(year_entry.path):
                        files_list.append(code_entry.path)
    
    return files_list
