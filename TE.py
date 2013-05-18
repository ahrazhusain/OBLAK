import re
import sys
import os



def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist



if len(sys.argv) < 2:
  print("Error: No start url was passed")
	sys.exit()


def total_urls():
    # Open a file
    fo = open("est.xml", "r")
    url = fo.read();

    # Close opend file
    fo.close()

    urls=int(url)+1
    urls=str(urls)
    print "Total URL's : ", urls
    #os.remove("est.xml")

    # Open a file
    fo = open("est.xml", "w")
    fo.seek(0,0)
    fo.write(urls);

    # Close opend file
    fo.close()

    
tags = sys.argv#"These are good times and I am | - rollin these a to"
#tags=tags.split()
url=sys.argv[1]
tags.remove(sys.argv[0])

tags.remove(url)


#print "URL: ", url
#print "TAGS: ",tags
#blah.remove(sys.argv[0])
#answer = re.sub(r'\w+:\s?','',blah)
#print answer

#blah=blah.split()


delete_list = "and I am are good these | - , . ' \" a to welcome home the is be of in that have it for not on with he as you do at this but his by from they we say her she or"
delete_list=delete_list.split()

c= cmp(tags, delete_list)

if c!=0:
    com= set(tags) & set(delete_list)
    #print com
    for n,i in enumerate(com):
          tags.remove(i)
          #print blah+i


#print tags
tags = ' '.join(tags)
tags=' '.join(unique_list(tags.split()))
tags=re.sub('[!@#$:-;,%*.\'1234567890]', '', tags);
print tags
total_urls()

scr="python OR.py "
scr=scr+url
scr=scr+" "
scr=scr+tags
#print "\n"
#print scr
os.system(scr)

