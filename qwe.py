#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, session
import subprocess as sp
import uuid
from os import path, makedirs


makedirs("codes", exist_ok=True)
makedirs("pdfs", exist_ok=True)
app = Flask(__name__)
app.secret_key = "hui"


def create_pdf(code, team, lang):
	filename = str(uuid.uuid4())
	open(path.join("codes", filename + ".txt"), "w").write(code)
	print("running enscript...")
	p = sp.run(["enscript", path.join("codes", filename + ".txt"), "-E" + lang, "-b", "{}: page $% of $=".format(team), "-C", "--color", "-o", path.join("pdfs", filename + ".pdf")])
	if p.returncode:
		print("error")
		print(p.stderr.decode())
	else:
		print("ok enscript ran successfully")
		print("filename is", filename)
		return path.join("pdfs", filename + ".pdf")


def print_file(filename):
	pass


def print_code(code, team, lang):
	filename = create_pdf(code, team, lang)
	if filename is None:
		return
	print_file(filename)


@app.route('/', methods=["GET", "POST"])
def index():
	if request.method == "POST":
		if request.form.get("code", ""):
			code = request.form.get("code", "")
			lang = request.form.get("lang")
			team = request.form.get("team")
			print_code(code, team, lang)
			session["lang"] = lang
			session["team"] = team
			session["state"] = "Printed!"
		return redirect(url_for('index'))
	state = session.get("state", "")
	if "state" in session:
		session.pop("state")
	lang = session.get("lang", "cpp")
	team = session.get("team", "")
	return render_template("index.html", state=state, lang=lang, team=team)

