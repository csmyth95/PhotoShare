# Get the feed object for Jule's aggregated feed and follow Eric's user feed
jule_aggregated_feed = client.feed('aggregated', 'jule')
jule_aggregated_feed.follow('user', 'eric')

# Add an activity with the verb watch to Eric's feed
eric_feed.add_activity({'actor': 'eric', 'verb': 'watch', 'object': 1, 'youtube_id': '0m_lU2RA9Ak'})

# Read the last 3 activities from Jule's aggregated feed
response = jule_aggregated_feed.get(limit=3)
