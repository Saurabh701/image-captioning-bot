from flask import Flask ,render_template,redirect ,request 

##import single_caption as sc
# __name __ == __main__
app = Flask(__name__)

@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/', methods= ['POST'])
def cap():
	if request.method == 'POST':

		f = request.files['userfile']
		path = './static/{}'.format(f.filename)
		f.save(path)

		caption = sc.pred_img(path)
		##caption = 'test'
		
		

	return render_template("index.html",  your_result = result_dic )

if __name__=='__main__':
	app.run(threaded=False)
