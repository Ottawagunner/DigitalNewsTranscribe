import praw
import time
import datetime
import sys

#Logs into reddit using an account.
r = praw.Reddit('all_comment_scraper 1.0 by u/ottawagunner')
r.login('user', 'pass') #removed for upload
reload(sys)
sys.setdefaultencoding('utf-8')


print "Welcome to Reddit Comment Data Miner"
print "-Built with PRAW"
print(sys.version)

done = [] #list of comment ID's that have been parsed, prevents duplicates
KeyWords = [] #extended version of listwords, that includeds capitalization variations
listWords=[] #list of word to look for

#asks for file names for input and output. and subreddit
filename = raw_input('Enter an output file name: ') #prompts for name of file to write to
subname = raw_input('Enter a subreddit name: ')     #asks for subreddit

#handles the users adding .txt or ignoring it.
filename=filename.replace('\n', '').replace('.txt','')
filename=filename+'.txt'
subname=subname.replace('\n', '').replace('/r/','').replace('/','') #the subreddit to parse.

#this extracts the keywords and builds an array.
with open('searchList.txt') as search_file:
    listWords = [x.strip('\n') for x in search_file.readlines()]
KeyWords.extend(listWords)
KeyWords.extend(map(lambda x:x.title(),listWords))

#sets the current subreddit to the one given
subreddit = r.get_subreddit(subname)

print "Looking for :"
print '\n'.join(KeyWords)

#MAIN LOOP
while True:
    print "Grabbing Comments %s" % datetime.datetime.time(datetime.datetime.now())
    for comment in praw.helpers.comment_stream(r, subname, limit=None): #Takes a stream of new comments
        has_keywords = any(string in comment.body for string in KeyWords)#opens the comment and looks for the keywords
        if comment.id not in done and has_keywords: #if we havent done this comment and it has keywords, download it
            print "Downloading comment by %s" % comment.author.name
            with open(filename, 'a+') as the_file: #builds a file, appending each comment with some information
                the_file.write("%s;" % comment.author.name.encode('utf-8'))
                the_file.write("%s;" % comment.subreddit.display_name.encode('utf-8'))
                the_file.write("%s;" % datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S').encode('utf-8'))
                the_file.write("%s;\n" % comment.body.replace('\n', ' ').replace('\r', '').replace(';',' ').encode('utf-8'))
                done.append(comment.id)

    print "Waiting 45 seconds"
    time.sleep(45)# not required but might help if there is a disconnection
