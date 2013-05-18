import sys
import re
import os
import socket
import urllib
import urllib2
import json
import unicodedata
import psycopg2
import tldextract
from tldextract import extract


con = None


def cutit(s,n):    
   return s[n:]

def check_keyword(keyword):
           
                try :
                     con = psycopg2.connect(host=$host,database=$db',user=$user,password=$pass)
                     cur = con.cursor()
                     cur.execute("select * from information_schema.tables where table_name=%s", (keyword,))
                     val = bool(cur.rowcount)
                     #print cur.rowcount
                     con.commit()
                     return cur.rowcount
                    
                except psycopg2.DatabaseError, e:
                    
                          if con: 
                            con.rollback()
                    
                            print 'Error %s' % e    
                    #sys.exit(0)
                    
                    
                finally:
                    
                    if con:
                        con.close()

                return 0
                
                       

def new_keyword(keyword):

                quer="CREATE TABLE "
                quer=quer+keyword
                quer=quer+"(id INT , url TEXT PRIMARY KEY, orank INT, otags TEXT, lati TEXT, longi TEXT, timestamp timestamp with time zone default current_timestamp)"
                #print "Query:",quer

                try:
                            con = psycopg2.connect(host=$host,database=$db',user=$user,password=$pass)    
                            cur = con.cursor()
                            cur.execute(quer)
                            con.commit()
                except psycopg2.DatabaseError, e:
                   print 'Error %s' % e  
                    


               
                con = psycopg2.connect(host=$host,database=$db',user=$user,password=$pass)   
                cur = con.cursor()
                cur.execute("select * from o_main_index_9716248472_o")
                con.commit()
                i=int(cur.rowcount)
                i=i+1
                #print "id : ",i
                query = "INSERT INTO o_main_index_9716248472_o (id, keyword, k) VALUES ("
                query=query+str(i)
                query=query+",'"
                keyword = keyword.replace("_", "")
                query=query+keyword
                query=query+"',1)"
                #print query
                try:
                    cur.execute(query)
                    con.commit()
                except psycopg2.DatabaseError, e:
                   print 'Error %s' % e  

                if con: 
                       con.rollback()
                       con.close()

                return 0


def new_entry(table,url,orank,tmp,u,lati,longi):

    

    con = None

    try:
         
        con = psycopg2.connect(host=$host,database=$db',user=$user,password=$pass)
        cur = con.cursor()
        quer="select * from "
        quer=quer+table
        
        cur.execute(quer)
        con.commit()
        id=cur.rowcount
        tmp= ' '.join(tmp)
        if u!=0:
            #print "OLD entry id: ",id
            id=int(id)+1
            #print "INCR!!"
        #print "U is: ",u    
        print "entry id: ",id


        data = (id, url, orank, tmp,lati,longi)
        query = "INSERT INTO "
        query=query+table
        query=query+" (id, url, orank,otags,lati,longi) VALUES ("
        query=query+str(data[0])
        query=query+",'"
        query=query+str(data[1])
        query=query+"',"
        query=query+str(data[2])
        query=query+",'"
        query=query+str(data[3])
        query=query+"','"
        query=query+str(data[4])
        query=query+"','"
        query=query+str(data[5])
        query=query+"')"
        #print query
        cur.execute(query)
        con.commit()
        if u==1:
            quer1="UPDATE o_main_index_9716248472_o SET k = "
            quer1=quer1+str(id)
            quer1=quer1+" WHERE keyword = '"
            table = table.replace("_", "")
            quer1=quer1+table
            quer1=quer1+"'"
            #print quer1
            try:
               cur.execute(quer1)
               con.commit()
            except psycopg2.DatabaseError, e:
                       print 'Error %s' % e      
            con.commit()
        

    except psycopg2.DatabaseError, e:
        
        if con:
            con.rollback()
        
        print 'Error %s' % e    
        sys.exit(1)
        
        
    finally:
        
        if con:
            con.close()

    return 0
                



def check_ambiguity(table,url,otags):
    

    con = None

    try:
         
        con = psycopg2.connect(host=$host,database=$db',user=$user,password=$pass)
        cur = con.cursor()
        

        query = "select * from "
        query=query+table
        query=query+" where url like '"
        query=query+str(url)
        otags= ' '.join(otags)
        query=query+"'"
        
        #print query
        cur.execute(query)
        con.commit()
        #print "Already?:",cur.rowcount
        x=cur.rowcount

    except psycopg2.DatabaseError, e:
        
        if con:
            con.rollback()
        
        print 'Error %s' % e    
        sys.exit(1)
        
        
    finally:
        
        if con:
            con.close()

        if x ==0:
            return 0
        
    return 1


def process(tags,url,orank):
        # tags="Ahraz Husain Rules!"

         #tags=tags.split()
         temp=tags

         for tag in list(tags):
            tmp=temp
            
            rem=tag
            tmp.remove(rem)
            print "Tag:",tag
            print 'Otags: ',tmp
            # ---------------MAIN PROCESSING -------------#

            urly= tldextract.extract(url);#cutit(url, 7);
            urlx=urly[1]+"."+urly[2];
            print "URL is -> "+urlx;
            ipadd=socket.gethostbyname(urlx);
            print "IP Address: "+ipadd;

            query='http://api.ipinfodb.com/v3/ip-city/?key=15e84bd5b21c4c7f60891aca3d15e4abed290374dfd8a6386b4c0e62789154c1&ip='+ipadd+'&format=xml'
            response = urllib.urlopen(query).read()

            #print(response)
            
            from xml.dom.minidom import parseString
            dom = parseString(response)
            lati = dom.getElementsByTagName('latitude')[0].childNodes[0].data
            longi= dom.getElementsByTagName('longitude')[0].childNodes[0].data
            reg= dom.getElementsByTagName('regionName')[0].childNodes[0].data
            print "Latitute:"+lati;
            print "Longitute"+longi;
            print "Region:"+reg
            
            h = lati.decode('utf-8')
                    
            tag=tag+"_"
            print "Keyword",tag," exists: ",bool(check_keyword(tag))
            u=1
            if check_keyword(tag)==0:
                u=0
                new_keyword(tag)
            if check_ambiguity(tag,url,tmp)==0:
                new_entry(tag,url,orank,tmp,u,lati,longi)

            
            tmp.append(rem)

         return






if len(sys.argv) < 2:
  print("Error: No start url was passed")
	sys.exit()


tags = sys.argv
#blah=blah.split()
url=sys.argv[1]
orank=sys.argv[2]
#print "OR: ",orank

tags.remove(orank)
tags.remove(url)
tags.remove(sys.argv[0])

print "SE"
print "URL: ", url
print "TAGS: ",tags
print "O-Rank:",orank
process(tags,url,orank)


    
 

