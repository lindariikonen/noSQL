USE datadb300;

COPY videos_by_genre (genre, added_date, video_id, description, encoding, tags, title, user_id)
FROM './data/d4-videos_by_genre.csv'
WITH HEADER=true;
