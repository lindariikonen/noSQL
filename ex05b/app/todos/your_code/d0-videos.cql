USE datadb300;

COPY videos 
FROM './data/d0-videos.csv' 
WITH HEADER=true;
