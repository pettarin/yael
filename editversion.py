#!/usr/bin/env python

import re
import os
import sys

def usage():
    print("Usage:")
    print("  $ ./%s X.Y.Z" % sys.argv[0])
    print("")

def main():
    if len(sys.argv) < 2:
        usage()
        return

    new_version = sys.argv[1]

    files = [
        {
            "directory": False,
            "path":      "setup.py",
            "pattern":   r"    version='([0-9]+\.[0-9]+\.[0-9]+)',"
        },
        {
            "directory": False,
            "path":      "docs/source/conf.py",
            "pattern":   r"release = '([0-9]+\.[0-9]+\.[0-9]+)'"
        },
        {
            "directory": False,
            "path":      "README.md",
            "pattern":   r"\* Version: ([0-9]+\.[0-9]+\.[0-9]+)"
        },
        {
            "directory": True,
            "path":      "yael/",
            "pattern":   r"__version__ = \"([0-9]+\.[0-9]+\.[0-9]+)\""
        },
        {
            "directory": True,
            "path":      "test/",
            "pattern":   r"__version__ = \"([0-9]+\.[0-9]+\.[0-9]+)\""
        },
    ]

    try:
        os.mkdir("bak/")
    except OSError:
        pass

    for source_file in files:
        
        if source_file["directory"]:
            paths = []
            for root, subdirs, files in os.walk(source_file["path"]):
                for name in files:
                    if name.endswith(".py"):
                        paths.append(os.path.join(root, name))
        else:
            paths = [source_file["path"]]
        
        for path in paths:
            pattern = source_file["pattern"]
            obj = open(path, "r")
            contents = obj.read()
            obj.close()

            bak = open("bak/" + os.path.basename(path), "w")
            bak.write(contents)
            bak.close()

            acc = contents.splitlines()
            for i in range(len(acc)):
                line = acc[i]
                matched = re.search(pattern, line)
                if matched != None:
                    replaced = line.replace(matched.group(1), new_version)
                    print("%s +%d" % (path, i+1))
                    print("  - " + line)
                    print("  + " + replaced)
                    acc[i] = replaced
            
            out = open("bak/tmp", "w")
            out.write("\n".join(acc) + "\n")
            out.close()

            os.rename("bak/tmp", path)


if __name__ == '__main__':
    main()



