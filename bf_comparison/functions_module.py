"""
The module with the functions that process information from two databases
(http://www.imdb.com/interfaces and https://www.bl.uk/collection-metadata/downloads) and
output the comparison of film duration and book length with some useful additional
data.

Note: imdb_path - path to the directory of IMDb, author_path - path to the directory
of the BNB (of the particular author).

!!! The path should be ended by '/' or '\\', so that we can understand what operating
system is it.
"""
import pandas

stored_titles = []


def get_path(path, destination):
    r'''
    (str) -> str
    Returns the path to the file associsted with destination.
    >>> get_path('MichaelPalin/', 'titles')
    'MichaelPalin/titles.csv'
    >>> get_path('Documents\\labs\\op\\mini-project\\IMDB\\', 'ratings')
    'Documents\\labs\\op\\mini-project\\IMDB\\title.ratings\\data.tsv'
    >>> get_path('IMdb/', 'basics')
    'IMdb/title.basics/data.tsv'
    '''
    # FOR LINUX AND MACOS
    if path.endswith('/'):
        if destination == 'ratings':
            return path + 'title.ratings/data.tsv'
        elif destination == 'basics':
            return path + 'title.basics/data.tsv'
        else:
            return path + 'titles.csv'
    # FOR WINDOWS
    elif path.endswith('\\'):
        if destination == 'ratings':
            return path + 'title.ratings\\data.tsv'
        elif destination == 'basics':
            return path + 'title.basics\\data.tsv'
        else:
            return path + 'titles.csv'


def get_year(str_year):
    '''
    (str) -> int
    Returns year of publication in convenient format.
    >>> get_year('1999')
    1999
    >>> get_year('1994-2004')
    1994
    '''
    if str_year.find('-') != -1:
        temp_lst = str_year.split('-')
        return int(temp_lst[0])
    elif str_year == 'nan':
        return None
    return int(str_year)


def get_pages(str_description):
    '''
    (str) -> int
    Determines the number of pages in str_description.
    >>> get_pages('xii, 198 pages, illustrations, 1 portrait, 20 cm')
    198
    >>> get_pages('361 pages, illustrations, 20 cm')
    361
    >>> get_pages('xxii, 650 pages, 24 pages of plates, illustrations (some colour), portraits, 24 cm')
    650
    >>> get_pages('12 unnumbered pages, colour illustrations, 29 cm')

    >>> get_pages('1 online resource (xx, 138 pages), illustrations')
    138
    >>> get_pages('144 pages (23 pages)')
    144
    '''
    last_occurence = 0
    slength = len(str_description)
    pages_variants = []
    # IT CAN BE MORE THAN ONE NUMBERS OF PAGES
    while str_description[last_occurence : slength+1].find(' pages') != -1:
        start_occurence = str_description[last_occurence : slength+1].find(' pages')
        # DETERMINING IF NUMBER OF PAGES IS FOUR-DIGIT, THREE-DIGIT...
        if len(str_description[last_occurence : last_occurence + start_occurence]) > 3:
            pages_variants.append(str_description[last_occurence + start_occurence-4 :
            last_occurence + start_occurence+1])
        elif len(str_description[last_occurence : last_occurence + start_occurence]) == 3:
            pages_variants.append(str_description[last_occurence + start_occurence-3 :
            last_occurence + start_occurence+1])
        elif len(str_description[last_occurence : last_occurence + start_occurence]) == 2:
            pages_variants.append(str_description[last_occurence + start_occurence-2 :
            last_occurence + start_occurence+1])
        elif len(str_description[last_occurence : last_occurence + start_occurence]) == 1:
            pages_variants.append(str_description[last_occurence + start_occurence-1 :
            last_occurence + start_occurence+1])
        last_occurence = last_occurence + start_occurence + 8
    if pages_variants == []:
        return None
    # STRIPPPING WHITESPACES
    for i in range(len(pages_variants)):
        # CHECKING FOR EXCEPTION
        try:
            pages_variants[i] = int(pages_variants[i].strip())
        except ValueError:
            return None
    return max(pages_variants)


def create_imdb_df(imdb_path):
    '''
    (str) -> object DataFrame
    Creates a convenient DataFrames(for IMDb) for browsing and analysing data.
    Returns tuple with DataFrames (df_basics, df_ratings).
    >>> create_imdb_df('IMDB/')[0]['primaryTitle']
    0                                       Carmencita
    1                           Le clown et ses chiens
    2                                   Pauvre Pierrot
    3                                      Un bon bock
    4                                 Blacksmith Scene
                                ...                   
    1048570                 The Wrath of Moonthunder!!
    1048571                       Is Spectreman Dead?!
    1048572    Death-Match!! G-Men vs. Monster Vegaron
    1048573    Operation: Destroy Gori's Saucer Base!!
    1048574                  Episode dated 5 June 2019
    Name: primaryTitle, Length: 1048575, dtype: object
    '''
    # DETECTING FILES
    basics_path = get_path(imdb_path, 'basics')
    ratings_path = get_path(imdb_path, 'ratings')
    # CREATING DATAFRAME
    df_basics = pandas.read_csv(basics_path, sep=',', comment='#')
    df_ratings = pandas.read_csv(ratings_path, sep='\t', comment='#')
    return (df_basics.loc[ : , ['tconst', 'primaryTitle', 'originalTitle', 'startYear', 'runtimeMinutes']],
    df_ratings)


def create_author_df(path):
    '''
    (str) -> object DataFrame
    Creates a convenient DataFrame(for BNB) for browsing and analysing data.
    >>> create_author_df('MPalin/')['Title']
    0      'Short Films (Gibbs etc.)/Script Ideas/Ian's T...
    1       A little light worrying : the best of Mel Calman
    2                              A pocketful of Python [4]
    3                                  A pocketful of Python
    4                                        A point of view
                                 ...                        
    174                                    Works. Selections
    175                                    Works. Selections
    176                                    Works. Selections
    177                                    Works. Selections
    178                                    Works. Selections
    Name: Title, Length: 179, dtype: object
    '''
    # DETECTING FILE
    titles_path = get_path(path, 'titles')
    # CREATING DATAFRAME
    df = pandas.read_csv(titles_path, sep=',', comment='#')
    return df.loc[ : , ['Title', 'Other titles', 'Date of creation/publication',
    'Physical description']]


def book_info_generator(path):
    '''
    (str) -> <class 'generator'>
    Returns the generator of titles for the particular author. The
    functions yields the tuple (title, list(other_titles), year_of_publication, number_of_pages).
    The date and the number of pages are related to the very first edition if
    these parametrs are stated. Otherwise it will consider data of the second edition
    and so forth. If the pages is not stated, the title will be ignored.
    '''
    df = create_author_df(path)
    for i in range(df.shape[0]):
        # CHEKING IF PAGES ARE STATED
        if df.iloc[i, 0] not in stored_titles and str(df.iloc[i, 3]).find(' pages') != -1:
            # GET TITLE
            title = str(df.iloc[i, 0])
            # GET OTHER TITLES WITH CHECK
            other_titles_str = str(df.iloc[i, 1])
            if other_titles_str == 'nan':
                other_titles = []
            else:
                other_titles = other_titles_str.split(' ; ')
            # GET PUBLICATION YEAR
            publication_year = get_year(str(df.iloc[i, 2]))
            if publication_year == 'nan':
                publication_year = None
            # GET PAGES
            pages = get_pages(str(df.iloc[i, 3]))
            yield (title, other_titles, publication_year, pages)


def imdb_comparison(imdb_path, author_path):
    '''
    (str, str) -> list(tuple)
    Returns the list of tuples for the books-films reading data from files
    (usage of previous functions).
    (book_title, publication_year, pages, film_title, release_year, minutes,
    pages_per_minute, film_rating).
    '''
    df_basics, df_ratings = create_imdb_df(imdb_path)
    # CREATING THE LIST OF ALL TITLES TO SEARCH FOR COINCIDENCE
    all_film_origtitles = list(df_basics.loc[ : , 'originalTitle'])
    bnb_generator = book_info_generator(author_path)
    # LIST FOR OUTPUT
    result_lst = []
    # LIST FOR STORING TITLES
    global stored_titles
    try:
        # USING GENERATOR TO SAVE MEMORY
        while True:
            book_info = next(bnb_generator)
            # PROCEEDING WITH 'OTHER TITLES' IF SUCH EXISTS.
            if book_info[1] != []:
                for other_title in book_info[1]:
                    if book_info[0] in all_film_origtitles:
                        proper_film_info = df_basics[df_basics['originalTitle'] ==
                        book_info[0]].values[0]
                    elif other_title in all_film_origtitles:
                        proper_film_info = df_basics[df_basics['originalTitle'] ==
                        other_title].values[0]
                    else:
                        proper_film_info = []
            else:
                if book_info[0] in all_film_origtitles:
                    proper_film_info = df_basics[df_basics['originalTitle'] ==
                    book_info[0]].values[0]
                else:
                    proper_film_info = []
            # CHECKING IF ADAPTATION IS FOUND
            if proper_film_info == []:
                continue
            # MINUTES PER PAGE
            if proper_film_info[4] == '\\N' or book_info[3] is None:
                proper_film_info[4] = ''
                pages_per_minute = None
            else:
                pages_per_minute = round(book_info[3] / int(proper_film_info[4]), 3)
            # FILM RATING
            if not df_ratings[df_ratings['tconst'] == proper_film_info[0]].empty:
                rating = df_ratings[df_ratings['tconst'] == proper_film_info[0]].values[0][1]
            else:
                rating = ''
            # APPENDING DATA
            if (proper_film_info[3] != '\\N' and pages_per_minute is not None and
            book_info[2] is not None and book_info[2] <= int(proper_film_info[3])):
                result_lst.append((book_info[0], book_info[2], book_info[3], proper_film_info[1],
                proper_film_info[3], proper_film_info[4], rating, pages_per_minute))
                stored_titles.append(book_info[0])
    except StopIteration:
        return result_lst


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
