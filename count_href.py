def parser(html_string):
# split html string into lines
    file = open(html_string, "r")
    lines = file.readlines()
    file.close
# count number href tags in lines
    count_href = 0
    for line in lines:
        line = line.strip()
        if line.find("href") != -1:
            count_href = count_href + 1

# print number of href
    print(count_href)
