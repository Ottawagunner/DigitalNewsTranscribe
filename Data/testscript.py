import praw
import time
import datetime
import sys
r = praw.Reddit('all_comment_scraper 1.0 by u/ottawagunner')
r.login('ottabot', 'testbot')
#flat_comments = praw.helpers.flatten_tree(all_comments)
reload(sys)
sys.setdefaultencoding('utf-8')

print "Welcome to Reddit Comment Data Miner"
print "-Built with PRAW"
print(sys.version)

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

subreddit = r.get_subreddit(subname)

print "Looking for :"
print '\n'.join(KeyWords)

while True:
	print "Grabbing Comments %s" % datetime.datetime.time(datetime.datetime.now())
	for comment in praw.helpers.comment_stream(r, subname, limit=None):
		has_keywords = any(string in comment.body for string in KeyWords)
		if comment.id not in done and has_keywords:
			print "Downloading comment by %s" % comment.author.name
			with open(filename, 'a+') as the_file:
				the_file.write("%s;" % comment.author.name.encode('utf-8'))
				the_file.write("%s;" % comment.subreddit.display_name.encode('utf-8'))
				the_file.write("%s;" % datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8'))
				the_file.write("%s;\n" % comment.body.replace('\n', ' ').replace('\r', '').replace(';',' ').encode('utf-8'))
				done.append(comment.id)

	print "Waiting 45 seconds"
	time.sleep(45)

#tutorial on raspberryPI