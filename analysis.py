import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import time

fname = 'jasons.xml'

#function to look up keywords in xml
def lookup(d, key):
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key :
            found = True
    return None

#parsing xml excel Library
stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print 'My iTunes Library at a Glance'
print (time.strftime("%d/%m/%Y"))
print 'Total number of files (including songs, podcasts, and movies):', len(all)
name_lst = list()
artist_lst = list()
count_lst = list()
length_lst = list()
genre_lst = list()
year_lst = list()

#looking things up
for entry in all:
    if ( lookup(entry, 'Track ID') is None ) : continue

    name = lookup(entry, 'Name')
    name_lst.append(name)
    artist = lookup(entry, 'Artist')
    artist_lst.append(artist)
    count = lookup(entry, 'Play Count')
    count_lst.append(count)
    length = lookup(entry, 'Total Time')
    length_lst.append((name, artist, length))
    genre = lookup(entry, 'Genre')
    genre_lst.append(genre)
    year = lookup(entry, 'Year')
    year_lst.append((name, artist, year))

    if name is None or artist is None or genre is None or length is None:
        continue

year_lst_1 = list()
for name, artist, year in year_lst:
    if name is not None and year is not None:
        year_lst_1.append((name, artist, year))
year_order = list()
for name, artist, year in year_lst_1:
    year_order.append((year, name, artist))
year_order.sort()
print "20 oldest songs in the library:"
rank = 0
just_year = list()
for year, name, artist in year_order[0:20]:
    rank = rank + 1
    ranka = str(rank)+"."
    just_year.append(year)
    print ranka, name, artist, year
print "\n20 most recent songs in the library:"
rank = 0
for year, name, artist in year_order[len(year_order)-20:len(year_order)]:
    rank = rank+1
    ranka = str(rank)+"."
    print ranka, name, artist, year

#counting artists
artist_lst_1 = list()
for artist in artist_lst:
    if artist is not None:
        artist_lst_1.append(artist)
artist_count = dict()
for art in artist_lst_1:
    if art not in artist_count:
         artist_count[art] = 1
    else:
        artist_count[art] = artist_count[art]+1
#order the artists based on count
artist_order = list()
for key, value in artist_count.items():
    artist_order.append((value, key))
artist_order.sort(reverse=True)
print "\nTotal number of artists:", len(artist_order)
top_20_artist = list()
for value, key in artist_order[0:20]:
    top_20_artist.append((key, value))
print "Top 20 artists in my library:"
#print artist based on rank
rank = 0
for key, value in top_20_artist:
    rank = rank+1
    ranka = str(rank)
    rankb = ranka+"."
    print rankb, key, value
#graph artists
artists_name = list()
artists_count = list()
for key, value in top_20_artist[0:5]:
    artists_name.append(key)
    artists_count.append(value)
y_pos = np.arange(len(artists_name))
plt.bar(y_pos, artists_count, align = 'center', alpha = 1)
plt.xticks(y_pos, artists_name ,fontsize=10)
plt.ylabel("Counts")
plt.title('Top 5 Artists')
plt.show()

#getting ride of missing data
genre_lst_1 = list()
for genre in genre_lst:
    if genre is not None:
        genre_lst_1.append(genre)
#counting genre
genre_count = dict()
for genre in genre_lst_1:
    if genre not in genre_count:
        genre_count[genre]=1
    else:
        genre_count[genre]=genre_count[genre]+1
print "\nTotal number of genres:", len(genre_count)
genre_order = list()
for key, value in genre_count.items():
    genre_order.append((value,key))
genre_order.sort(reverse=True)
top_20_genre=list()
rank = 0
def percentage(a,b):
    per = 100*(float(a)/float(b))
    return ("%.2f" % per)
print "Top 20 genres in my library"
for value, key in genre_order[0:20]:
    rank = rank + 1
    ranka = str(rank)
    rankb = ranka+"."
    y = percentage(value, len(all))
    print rankb, key, value, "("+y+"%)"

#pie chart genre_count
genre_name = list()
genre_perct = list()
others = list()
for value, key in genre_order:
    y = float(percentage(value, len(all)))
    if y>5:
        genre_name.append(key)
        genre_perct.append(y)
    elif y<5:
        others.append(y)
total = 0
for number in others:
    total = total + number
genre_name.append("Others")
genre_perct.append(round(total,2))
labels = genre_name
sizes = genre_perct
patches, texts = plt.pie(sizes)
plt.legend(patches, labels, loc ="best")
plt.title('Top Genres')
plt.axis('equal')
plt.tight_layout()
plt.show()

#function to calculate length in minutes and seconds
def minutes(object):
    y = float(object)/60000
    y_s = int(y)
    z = y - y_s
    if z <0.01667:
        return "%s:00"%(y_s)
    j = z*60 -int(z*60)
    if j == 0:
        return "%s:00"%(y_s)
    elif j >= 0.5:
        a = int(z*60)+1
        return "%s:%s"%(y_s,a)
    elif j < 0.5:
        b = int(z*60)
        return "%s:%s"%(y_s,b)
length_lst_1 = list()
for name, artist, length in length_lst:
    if name is not None and artist is not None and length is not None:
        length_lst_1.append((name,artist,float(length)))
print "\nTotal number of songs:", len(length_lst_1)
length_order = list()
for artist, name, length in length_lst_1:
    length_order.append((length, name, artist))
length_order.sort(reverse=True)
justlength = list()
for length, name, artist in length_order:
    justlength.append(float(length))
#computing average and median
count = 0
total = 0
for length in justlength:
    count = count + 1
    total = total + length
average = int(total/count)
print "Average duration:", minutes(average)
def median(object):
    object.sort()
    if len(object)%2==0:
        a = len(object)/2
        b = (len(object)/2)-1
        x = float(object[a])
        y = float(object[b])
        return float((x+y)/2)
    if len(object)%2!=0:
        a = len(object)/2
        x = object[a]
        return x
print "Median duration:", minutes(median(justlength))
print "Range:", minutes(justlength[0])+"~"+minutes(justlength[len(justlength)-1])
#print length_order
print "Top 20 track duration in my library"
rank = 0
for length, name, artist in length_order[0:20]:
    rank = rank + 1
    ranks = str(rank)
    rankf = ranks + "."
    j = minutes(length)
    print rankf, name, "("+artist+")", j
#plotting a histogram
x = np.array(justlength, np.int32)
x = x/60000.0
plt.hist(x, bins = 200)
plt.title('Track Duration Count')
plt.xlabel('Track Duration')
plt.ylabel('Count')
plt.show()
#getting ride of outliers
#for length under 20 minutes
justshort = list()
for length in justlength:
    x = 20*60000.0
    if length<x:
        justshort.append(length)
print "Total number of songs under 20 minutes:", len(justshort)
x = np.array(justshort, np.int32)
x = x/60000.0
plt.hist(x, bins = 200)
plt.title('Track Duration Count (<20 minutes)')
plt.xlabel('Track Duration')
plt.ylabel('Count')
plt.show()
