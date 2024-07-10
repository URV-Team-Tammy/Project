# Project
Predicting workload of regions in Europe based on existing data from ENTSO-E and Electricity Maps.

## Data Cleaning
Use ``autocleaner.sh`` to automatically clean ENTSO-E generation files in ``Data Cleaning/in``, outputted into ``Data Cleaning/out``. ``cleaner.py`` is the backend of this script, and can be used from the command line with the following command: ``python3 cleaner.py filename``.

