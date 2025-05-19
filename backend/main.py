import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')

def obter_distancia_google(origem, destino):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origem,
        "destinations": destino,
        "key": API_KEY,
        "mode": "driving",
        "language": "pt-BR",
        "region": "br"
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        distancia_metros = data['rows'][0]['elements'][0]['distance']['value']
        distancia_km = distancia_metros / 1000
        return distancia_km
    except (KeyError, IndexError):
        return None

def calcular_custo_viagem(distancia_km, autonomia_km_litro, preco_combustivel):
    litros = distancia_km / autonomia_km_litro
    custo = litros * preco_combustivel
    return litros, custo

def main():
    origem = input("Digite o endereço de ORIGEM: ")
    destino = input("Digite o endereço de DESTINO: ")
    autonomia = float(input("Digite a autonomia do veículo (km por litro): "))
    preco = float(input("Digite o preço do combustível (R$/litro): "))
    distancia_km = obter_distancia_google(origem, destino)

    if distancia_km is None:
        print("Não foi possível obter a distância. Verifique os endereços.")
        return

    litros, custo = calcular_custo_viagem(distancia_km, autonomia, preco)

    print(f"Distânia: {distancia_km:.2f} km")
    print(f"Combustível necessário: {litros:.2f} litros")
    print(f"Custo estimado: R$ {custo:.2f}")

if __name__ == "__main__":
    main()
