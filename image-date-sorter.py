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
    for i in os.listdir(args.image_dir):
        if not os.path.isfile(f"{prefix}/{i}"):
            continue

        # ignore recent files
        stat_result = os.stat(f"{prefix}/{i}")
        mtime = datetime.fromtimestamp(stat_result.st_mtime)
        if mtime > date_limit:
            files_ignored += 1
            continue

        # find and create the directory if needed
        target_dir = f"{mtime.year:04}-{mtime.month:02}"
        if not os.path.exists(f"{prefix}/{target_dir}"):
            print(f"+ {target_dir}")
            os.mkdir(f"{prefix}/{target_dir}")
            dirs_created += 1

        # move the file
        print(f"{i} -> {target_dir}")
        os.rename(f"{prefix}/{i}", f"{prefix}/{target_dir}/{i}")
        files_moved += 1

print("Done:")
print(f"\t  + {dirs_created} directories created")
print(f"\t -> {files_moved} files moved")
print(f"\t () {files_ignored} files ignored")
