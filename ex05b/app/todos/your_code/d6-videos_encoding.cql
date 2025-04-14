USE datadb300;

COPY videos (video_id, encoding)
FROM './data/d6-videos_encoding.csv'
WITH HEADER=true;
