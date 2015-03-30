Harvesting Reddit Comments and Analyzing Historical Figures
------
###Purpose

With my background in computer science I wanted to do something that involved web scraping, as it could be done with a script. I looked into Twitter's TWARK API, but after learning Reddit was encoded into J son I chose Reddit to mine. I found an API called PRAWS that would help me develop a script that could mine for me. My goal was to look at how Reddit uses World War II leaders in their comments and how subreddits differ in use. 

###The Script

```python
import praw
import time
import datetime
import sys
r = praw.Reddit('all_comment_scraper 1.0 by u/ottawagunner')
r.login('user', 'pass') #removed for upload
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
```

The script I wrote asks the user for a file name to save the data into. Then prompts the user for a subreddit or multiple subreddits. The script looks into a file that holds keywords. The script takes everything inputted and will scan said subreddits comments for the keywords then download the comment as well as the subreddit the the comment came from and the date and username. it formated into a pseudo CSV file. From this I analyzed the produced files.

###Hiccups and learning the script

Despite my computer science background I have not ever coded in Python before and it was a bit of a learning curve. When I got the hang of it I did run into some issues mainly data sanitation. 

In the code where is says 
`KeyWords.extend(map(lambda x:x.title(),listWords))` 
It is actually taking the keyword list and adding the whole list again to it's self but is capitalizing the words. So if the keyword file had 'stalin' it would add the word 'Stalin' making the file look like 'stalin Stalin' so that when it searches it looks for both cases.

When looking in the script you can see a few times it will use the command 
`.replace('\n', ' ')`
This is part of the data sanitation. What this does is looks through text and when it finds the newline divider (\n) it replaces it with a empty space. This is important for the writing to file as CSV's don't like newlines.

###Wrangling data

After obtaining the data files there was a need to go through them and remove errors and make the data more manageable. Using [Voyant Tools](voyant-tools.org) I looked at the word count that would indicate errors in the file. Some errors were comments that were comprised of only the letter á. I simply removed those comments. As well there were comments that contained the word &gt, which I found out was quoted text. I removed the instances of &gt with a space.

After the data was relatively solid I performed a sentiment analysis on the data. The package is called [syuzhet](https://github.com/mjockers/syuzhet). I used a starting base [here](https://gist.githubusercontent.com/shawngraham/87bb74b576395737fc76/raw/3abe097b2d8d6f59ebe1cc6bf51f11ee78576f6d/working-w-syuzhet.R) to start my script that now looks like this.
```
install.packages("devtools")
devtools::install_github("mjockers/syuzhet")
library("syuzhet")

data <- read.csv('RedditAll.csv', colClasses=c('NULL','NULL', 'NULL', NA)) #only selects the text of the csv

x <-as.character(data[["Text"]]) 

stext <- get_sentiment(x)

write.csv(stext, "stext.csv")
```
From this I get sentiment numbers that tell the sentiment of all the comments. I then performed a simple average to get the average sentiment on each leader.This number was used in the final visualization graph.

###Visualization Aims

Well for the visualization I wanted to do some sort of poster that would show the data in a well presented format. I used InkScape and gereated all the 

###Faults

Didn't catch Spanish comments

Tojo was removed as it created problematic and minimal responses



###Results
