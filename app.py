import requests
from flask import Flask, render_template, request

app = Flask(__name__)

keys = {
	"value1": "5a55de396be770d56804a34d6c586360"
}

@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template("index.html")
	else:
		email = request.form["username"]
		key = keys.get(request.form["key"])
		r = requests.get(f"https://myrz.org/api/email_search.php?key={key}&email={email}")
		results = ""
		if '"success":true' in r.text:
			for i in r.json()["results"]:
				results += i["line"] + "\n"
			return render_template("result.html", results=results, total=r.json()["resultCount"])

		elif '"resultCount":0' in r.text:
			message = "Not Found"
		elif 'Введите корректный email или логин для поиска':
			message = "Enter a valid email address"
		else:
			message = "Unknown Error"

		return render_template("index.html", message=message)


if __name__ == '__main__':
	app.run(debug=True)