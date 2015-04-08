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

Well for the visualization I wanted to do some sort of poster that would show the data in a well presented format. I used InkScape and generated all the graphs and charts.

The graphs were made by setting the height or width based on the data that I got, then scaled them all up to make them the same ratio. 

The final result was a divided poster, with the Reddit r/all data on one side and Reddit r/history on the other. It followed the rule of thirds almost, where data was distributed in four quadrants. 

###Faults

Some of the issues that came up during the building of the data and the visualization.There were a fair amount of Spanish comments that i did not realize were in the data. I don't know how the sentiment works with that so it's a potential outlier. 

I had to remove the leader Tojo, simply not enough people were talking about him. As well the word tojo can be a subset of larger words, so the word "photojournalist" has the word tojo in it. Meaning i caught a lot of comments that had nothing to do with Tojo Hideki. 

There are issues with sentiment analysis that are evident. It does not take into consideration context and quotes. It also cannot figure out sarcasm, so it can mark harshly on sarcastic text. Short grammatically incorrect texts are often not parsed well and will yield errors. There is also a big issue of Anaphora Resolution. The algorithm simply can't figure out the pronoun and noun refers to. An example: "We watched the movie and went to dinner; it was awful." What does "It" refer to? Sentiment analysis is sill new and there are limitations on what to expect from it. Reference [here](http://www.cs.uic.edu/~liub/FBS/IEEE-Intell-Sentiment-Analysis.pdf)

As well unfortunately I lost a fair bit of data for some reason, luckily the largest dataset from March 17 was untouched, but a variety of others were completely blank. I'm not sure what caused this. Could be the VM or the code.    

####Visualization Iterations

I went through numerous iterations of my poster. Each one can be seen on [github.](https://github.com/Ottawagunner/RedditData/tree/master/Visual) I had many aspects to look at. Between visual1 and visual3 I changed the background to a lighter and easier to look at color. The black background made it difficult to see text and even choose colors since everything went with it. Between visual3 and vis4 I changed the background further lightening it. As well I changed the layout to a more horizontal focused one, which allowed me to show both posters in one. There was issues with wording, seeing Dr.Graham's additions to my title I changed it to his since it was much more on the point than my original one. As well I had gotten the advice to change the words "Good and Poor" to "Good" and "Bad".    

###Results

The results of this data mining and analysis are really amazing. Although it does have holes, it really shows the separation of Reddit. The use of historical figures in a public network is something untapped. From looking at this data we can see that Reddit uses Hitler the most and dislikes Churchill more than Hitler and Stalin. Reddit is one of the most trafficked website currently and it would be a wasted resource if we didn't look into it. From what I've gathered it shows that potentially Hitler is not being taken as seriously as it had been in earlier years. There is more debate on allied leaders, such as Churchill. All of this data was taken from a single day, March 17, and was the largest dataset taken. Obviously the more data would paint a clearer picture.