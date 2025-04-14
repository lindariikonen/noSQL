USE datadb300;

COPY videos_by_actor (actor, added_date, video_id, character_name, description, encoding, tags, title, user_id)
FROM './data/d3-videos_by_actor.csv'
WITH HEADER=true;
