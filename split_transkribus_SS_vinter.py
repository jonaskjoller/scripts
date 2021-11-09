# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 21:51:21 2021

@author: jonas
"""
import re
import os

# =============================================================================
#Save temporarily stored text to a file
def save_temp():
    global file_counter, file_temp, file_name
    
    #Create file
    filename = directory[0] + str(file_counter).zfill(2) + '_' + descriptor[file_counter] + '.txt'
    filename_E = directory[1] + str(file_counter).zfill(2) + '_' + descriptor[file_counter] + '_E.txt'        
    filename_G = directory[2] + str(file_counter).zfill(2) + '_' + descriptor[file_counter] + '_G.txt' 
    filename_P = directory[3] + str(file_counter).zfill(2) + '_' + descriptor[file_counter] + '_P.txt'
    
    #Clean the file
    file_temp = file_temp.lower() #Lower case
    file_temp = re.sub('[/.:?]','',file_temp) #Remove special characters
    file_temp = re.sub('=\n','',file_temp) #Contract hyphenated words
    file_temp = re.sub('\n',' ',file_temp) #Substitute new line with space
    file_temp = re.sub(' +', ' ', file_temp)
    
    keyword_1 = 'evangelium skriffuer'
    keyword_2 = 'bønen'

    if file_counter == 16:
        pass
    elif file_counter == 27 or file_counter == 28:
        save_split(filename_E,file_temp,0,len(file_temp))
    elif file_counter == 29:
        save_split(filename_G,file_temp,0,len(file_temp))
    else:
        pos_1 = re.search(keyword_1,file_temp).start()
        counter = 0
        pos_2 = []
        for match in re.finditer(keyword_2,file_temp):
            counter += 1
            pos_2.append(match.start())
        
        
        save_split(filename_E,file_temp,0,pos_1)
        save_split(filename_G,file_temp,pos_1,pos_2[counter-1])
        save_split(filename_P,file_temp,pos_2[counter-1],len(file_temp))
        
    save_split(filename,file_temp,0,len(file_temp))
    
    file_counter += 1
    file_temp = ''
# =============================================================================        
def save_split(file,text,pos_1,pos_2):
    output = open(file,'w',encoding='utf-8')
    output.write(text[pos_1:pos_2])
    output.close
# =============================================================================            
descriptor = ['1SinAdv','2SinAdv','3SinAdv','4SinAdv','Christmas','StSteph','StJohn','1SafChr','NewYear',
              '1SaftNY','Epiph','1SaftEpi', '2SaftEpi','3SaftEpi','4SaftEpi','5SaftEpi','6SaftEpi',
              'MaryPur','Sept','Sexa','Lent','1SinLent','2SinLent','3SinLent','Laetare','SaftLat',
              'MaryAnnun','PalmSun','MaunThur','GoodFri']

directory = ['output_SS_vinter_SunFeast/','output_SS_vinter_Sermons_E/','output_SS_vinter_Sermons_G/','output_SS_vinter_Prayer/']

file_name = ''
file_counter = 0
file_temp = '' #Temporarily stores text for next file save

section_counter_pri = False #Switch for preparing a save after 'prayer' section
section_counter_sec = False #Switch for when a key term occurs multiple times before file save
    
file = open('Sabbati_Sanctificatio_Vinter_(Brochmand).txt','r',encoding='utf-8')
# =============================================================================

#Create directory
for i in range(4):
    try:
        os.mkdir(directory[i])
    except:
        pass

for line in file:
    #Main trigger
    if 'Amen' in line or 'AMEN' in line:
        if section_counter_pri == True:
            section_counter_pri = False
            file_temp += line
            save_temp()
        else:
            file_temp += line
    elif 'Bønen.\n' in line:
        section_counter_pri = True
        file_temp += line
    #Exceptions
    elif 'Paa Mariæ Renselsis\n' in line:
        save_temp()
        file_temp += line      
    elif 'Paa Skiertorsdag.\n' in line:
        if section_counter_sec == True:
            file_temp += line
        else:
            section_counter_sec = True
            save_temp()
            file_temp += line
    elif 'Paa Langfredag.\n' in line:
        if section_counter_sec == False:
            file_temp += line
        else:
            section_counter_sec = False
            save_temp()
            file_temp += line
    else:
        file_temp += line

save_temp() #Saves the last remaining file

file.close()