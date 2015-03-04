import praw
import time
import datetime

r = praw.Reddit('all_comment_scraper 1.0 by u/ottawagunner')
print "Looping comments"
done = []
KeyWords = [' Hitler ',' Stalin ']

while True:
	print "Grabbing %s" % datetime.datetime.time(datetime.datetime.now())
	subreddit = r.get_subreddit('all')
	all_comments = subreddit.get_comments(limit=None)
	#all_comments = r.get_comments('all')
	for comment in all_comments:
		has_keywords = any(string in comment.body for string in KeyWords)
		if comment.id not in done and has_keywords:
			print "///////////////////////////////%s" % comment.author.name
			with open('dictator_use2.txt', 'a') as the_file:
				the_file.write("%s;" % comment.author.name.encode('utf-8'))
				the_file.write("%s;" % comment.subreddit.display_name.encode('utf-8'))
				the_file.write("%s;" % datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8'))
				the_file.write("%s;\n" % comment.body.replace('\n', ' ').replace('\r', '').replace(';',' ').encode('utf-8'))
				done.append(comment.id)
	print "Waiting"
	if len(done) >= 7000:
		done[:] = []
		print "More than 7000 elements, clearing... "
	time.sleep(30)
