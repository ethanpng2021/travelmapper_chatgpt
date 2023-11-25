# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request
import pandas as pd
import openai
import markdown
import ast
from flask_cors import CORS, cross_origin


openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app)



# Chat engine
def chat_with_chatgpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=600,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = response.choices[0].text.strip()
    return message


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        coord = [103.8146499, 1.36219165]

        df2 = [[103.6580253, 1.346533], [104.006950, 1.349143]]
        
        return render_template('index.html', df2=df2, origin=df2[0], midpt=coord)

    if request.method == 'POST':

        if request.form.get("textp") == "yes":

            text = request.form.to_dict(flat=True)
       
            add1 = "In the last paragraph, give the gps coordinates of each of these places in a Python dictionary."

            markdown_text_main = chat_with_chatgpt(text["textprompt"] + add1)
            html = markdown.markdown(markdown_text_main)

            listo = []
            keyo = []
            latlist = []
            lonlist = []
            coord = []

            try:

                ans = markdown_text_main.split("{")

                p1 = ans[1]

                pwhole = "{" + p1 

                print(pwhole)

                #dict1 = json.loads(pwhole)
                res_coord = ast.literal_eval(pwhole)

                print(res_coord, type(res_coord))   
                
                for key, value in res_coord.items():

                    print(key, value)

                    listo.append([value[1], value[0]])
                    keyo.append(key)
                    latlist.append(value[0])
                    lonlist.append(value[1])

                print(keyo, listo)

                print("latlist: ", latlist)
                print("lonlist: ", lonlist)

                lon_mid = sum(lonlist)/len(lonlist)

                print(lon_mid)

                lat_mid = sum(latlist)/len(latlist)

                print(lat_mid)

                coord = [lon_mid, lat_mid]

                print(coord)

            except:

                pass

            
            return render_template("index.html", out=html, df2=listo, origin=listo, midpt=coord)







if __name__ == "__main__":
   
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
    
