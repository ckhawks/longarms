# basic static parsing rss feeds
d = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id=UCXIyz409s7bNWVcM-vjfdVA')

print(d['feed']['title']) # Majestic Casual
print(d['feed']['link']) # Majestic Casual
print(len(d['entries']))
videotitle = d['entries'][1]['title']
print(videotitle)
titlearray = videotitle.split("-")
print(titlearray)


for post in d.entries:
    uploadtime = dateutil.parser.parse(post.published)
    print(post.title + " at " + uploadtime.isoformat())

    artist = ""; title = "";
    titlearray = post.title.split("-")

    if(len(titlearray) > 1):
        artist = titlearray[0]
        title = titlearray[1]
    else:
        artist = ""
        title = post.title

# timedate-related things

print(NOW) # 2019-03-07 05:21:49.872484
lastRun = NOW+relativedelta(minutes=+-5)
print(lastRun) # 2019-03-07 05:22:44.820410
               # 2019-03-07 05:17:44.820410
