from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_cors import CORS
import requests
import datetime
import csv

app = Flask(__name__)
CORS(app)  #Por el error CORS policy: No 'Access-Control-Allow-Origin'

def timeAct():
    hora=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hora=str(hora)
    return hora

def saveData():
    time=timeAct()
    with open('./archivos/sensor.csv', 'r', newline='') as sensor:  #with open: context manager; newline: Quitar espacio en blanco
        
        reader=csv.reader(sensor)
        for x, row in enumerate(reader):
            if x==0:
                continue  #como es la cabecera no haga nada

        with open('./archivos/sensor.csv', 'a', newline='') as sensor:        
            writer = csv.writer(sensor)
        
            writer.writerow((time,valor,valor2))

@app.route('/sensor', methods = ['POST', 'GET'])
def valorSensor():
    global valor, valor2  
    
    
    if request.method=='GET':
        
        
        print("Estas enviando un valor por el metodo GET")
        valor=request.args.get('value')
        valor2=request.args.get('value2')
        saveData()
        
        
        print(type(valor))
      
        #num=request.args.get('num')
        print(f'El valor enviado por el cliente es {valor} y {valor2}')      
        
               
        
    if request.method=='POST':
        print("Estas enviando un valor por el metodo POST 1")
        #dato=request.get_json() #recibe como parametro la clave del dato a pedir
        #dato=request.args
        dato = request.get_json()
        #print(type(dato))
        print(type(dato))
        print(dato['temp'])
        

    return 'Valor enviador por el servidor Flask'
    
@app.route('/valorSensor', methods = ['POST', 'GET'])
def consulta():
    hora=timeAct()
    global stateLed
    if request.method=='GET':
        return render_template('dashboard.html', value=valor, value2=valor2, hour=hora)



    if request.form['submit']=='Encender':
        print("Led encendido")
        #return redirect( url_for('turn_on') )
        stateLed=True
        return redirect(request.url)  

            

    elif request.form['submit']=='Apagar':
        print('Led apagado')
        #return redirect( url_for('turn_off') )
        stateLed=False
        return redirect(request.url)

    else:
        pass

@app.route('/update')
def update():
    tiempo=timeAct()
    sensores={'valor1':valor, 'valor2':valor2, 'valor3':tiempo}
    return sensores

    
@app.route('/stateLed')
def stateLed():
    print("Cliente verificando estado de led")
    if stateLed:
        return 'on'
    return 'off'
    


@app.route('/', methods = ['POST', 'GET'])
def sensor():
    autor="Servidor IoT"
    sensor=75

    if request.method=='GET':
        print("Estas enviando un valor por el metodo GET")
        valor=request.args.get('value')
        num=request.args.get('num')
        print(f'El valor enviado por el cliente es {valor} y es {num}')
        

    if request.method=='POST':

        print("Estas enviando un valor por el metodo POST 2")
        #dato=request.get_json() #recibe como parametro la clave del dato a pedir
        
        #print(dato)
        if request.form['submit']=='Turn On':
            print("Led encendido")
            

        elif request.form['submit']=='Turn Off':
            print('Led apagado')

        else:
            pass


    return render_template('dashboard.html',author=autor, value=sensor)

@app.route('/encender', methods=['GET'] )
def turn_on():
    # turn on LED on arduino
    print("Encender desde la web")
    
    return 'on'


@app.route('/apagar', methods=['GET'] )
def turn_off():
    # turn off LED on arduino
    print("Apagar desde la web")
    return 'off'

@app.route('/json-example', methods=['POST'])
def json_example():
    data = request.get_json() #Json lo convierte en un diccionario de Python

    language = data['language']
    framework = data['framework']

    print(f'El framework es {framework}')
    print(type(data))

    # two keys are needed because of the nested object
    python_version = data['version_info']['python']

    # an index is needed because of the array
    example = data['examples'][1]
    print(f'El valor del array es {example}')

    boolean_test = data['boolean_test']

    return 'JSON Object Example'

@app.route('/download/<documento>')
def download(documento):
    #path=r'C:\Users\jhorv\OneDrive\Documentos\IoT\Servidor Flask\servidor\static\client\csv\sensor.csv'
    #path=r'C:\Users\jhorv\OneDrive\Documentos\IoT\Servidor Flask\servidor\static\client\csv'
    path=r'C:\Users\jhorv\OneDrive\Documentos\IoT\Servidor Flask\Server2\archivos'
    #return send_file(path,filename=documento, as_attachment=False)
    return send_from_directory(path,filename=documento, as_attachment=False, cache_timeout=0) #cache_timeout: para evitar que cargue desde cache
    #return send_from_directory(path, attachment_filename ='sensor.csv', as_attachment=True)

if __name__=='__main__':
    app.run(host='0.0.0.0')  # ip=0.0.0.0 convertir el servidor publico