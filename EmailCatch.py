import re

def catch_email(website): #website is html String
    # variable def
    email_list = []

    # collect email that is linked
    file = open(website, "r")
    lines = read.lines()
    file.close

    # iterate through lines looking for '@'
        match = re.search('(?=.com|.cn|.io)href', website)
