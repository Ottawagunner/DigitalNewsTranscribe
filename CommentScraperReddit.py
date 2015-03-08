import praw
import time
import datetime

r = praw.Reddit('all_comment_scraper 1.0 by u/ottawagunner')
#flat_comments = praw.helpers.flatten_tree(all_comments)
print "Welcome to Reddit Comment Data Miner"
print "-Built with PRAW"
#subreddit = r.get_subreddit('learnpython')
done = []
KeyWords = []
listWords=[]

filename = raw_input('Enter an output file name: ') #prompts for name of file to write to
subname = raw_input('Enter a subreddit name: ')     #asks for subreddit

filename=filename.replace('\n', '').replace('.txt','')
filename=filename+'.txt'
subname=subname.replace('\n', '').replace('/r/','').replace('/','')

with open('searchList.txt') as search_file:
	listWords = [x.strip('\n') for x in search_file.readlines()]
KeyWords.extend(listWords)
KeyWords.extend(map(lambda x:x.title(),listWords))


print "Looking for :"
print '\n'.join(KeyWords)

while True:
	print "Grabbing Comments %s" % datetime.datetime.time(datetime.datetime.now())
	subreddit = r.get_subreddit(subname)
	all_comments = subreddit.get_comments(limit=None)
	#all_comments = r.get_comments('all')
	for comment in all_comments:
		has_keywords = any(string in comment.body.encode("utf-8") for string in KeyWords)
		if comment.id not in done and has_keywords:
			print "Downloading comment by %s" % comment.author.name
			with open(filename, 'a+') as the_file:
				the_file.write("%s;" % comment.author.name.encode('utf-8'))
				the_file.write("%s;" % comment.subreddit.display_name.encode('utf-8'))
				the_file.write("%s;" % datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8'))
				the_file.write("%s;\n" % comment.body.replace('\n', ' ').replace('\r', '').replace(';',' ').encode('utf-8'))
				done.append(comment.id)
	print "Waiting 30 seconds"
	if len(done) >= 7000:
		done[:] = []
		print "More than 7000 elements, clearing... "
	time.sleep(30)
