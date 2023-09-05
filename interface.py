"""Publish contents
"""
import argparse


def get_args():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder_path", help="Folder path to be mounted as static repo")
    parser.add_argument("--update", help="Update front", type=bool, default=False)
    args = parser.parse_args()
    return args
