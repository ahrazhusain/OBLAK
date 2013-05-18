import sys
import os
import re
import sched, time
import psycopg2


s = sched.scheduler(time.time, time.sleep)
i=0;
timedelay=10#in seconds



def run_script(url):
                    scr1="python OS.py "
                    scr1=scr1+url
                    print " url processed!\n"
                    os.system(scr1)

                    return 0;


def ocrawl(id):
            try :
                     con = psycopg2.connect(host='192.73.234.205',database='oblakdb',user='postgres',password='12345')
                     cur = con.cursor()
                     quer="select * from submissions where id="
                     quer=quer+str(id)
                     #print(quer)
                     cur.execute(quer)
                     rows = cur.fetchall()
                     """print "\nRows: \n"
                     for row in rows:
                         print "   ", row[0]
                     """    
                     val = bool(cur.rowcount)
                     url=rows[0][0]
                     #print "Url found:",url
                     
                     
                     quer1="DELETE FROM submissions WHERE id="
                     quer1=quer1+str(id)
                     #print(quer1)
                     cur.execute(quer1)
                     run_script(url)

                     con.commit()
                     

            except psycopg2.DatabaseError, e:
                    if con: 
                      con.rollback()
                    
                    print 'Error %s' % e    
                    #sys.exit(0)

            finally:
                    
                    if con:
                        con.close()
            return 0



def check_new():
           
                try :
                     con = psycopg2.connect(host='192.73.234.205',database='oblakdb',user='postgres',password='12345')
                     cur = con.cursor()
                     cur.execute("select * from submissions")
                     val = bool(cur.rowcount)
                     print "Unheeded urls found : ",val
                     con.commit()
                     if(cur.rowcount>0):
                        #print "Id: ", cur.rowcount;
                        ocrawl(cur.rowcount)
                    
                except psycopg2.DatabaseError, e:
                    
                          if con: 
                            con.rollback()
                    
                            print 'Error %s' % e    
                    #sys.exit(0)
                    
                    
                finally:
                    
                    if con:
                        con.close()

                return 0
            

def do_something(sc,i): 
    print "\nChecking..."
    # do your stuff
    i=i+1
    check_new();
          
    sc.enter(timedelay, 1, do_something, (sc,i))

s.enter(timedelay, 1, do_something, (s,i))
s.run()
