from flask import Flask, app, json, render_template, request
import numpy as np
from geopy.distance import geodesic
from sympy import symbols
from scipy.interpolate import interp1d
import scipy.integrate

a2 = np.load('Limite izquierda.npy')
b2 = np.load('limite derecha.npy')
#############|Derecha|#########

y0=0

def clear(x, y): 
    cx = []
    cy = []
    for i in range(len(x)):
        cx.append(x[i][0].km)
        cy.append(y[i][0].km)
    return cx, cy
#######################
def corres(cord):
    x=[]
    y=[]
    global y0
    lat = cord[0]
    lng = cord[1]
    if y0==0:
        y0=lat
    disy=[]
    disx=[]
    for i in range(len(a2)):
        disy.append(geodesic(b2[i],[lat, lng]))
    
    x.append(geodesic([y0, lng],[lat, lng]))
    y.append(min(disy))
    disy=[]
    disx=[]
    return (x),(y) 
#########################                                                     
def grafico(x,y):
    ecu =interp1d(x, y) 
    return ecu
######################
def integral(ecu, limit):
    x  = symbols('x')
    f = ecu
    ar=(scipy.integrate.quad(f, min(limit), max(limit)))
    return ar
#######################
coords=[]
def area(coord):
    global y0
    global coords
    disy=[]
    disx=[]
    marker=[]
    for i in range(len(coord)):
        dx, dy = corres(coord[i]['coordenadas'])
        marker.append(coord[i]['coordenadas'])
        disx.append(dx)
        disy.append(dy)
    disx, disy = clear(disx,disy)
    ecu = grafico(disx, disy)
    area = integral(ecu, disx)
    y0=[]
    marker=[]  
    return area[0] 

app = Flask(__name__) 

@app.route('/')
def index():
    return render_template('mapamark.html')

@app.route('/GetData')
def getdata():
    j = {'1':a2.tolist(),
          '2':b2.tolist()
          }
    return j

@app.route('/SendData', methods=['POST'])
def SendData():
    ar = 0
    output = request.get_json()
    result = json.loads(output) 
    ar = area(result['coordenadas'])
    result=[]
    return str(ar)

if __name__ == '__main__':
    app.run(debug=True)
    