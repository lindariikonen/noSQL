USE datadb300;

COPY videos (video_id, added_date, description, tags, title, user_id)
FROM './data/d5-videos.csv'
WITH HEADER=true;
