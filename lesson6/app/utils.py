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
    for year_entry in os.scandir(path):
        if year_entry.is_dir(follow_symlinks=False):
            for code_entry in os.scandir(year_entry.path):
                if code_entry.is_dir(follow_symlinks=True):
                    for cve_entry in os.scandir(code_entry.path):
                        files_list.append(cve_entry.path)
    
    return files_list
