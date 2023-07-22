# --------- USAGE -----------
# USE THIS FILE IF YOU WANT TO MAINTAIN DIRECTORY STRUCTURE WHILE DECOMPILING ".PYC" TO ".PY" RECURSIVELY
# Install Python 
# Run -> pip install uncompyle6
# Run -> python decompile_pyc_recursively.py -p [PATH-OF-PYC-DIR]
# ----------------------------


import argparse
import os
import glob
import subprocess

FROM_EXTENSION = "pyc"
TO_EXTENSION = "py"

parser = argparse.ArgumentParser(
    description='Decompile .pyc files recursively. '

                'It takes a directory in --path argument to scan for .pyc files to uncompile')

parser.add_argument('-p', '--path', dest='path',

                    default=os.path.abspath("."),

                    help="Specify root directory to scan pyc files from")


class uncompyle6:
    def __init__(self):
        pass

    @staticmethod
    def check_uncompyle():
        try:
            subprocess.call(["uncompyle6", "--version"])
        except OSError as e:
            print("[ERROR] - uncompyle6 or any of its dependencies are not installed")
            print(
                "[ERROR] - refer to https://pypi.org/project/uncompyle6/ to install uncompyle6 and try again")
            exit(e.errno)

    @staticmethod
    def swap_extension(compiled):
        """
        Swap file extension from .pyc to .py
        :param compiled:
        :return:
        """

        metadata = os.path.splitext(compiled)

        return "{0}.{1}".format(metadata[0], TO_EXTENSION)

    def normalize_path(self, paths):
        """
        Normalize paths
        :param paths:
        :return:
        """

        clean = []  # hold clean list of normalized matching paths

        prefix = os.path.commonprefix(paths)

        for i in paths:
            source = i

            base = self.swap_extension(i.replace(prefix, ""))

            clean.append({"source": source, "dirname": os.path.dirname(
                base), "name": os.path.basename(base)})

        return clean

    @staticmethod
    def search_pyc(use_directory):
        """
        Search .pyc files
        :param use_directory:
        :return:
        """

        return glob.glob("/".join([use_directory, "*." + FROM_EXTENSION]))

    @staticmethod
    def setup_directories(directories, parent):
        """
        Mimic file organization
        :param directories:
        :param parent:
        :return:
        """

        for i in directories:
            if i["dirname"]:
                directory_name = os.path.join(parent, i["dirname"])
                if os.path.exists(directory_name):
                    continue
                os.mkdir(directory_name)
                print("[INFO] - Done creating %s directory" % directory_name)

    @staticmethod
    def uncompyle(locations, parent):
        for i in locations:
            uncompyle_source = i["source"]
            uncompyle_to = os.path.join(parent, i["dirname"], i["name"])
            subprocess.call(
                ["uncompyle6", "-o", uncompyle_to, uncompyle_source])
            print(
                "[INFO] - {0} decompiled at {1}".format(uncompyle_source, uncompyle_to))


if __name__ == "__main__":
    matches = []
    args = parser.parse_args()
    path = args.path
    os.mkdir('decompiled')
    cwd = os.path.abspath("./decompiled")
    uncompyler = uncompyle6()
    uncompyler.check_uncompyle()
    for root, dirs, files in os.walk(path):
        for result in uncompyler.search_pyc(root):
            matches.append(result)
    normalized = uncompyler.normalize_path(matches)
    uncompyler.setup_directories(normalized, cwd)
    uncompyler.uncompyle(normalized, cwd)

    exit(0)
