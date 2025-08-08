`image-date-sorter`
===================

image-date-sorter is a script that sorts images into directories based on date.
It creates one directory per month, named according to ISO 8601 (e.g., the
directory for july 2024 is named `2024-07`).

It accepts two options:

- `--image-dir`: the directory to operate on;
- `--ignore-last-days`: do not sort images modified within the last `n` days.
  Set this to zero if you would like to sort all images. (This is useful if
  you're just trying to archive old images, but would like to keep recent ones
  on hand.)

This is a script I made for personal use, and I can't make guarantees as to how
robust it is. Still, it is robust enough for me to use it :)

Contributing
------------

If you'd like to contribute, feel free to do so! Please check your code with
mypy and flake8 before submitting a PR.

Licensing
---------

This repository and its contents are FOSS and published under GPL v3 (see
[the license](license.txt)).

