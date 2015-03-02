import praw
import time

r = praw.Reddit('all_comment_scraper 1.0 by u/ottawagunner')
print "Looping comments"
done = []

while True:
	print "Grabbing"
	subreddit = r.get_subreddit('all')
	all_comments = subreddit.get_comments(limit=None)
	#all_comments = r.get_comments('all')
	for comment in all_comments:
		if comment.id not in done:
			print "%s" % comment.author.name
			with open('test15.txt', 'a') as the_file:
				the_file.write("%s;" % comment.author.name.encode('utf-8'))
				the_file.write("%s;" % comment.subreddit.display_name.encode('utf-8'))
				the_file.write("%s;\n" % comment.body.replace('\n', ' ').replace('\r', '').replace(';',' ').encode('utf-8'))
				done.append(comment.id)
	print "Waiting"
	time.sleep(10)
