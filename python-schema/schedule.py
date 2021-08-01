import re

def hourify(strTime):
	arr = strTime.split(".")
	return float(arr[0])+float(arr[1])/60.0

class Post:
	def __init__(self,arr):
		times = arr[0].split("-")
		print(times)
		self.start = times[0]
		self.end = times[1]
		self.hour = hourify(times[0])
		self.hourEnd = hourify(times[1])
		
		if(arr[1]=="Handledningstid"):
			self.tutor = arr[2]
			self.handledning = True
		else:
			self.tutor = arr[4][1:-1]
			self.klass = arr[1]
			self.room = arr[3]
			self.handledning = False

	def print(self):
		if self.handledning:
			print(self.start + " <-> " + self.end + " Handledning")
		else:
			print(self.start + " <-> " + self.end + " " + self.klass + " i " + self.room)

posts = []
p = re.compile('Måndag|Tisdag|Onsdag|Torsdag|Fredag');

f = open("data", encoding="utf-8", mode="r")
for line in f:
	lineshort = line.strip()
	if p.search(lineshort):
		posts.append( [] )
	else:
		data = lineshort.split(" ")
		if len(data) > 1:
			post = Post(data)
			posts[-1].append(post)


height_per_hour=80
number_of_hours=7
start_hour=8
left = 10
width = 16
top_margin=30

s = "<style> div.post { background-color: #3df; border: black 1px SOLID; font-family: verdana; font-size: 11px} div.inner {margin: 5px; } div.line { border-bottom:#aaa 1px SOLID; width:100%; height:"+str(height_per_hour)+"px; position:absolute; left:"+str(0)+"px; font-family: verdana; font-size: 10px; color: #aaa} div.shade {position:absolute; background-color: #eee; height:"+str(height_per_hour*number_of_hours)+"px; width:"+str(width)+"%; top:"+str(top_margin)+"px;} div.day {text-align: center; position:absolute; top:8px; width:"+str(width)+"%; vertical-align:bottom; color:aaa; height:"+str(top_margin)+"px;}</style>"

colors = ["#fdb","#dfb","#bdf","#fbd","#bfd","#dbf"]
colorId = 1
colorDict = {}
days = ["Måndag","Tisdag","Onsdag","Torsdag","Fredag"]

for pos in range(0,5):
	s += "<div class=\"day\" style=\"left:"+str(left+pos*width)+"%;\">"+days[pos]+"</div>"
	if pos%2==0:
		s += "<div class=\"shade\" style=\"left:"+str(left+pos*width)+"%;\"></div>"

	s += "<div style=\"border-bottom: #aaa 1px SOLID; width: 100%; height:"+str(top_margin)+"px; position:absolute; top:0px; left:0px;\"></div>"
for pos in range(0,number_of_hours):
	s += "<div class=\"line\" style=\"top:"+str(top_margin+pos*height_per_hour)+"px;\">"+str(pos+start_hour)+":00</div>"

for day in posts:
	for post in day:
		
		start = post.hour - start_hour
		end = post.hourEnd - start_hour
		height = (end-start)*height_per_hour
		top = top_margin+start*height_per_hour
		info = ""
		color = ""
		if post.handledning:
			info = "Handledning " + post.tutor
			color = colors[0]
		else:
			info = post.room + " " + post.klass
			if not post.klass in colorDict:
				colorDict[post.klass]=colors[colorId]
				colorId+=1
			color = colorDict[post.klass]
		
		print(str(post.hour) + " " + str(post.hourEnd) + " " + str(start) + " " + str(end))
		s += "<div class=\"post\" style=\"background-color:"+color+"; position:absolute; width:"+str(width)+"%; height:"+str(height)+"px; top:"+str(top)+"px; left:"+str(left)+"%;\"><div class=\"inner\">"+post.start+"-"+post.end+"<br />"+info+"</div></div>\n"
	left += width
	
f = open("output.html","w")
f.write(s)
f.close()