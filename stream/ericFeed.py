import stream

# SCALABLE NEWS FEED
#Works for 3 users but can be changed for more

#Part 1
client = stream.connect('8d2pm9kfhbt4', 'bpqn7haggg75qdjuwgfagfu4n9wspekn2hq8z88wq2hm7j3btym45p7g3rrmg6gt')
# Get the feed object
eric_feed = client.feed('user', 'eric')
# Add the activity to the feed
eric_feed.add_activity({'actor': 'eric', 'verb': 'tweet', 'object': 1, 'tweet': 'Hello world'});

#Part 2
# Let Jessica's flat feed follow Eric's and Rick's feeds
jessica_flat_feed = client.feed('flat', 'jessica')
jessica_flat_feed.follow('user', 'eric')
jessica_flat_feed.follow('user', 'rick')

# activities on Eric's personal feed will flow automatically in Jessica's feed
user1 = client.feed('user', '1')
user1.add_activity({'actor': 1, 'verb': 'watch', 'object': 1, 'youtube_id': 'z_AbfPXTKms'});

# Read the activities from Jessica's flat feed
response = jessica_flat_feed.get(limit=3)
