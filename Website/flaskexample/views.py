from flask import render_template
from flaskexample import app
from flask import request
import pandas as pd
from SimModel import SimilarityModel

@app.route('/')

@app.route('/index')
def index():
    return render_template("input.html")

@app.route('/output')
def cesareans_output():
  #pull 'birth_month' from input field and store it
  userinput = request.args.get('userinput')
  topicinput = request.args.get('topicinput')
  #SimilarityModel(userinput)
  #hikename = SimilarityModel(userinput)[0]
  #score = SimilarityModel(userinput)[1]
  result = SimilarityModel(userinput, topicinput)
  hikename = result[0]
  score = result[1]
  postext = result[2]
  posdate = result[3]
  posurl = result[4]
  imgname = result[5]
  topicinput = result[6]
  searchinput = result[7]
  return render_template("output.html", l1 = hikename, l2 = score, l3 = postext, l4 = posdate, l5 = posurl, l6 = imgname, l7 = topicinput, l8 = searchinput)
