import re
filePath="/home/aronzx/Desktop/Mail/test.eml"
f=open(filePath,"r")
num_lines = sum(1 for line in open(filePath,"r"))
url=f.read()
print num_lines
f.close()
urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
print len(urls)

print len(urls)/float(num_lines)

#for x in urls:
#	print x + '\n'
