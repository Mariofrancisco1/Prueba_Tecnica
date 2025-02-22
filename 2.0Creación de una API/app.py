from flask import Flask, request, jsonify

class ConjuntoNumeros:
    def __init__(self):
        self.numeros = list(range(1, 101))  
        self.numero_extraido = None

    def extract(self, numero):
        # Validación de entrada
        if not isinstance(numero, int):
            return "El número debe ser un entero."
        if numero <= 0 or numero > 100:
            return "El número debe ser mayor que 0 y menor o igual a 100."

        # Extraer el número
        if numero in self.numeros:
            self.numeros.remove(numero)
            self.numero_extraido = numero
            return True  
        else:
            return "El número no está en el conjunto."
    
    def calcular_extraido(self):
     
        conjunto_completo = set(range(1, 101))
        conjunto_actual = set(self.numeros)
        faltante = conjunto_completo - conjunto_actual
        return faltante.pop() if faltante else None

app = Flask(__name__)

@app.route('/extraer', methods=['POST'])
def extraer_numero():
    data = request.get_json()

    if 'numero' not in data:
        return jsonify({"error": "Falta el parámetro 'numero'."}), 400

    numero = data['numero']
    conjunto = ConjuntoNumeros()
    
    # Extraemos el número indicado
    resultado = conjunto.extract(numero)
    
    if resultado is True:
        # Calculamos el número faltante
        numero_faltante = conjunto.calcular_extraido()
        return jsonify({
            "numero_extraido": numero,  
            "numero_faltante": numero_faltante, 
            "resultado": f"Número extraído: {numero}"
        })
    else:
        return jsonify({"error": resultado}), 400

if __name__ == '__main__':
    app.run(debug=True)
