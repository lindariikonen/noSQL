USE datadb300;

COPY videos_by_title_year 
FROM './data/d1-videos_by_title_year.csv'
WITH HEADER=true;

