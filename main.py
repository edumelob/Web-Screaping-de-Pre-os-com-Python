import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def coletar_produtos(url: str):
    """Coleta o nome e o preço dos produtos de uma página HTML."""
    
    # Requisição HTTP
    resposta = requests.get(url)
    
    # Verificar se deu certo
    if resposta.status_code != 200:
        print("Erro ao acessar a página:", resposta.status_code)
        return []
    
    # Parse do HTML
    soup = BeautifulSoup(resposta.text, "html.parser")
    
    # Seleciona os produtos — aqui você adapta ao site real
    itens = soup.select(".product")  # exemplo de classe
    
    lista_produtos = []
    
    for item in itens:
        nome = item.select_one(".product-name").get_text(strip=True)
        preco = item.select_one(".product-price").get_text(strip=True)
        
        lista_produtos.append({
            "nome": nome,
            "preco": preco
        })
    
    return lista_produtos


def salvar_json(dados, arquivo="produtos.json"):
    """Salva os dados coletados em um arquivo JSON."""
    
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump({
            "atualizado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "quantidade": len(dados),
            "produtos": dados
        }, f, indent=4, ensure_ascii=False)
    
    print(f"Arquivo '{arquivo}' salvo com sucesso.")


if __name__ == "__main__":
    url = "https://exemplo.com/produtos"  # coloque um site real
    
    print("Coletando informações...")
    produtos = coletar_produtos(url)
    
    if produtos:
        salvar_json(produtos)
    else:
        print("Nenhum produto encontrado.")
