from flask import Flask, render_template, url_for, request
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

def data_cleanup(array):
	L = []
	for i in array:
		i = i.replace("+","")
		i = i.replace("-","")
		i = i.replace(",",".")
		if i == "":
			i = "0"
		L.append(i.strip())
	return L

@app.route("/")
def index():
	
	r = requests.get("https://www.worldometers.info/coronavirus/")
	content = r.content
	soup = BeautifulSoup(content, "html.parser")
	numberlist = []
	for span in soup.find_all("div", class_="maincounter-number"):
		numberlist.append(span.get_text())
	country = "USA"
	data_check= []
	worldmetersLink = "https://www.worldometers.info/coronavirus/"
		
	while True:
		try:
			html_page = requests.get(worldmetersLink)
		except requests.exceptions.RequestException as e: 
			print (e)
			continue
		bs = BeautifulSoup(html_page.content, 'html.parser')

		search = bs.select("div tbody tr td")
		start = -1
		for i in range(len(search)):
			if search[i].get_text().find(country) !=-1:
				start = i
				break
			
		data = []
		for i in range(1,8):
			try:
				data = data + [search[start+i].get_text()]
			except:
				data = data + ["0"]



		print("before :-----------------------------------------")
		print(data)
		data= data_cleanup(data)
		print("after :------------------------------------------")
		print(data)



		message = "Total infected = {}, New Case = {}, Total Deaths = {}, New Deaths = {}, Recovred = {}, Active Case = {}, Serious Critical = {}".format(*data)
		

		obj = {"cases":numberlist[0],
				"deaths": numberlist[1],
				"recoverd": numberlist[2]}
		
		return render_template("covid.html",  obj = obj, message=data, country=country)


@app.route("/country", methods = ["GET", "POST"])
def api():
	error="North America"
	if request.method == "POST":
		country = request.form.get("country")
		print(country)
		r = requests.get("https://www.worldometers.info/coronavirus/")
		content = r.content
		soup = BeautifulSoup(content, "html.parser")
		numberlist = []
		for span in soup.find_all("div", class_="maincounter-number"):
			numberlist.append(span.get_text())
		
		data_check= []
		worldmetersLink = "https://www.worldometers.info/coronavirus/"
			
		while True:
			try:
				html_page = requests.get(worldmetersLink)
			except requests.exceptions.RequestException as e: 
				print (e)
				continue
			bs = BeautifulSoup(html_page.content, 'html.parser')

			search = bs.select("div tbody tr td")
			start = -1
			for i in range(len(search)):
				if search[i].get_text().find(country.capitalize()) !=-1:
					start = i
					break
				
				
			data = []
			for i in range(1,8):
				try:
					data = data + [search[start+i].get_text()]
				except:
					data = data + ["0"]



			print("before :-----------------------------------------")
			print(data)
			data= data_cleanup(data)
			print("after :------------------------------------------")
			print(data)



			# message = "Total infected = {}, New Case = {}, Total Deaths = {}, New Deaths = {}, Recovred = {}, Active Case = {}, Serious Critical = {}".format(*data)
			

			obj = {"cases":numberlist[0],
					"deaths": numberlist[1],
					"recoverd": numberlist[2]}
			
			return render_template("covid.html",  obj = obj, message=data, country=country,error=error)
	else:
		return"ERROR"
	return render_template("covid.html",  obj = obj, message=data, country=country,error=error)
if __name__ == "__main__":
	app.run()