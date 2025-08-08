#!/usr/bin/python3

import argparse
import os

from datetime import datetime, timedelta
from typing import Any, Dict


allowed_args: Dict[str, Dict[str, Any]] = {
    "--image-dir": {
        "type": str,
        "required": True,
        "action": "store",
        "help": "Directory to be sorted",
    },
    "--ignore-last-days": {
        "type": int,
        "required": False,
        "action": "store",
        "default": 7,
        "help": "Ignore images from the last X days",
    },
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for i in allowed_args:
        parser.add_argument(i, **allowed_args[i])
    args = parser.parse_args()

    prefix = args.image_dir
    date_limit = datetime.now() - timedelta(days=args.ignore_last_days)

    print(f"Operating on {prefix}")
    print(
        f"Date limit: {args.ignore_last_days} days "
        f"({date_limit.strftime('%FT%H:%M:%S%z')})"
    )

    dirs_created = 0
    files_moved = 0
    files_ignored = 0
    for i in os.listdir(prefix):
        if not os.path.isfile(f"{prefix}/{i}"):
            continue

        # Ignore recent files
        stat_result = os.stat(f"{prefix}/{i}")
        mtime = datetime.fromtimestamp(stat_result.st_mtime)
        if mtime > date_limit:
            files_ignored += 1
            continue

        # Find and create the directory if needed
        target_dir = f"{mtime.year:04}-{mtime.month:02}"
        if not os.path.exists(f"{prefix}/{target_dir}"):
            print(f"+ {target_dir}")
            os.mkdir(f"{prefix}/{target_dir}")
            dirs_created += 1

        # Move the file
        print(f"{i} -> {target_dir}")
        os.rename(f"{prefix}/{i}", f"{prefix}/{target_dir}/{i}")
        files_moved += 1

# Align numbers to the right, padding with spaces. It should look like this:
# Done:
#      +   3 dirs created
#     -> 123 files moved
#     ()  23 files ignored

n_len = max((len(str(i)) for i in [dirs_created, files_moved, files_ignored]))
print("Done:")
print("\t  + {d: >{len}} dirs created".format(d=dirs_created, len=n_len))
print("\t -> {f: >{len}} files moved".format(f=files_moved, len=n_len))
print("\t () {f: >{len}} files ignored".format(f=files_ignored, len=n_len))
