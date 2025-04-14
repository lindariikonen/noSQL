USE datadb300;

COPY bad_videos_by_tag_year 
(tag, added_year, video_id, added_date, description, title, user_id) 
FROM './data/d2-videos_by_tag_year.csv' WITH HEADER=true;
