from flask import Flask, render_template_string, request, json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    try:
        if request.method == 'POST':
            vals = request.form.getlist('values')
            valuew = float(vals[0])
            Valuetwo = float(vals[1])
            result = valuew + Valuetwo 
            multipi = valuew * Valuetwo      
            divi =  valuew / Valuetwo  
            subt = valuew - Valuetwo 
        else:
            valuew =''
            Valuetwo = ''
            result = ''
            multipi = ''
            divi = ''
            subt = '' 
        return render_template_string('''<!DOCTYPE html>    
<html lang="en"> 
<head>
    <title>Harold's Python Page</title>  
    <link type="text/css" rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
 <div class="container">
      <table class=Main1 width="100%" align="left">
        <tr>
            <th><a href="index.html">Home</a>|
        </tr>
        <tr>
            <td>                         
               <h1>Harold's Python Page</h1>
   <form action='/' method='POST'>
	<p>Value 1:<input type="number" name="values" value="{{valuew}}">	
    <p>Value 2: <input type="number" name="values" value="{{Valuetwo}}">
 	<p><button type=''submit''> Calculate </button>
    <p>Multpication: <input type="number" name="multipi_dc" value="{{ multipi }}"></p>
    <p>Division: <input type="number" name="divi_dc" value="{{ divi }}"></p>    
    <p>Additon: <input type="number" name="result_dc" value="{{ result }}"></p>    
    <p>Subtraction: <input type="number" name="subt_dc" value="{{ subt }}"></p>
</form></td></tr>
    </table>''',result=result,multipi=multipi,valuew=valuew
    ,Valuetwo=Valuetwo,divi=divi,subt=subt)
    except ZeroDivisionError as error:
        return "Zero division is not allowed in Python Jackass"
    except:
        return "Fatal Error"

if __name__ == '__main__':
        app.run(host='127.0.0.1', port=8080, debug=True)
