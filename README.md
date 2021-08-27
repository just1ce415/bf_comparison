# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.


I. The main purpose of the library is a comparison between a book and relevant adaptation, in particular the volume of the book and the film duration.
Also the library provides addtional data such as year of publication and release, film rating.

II. Input:
Usage: python main_module.py imdb_path bnb_path
    Where imdb_path - the path (absolute or relative) to the IMDb database, bnb_path - the path to the BNB database of the particular author.
Usage: python main_module.py
    That way, the script will use databases in the root of the project. That is IMDB/ and MPalin/. If one argument is spared, it would be equal to the above command.
Usage: pythom main_module IMDB/ JAusten/
    For ulistrative purposes, the BNB database with Jane Austen is included to the project root.
ATTENTION!!!
    The directories with databases should have the same structure as providing archives from consequent websites.
    For IMDb that's directories with file data.tsv for each:
    name.basics title.akas title.basics title.crew title.episode title.principals title.ratings
    For BNB that's such files (showed for Michael Palin):
    british_library_catalogue_dataset_tc.pdf classification.csv names.csv Readme - Michael Palin.txt records.csv titles.csv topics.csv

III. Output:
Finished working, the script will output relevant message and the time of working.
ATTENTION!!!
    The script processes big data arrays, so it could work a bit long. For instance, for Michael Palin it could take approximately 10 seconds, for Jane Austen - less than 5 minutes.
The script writes all the processed data to the result.csv that has such column structure: Book title, Publication year, Number of pages, Film title, Year of release, Duration in minutes, Film rating, Pages per minute.
The titles which hasn't such parameters (except Film rating) will be ignored.

IV. Modules used:
Built-in: sys, time. Third-party: pandas.

V. Information usage:
The databases used are in open source and can be reaches by links:
    For IMDb: https://www.imdb.com/offsite/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3aefe545-f8d3-4562-976a-e5eb47d1bb18&pf_rd_r=G6KZX7NHZTDF4M9K50HH&pf_rd_s=center-1&pf_rd_t=60601&pf_rd_i=interfaces&page-action=offsite-imdbws&token=BCYlLIB7tRnKphnDuEgNczf1t8HVNcmpBdUwIFT9Tnhf1hwUNrTLJcPyLaBAklURKnghpoI-TNHW%0D%0A4IOOVPEJmk6DFAtdG9DM-WQGr9i4y4rLTcUOElBSk619GeoePAUE-M0KC2gxSUIe86K62uI0g6q_%0D%0AymxGw3x8B9d_2FsGhjw5TQkvcSUgXCprnbx_sh-cIsFAzh-JKSVKWHIZ4Ts-eFuEEA%0D%0A&ref_=fea_mn_lk3
    For BNB (M. Palin): https://www.bl.uk/bibliographic/downloads/MPalinResearcherFormat_202008_csv.zip
    For BNB (J. Austen): https://www.bl.uk/bibliographic/downloads/JAustenResearcherFormat_202007_csv.zip
