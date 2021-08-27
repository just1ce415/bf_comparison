"""The module to cut database with single function to optimize the code."""

import pandas

def cut_title_basics(path):
    '''
    (str) ->
    Throws out unnecessary titles.
    '''
    datafr = pandas.read_csv(path, sep=',', comment='#')
    datafr = datafr[(datafr['titleType'] == 'movie') | (datafr['titleType'] == 'tvMovie') |
    (datafr['titleType'] == 'tvSeries') | (datafr['titleType'] == 'tvSpecial')]
    datafr = datafr[datafr['startYear'] != '\\N']
    datafr = datafr[datafr['runtimeMinutes'] != '\\N']
    datafr.to_csv(path)


if __name__ == '__main__':
    cut_title_basics('IMDB/title.basics/data.tsv')
