#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Description: Create a BioConda Database Search Console
"""

from bs4 import BeautifulSoup

import requests

import sqlite3

def extractBioCondaData(numberOfPages, conn, c):
    
    for j in range(1,numberOfPages+1):
        
        while True:  
            r  = requests.get("https://anaconda.org/bioconda/repo?page=" + str(j))
            if (r.status_code == 200):
                break
            
        data = r.text
                    
        soup = BeautifulSoup(data, 'lxml')      
                            
        y = [x.extract() for x in soup.find_all('tr')]
                
        names = []
        
        status = []
        
        description = []
        
        last_update = []
        
        all_data = []
        
        for i in y:
            print(str(i.span).replace('<span class="packageName">',"").replace("</span>",""))
            for data in i.find_all("td"):
                all_data.append(data.get_text().replace("\n", "").strip())
            names = all_data[0::4]
            status = all_data[1::4]
            description = all_data[2::4]
            last_update = all_data[3::4]
    
        print(names)
        print(status)
        print(description)
        print(last_update)
        
        for i in range(0,len(names)):
            c.execute("INSERT INTO bioCondaPackageRepository VALUES (?, ?, ?, ?)",(names[i], status[i], description[i], last_update[i]))            

        conn.commit()
        
        print(j)
        
def main(): 
    
    conn = sqlite3.connect('bioCondaPackageRepository.db') 
    
    c = conn.cursor()
    
    c.execute('''CREATE TABLE bioCondaPackageRepository(Package Name, Access, Summary, Updated)''') 
 
    extractBioCondaData(165,conn,c) # BioConda Data Forum - # please insert the current number of pages
    
    conn.close()
    
main()


