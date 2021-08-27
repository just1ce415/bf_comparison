"""
The module to represent the performance of functions from functions_module.py.
Note: imdb_path - path to the directory of the IMDb, author_path - path to the directory
of the BNB (of the particular author).

The directories sholud have the same structure as an archives that can be downloaded
from http://www.imdb.com/interfaces and https://www.bl.uk/collection-metadata/downloads
consequently.

!!! The path should be ended by '/' or '\\', so that we can understand what operating
system is it.

For details check report.pdf or README.md.
"""

import time
import sys
import pandas
from functions_module import imdb_comparison as get_data


def main_func(imdb_path, author_path):
    '''
    (str, str) ->
    Stores all the data to the result.csv. The information will be presented in such order:
    Book title, Publication year, Number of pages, Film title (of adaptation), Year
    of release, Duration in minutes, Minutes per page, Film rating.
    '''
    # TO MEASURE THE TIME OF WORKING
    start = time.time()
    # GETTING DATA
    processed_data = get_data(imdb_path, author_path)
    # STORING IT TO CSV FILE
    datafr = pandas.DataFrame(processed_data, columns=['Book title', 'Publication year',
    'Number of pages', 'Film title', 'Year of release', 'Duration in minutes',
    'Film rating', 'Pages per minute'])
    datafr.to_csv('result.csv')
    seconds = time.time() - start
    print('Finished working\n' + 'Time spent: ' + str(round(seconds, 3)) + 'sec.')


if __name__ == '__main__':
    try:
        main_func(sys.argv[1], sys.argv[2])
    except IndexError:
        main_func('IMDB/', 'MPalin/')
