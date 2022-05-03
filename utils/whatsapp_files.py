import sys
import numpy as np
import re
from datetime import datetime
import pandas as pd

# https://regex101.com/
def startsWithDateTime(s):
    # pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]):([0-9][0-9]) -' #ingles?
    #pattern = '^([0-2][0-9]|[0-9]|(3)[0-1])(\/)(([0][0-9])|[0-9]|((1)[0-2]))(\/)(\d{2}|\d{4}) ([0-9][0-9]|[0-9]):([0-9][0-9]|[0-9]) ([ap]\. m\.) -'
    pattern = '^([0-2][0-9]|[0-9]|(3)[0-1])(\/)(([0][0-9])|[0-9]|((1)[0-2]))(\/)(\d{2}|\d{4}) ([0-9][0-9]|[0-9]):([0-9][0-9]|[0-9]) (.*) -'
    result = re.match(pattern, s)
    if result:
        return True
    return False

def startsWithAuthor(s):
    patterns = [
        '([\w]+):',                        # First Name
        '([\w]+[\s]+[\w]+):',              # First Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
        '([+]\d{2} \d{5} \d{5}):',         # Mobile Number (India)
        '([+]\d{2} \d{3} \d{3} \d{4}):',   # Mobile Number (US)
        '([+]\d{2} \d{4} \d{7})',           # Mobile Number (Europe)
        '([+]\d{2} \d{1} \d{2} \d{4}-\d{4})'# Argentina: +54 9 11 4565-4578:
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False

def getDataPoint(line):
    # line = 18/06/17, 22:47 - Loki: Why do you have 2 numbers, Banner?
    splitLine = line.split(' - ')# splitLine = ['18/06/17, 22:47', 'Loki: Why do you have 2 numbers, Banner?']
    d = splitLine[0].encode("ascii", "ignore").decode()
    d = re.sub("a.m.", "AM", d)
    d = re.sub("p.m.", "PM", d)
    format = '%d/%m/%Y %I:%M %p'
    date_time = datetime.strptime(d, format) # date = '18/06/17'; time = '22:47'
    format = '%Y-%m-%d'
    date = date_time.strftime(format)
    message = ' '.join(splitLine[1:]) # message = 'Loki: Why do you have 2 numbers, Banner?'
    #print(message)
    if startsWithAuthor(message): # True
        splitMessage = message.split(': ') # splitMessage = ['Loki', 'Why do you have 2 numbers, Banner?']
        author = splitMessage[0] # author = 'Loki'
        message = ' '.join(splitMessage[1:]) # message = 'Why do you have 2 numbers, Banner?'
    else:
        author = None
    return date, date_time, author, message

def read_whatsapp_file(wpath):
    parsedData = [] # List to keep track of data so it can be used by a Pandas dataframe
    with open(wpath, encoding="utf-8") as fp:
        fp.readline() # Skipping first line of the file (usually contains information about end-to-end encryption)
            
        messageBuffer = [] # Buffer to capture intermediate output for multi-line messages
        date, date_timetime, author = None, None, None # Intermediate variables to keep track of the current message being processed
        
        while True:
            line = fp.readline() 
            if not line: # Stop reading further if end of file has been reached
                break
            line = line.strip() # Guarding against erroneous leading and trailing whitespaces
            if startsWithDateTime(line): # If a line starts with a Date Time pattern, then this indicates the beginning of a new message
                if (len(messageBuffer) > 0) and (author!=None): # Check if the message buffer contains characters from previous iterations
                    parsedData.append([str(date), str(date_time), author, ' '.join(messageBuffer), 0]) # Save the tokens from the previous message in parsedData
                messageBuffer.clear() # Clear the message buffer so that it can be used for the next message
                date, date_time, author, message = getDataPoint(line) # Identify and extract tokens from the line
                #print('DateTime ' + str(date_time) + ' Autor ' + str(author) + ' Mensaje ' + message)
                messageBuffer.append(message) # Append message to buffer
            else:
                messageBuffer.append(line) # If a line doesn't start with a Date Time pattern, then it is part of a multi-line message. So, just append to buffer
    df = pd.DataFrame(parsedData, columns=['Date','DateTime', 'Author', 'Message', 'contact_id'])
    return df

def main():
    print("whatsapp_files!!")
    if (len(sys.argv)<2):
        return
    args = sys.argv[1:]
    df = read_whatsapp_file(args[0])
    contacts = df['Author'].unique()
    print(len(contacts))
    grupo = "LEONXIII"

    import sqlite3
    from sqlite3 import Error
    try:
        nlpdb = sqlite3.connect('db.sqlite3')
    except Error as e:
        print(e)
        return
    nlpdb.execute('INSERT INTO whatsapp_whatsappgroup(name) VALUES(?)', [grupo]);
    nlpdb.commit()
    nlpdb.close()

    nlpdb = sqlite3.connect('db.sqlite3')
    for c in contacts:
        print(c)
        nlpdb.execute("INSERT INTO Contact(name) VALUES(?)", [c]);
    nlpdb.commit()
    nlpdb.close()

    #df['contact_id']=0
    print(df.shape)
    i=1
    for c in contacts:
        #df[df['Author']==c, 'contact_id']=i
        for x in range(0, df.shape[0]):
            if df['Author'][x]==c:
                df.loc[x, 'contact_id']=int(i)
        i = i + 1 

    nlpdb = sqlite3.connect('db.sqlite3')
    for c in range(0, df.shape[0]):
        nlpdb.execute("INSERT INTO WhatsApp(contact_id, whatsappgroup_id, dt_message, message) VALUES(?,?,?,?)", [int(df['contact_id'][c]), 1, df['DateTime'][c], df['Message'][c]]);
        #print(df['contact_id'][c], 1, df['DateTime'][c], df['Message'][c])
    nlpdb.commit()
    nlpdb.close()

if __name__ == "__main__":
    main()