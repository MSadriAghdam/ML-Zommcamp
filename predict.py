import pickle
import pandas as pd
from flask import Flask
from flask import request
from flask import jsonify
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


model_file = 'model_C=1.0.bin'
df_final = pd.read_pickle("df_final.plk")
with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)



app = Flask('predict')

@app.route('/predict', methods=['POST'])
def predict():
    prediction = model.predict(df_final)
    df_final['Cluster'] = prediction+1
    return plot_png()

def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    fig = plt.scatter(x=df_final["income"], y=df_final["expences"],
            c=df_final["Cluster"], s = 20 , cmap='viridis')
    plt.xlabel('Income')
    plt.ylabel('Expenses')
    plt.show()
    return fig

            
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)