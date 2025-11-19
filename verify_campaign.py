import pandas as pd
import requests
import json
import os

# Constantes
SDW2023_API_URL = 'https://sdw-2023-prd.up.railway.app'

# 1. Extract: Carregar IDs dos usuários
try:
    df = pd.read_csv('SDW2023.csv')
    user_ids = df['UserID'].tolist()
    print(f"User IDs to process: {user_ids}")
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit(1)

# 2. Extract: Buscar dados do usuário (Mocked)
def get_user(id):
    # Dados Mocked para 4 usuários específicos
    users_db = {
        1: {"name": "Maria Silva", "account_number": "01.00001-1", "card_number": "xxxx xxxx xxxx 1111"},
        2: {"name": "João Santos", "account_number": "01.00002-2", "card_number": "xxxx xxxx xxxx 2222"},
        3: {"name": "Ana Costa", "account_number": "01.00003-3", "card_number": "xxxx xxxx xxxx 3333"},
        4: {"name": "Pedro Oliveira", "account_number": "01.00004-4", "card_number": "xxxx xxxx xxxx 4444"}
    }
    
    user_data = users_db.get(id)
    if not user_data:
        # Fallback para outros IDs
        user_data = {"name": f"Devweekerson {id}", "account_number": f"01.0000{id}-{id}", "card_number": f"xxxx xxxx xxxx {id}{id}{id}{id}"}

    mock_user = {
      "id": id,
      "name": user_data["name"],
      "account": {
        "id": id,
        "number": user_data["account_number"],
        "agency": "2030",
        "balance": 624.12 + (id * 100), # Variação no saldo
        "limit": 1000.00
      },
      "card": {
        "id": id,
        "number": user_data["card_number"],
        "limit": 2000.00
      },
      "features": [
        {
          "id": 1,
          "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/pix.svg",
          "description": "PIX"
        },
        {
          "id": 2,
          "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/pay.svg",
          "description": "Pagar"
        },
        {
          "id": 3,
          "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/transfer.svg",
          "description": "Transferir"
        },
        {
          "id": 4,
          "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/account.svg",
          "description": "Conta Corrente"
        },
        {
          "id": 5,
          "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/cards.svg",
          "description": "Cartões"
        }
      ],
      "news": [
        {
          "id": 2,
          "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/insurance.svg",
          "description": "Santander Seguro Casa, seu faz-tudo. Mais de 50 serviços pra você. Confira!"
        },
        {
          "id": 1,
          "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
          "description": "O Santander tem soluções de crédito sob medida pra você. Confira!"
        }
      ]
    }
    return mock_user

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(f"Successfully fetched {len(users)} users.")

# Verificar se existem usuários para processar
if not users:
    print("No users found. Exiting.")
    exit(0)

# 3. Transform: Gerar mensagens de marketing (Mocked)
print("Mocking AI generation to verify logic...")
for user in users:
    news_content = f"Investir é importante, {user['name']}!"
    print(f"Generated news for {user['name']}: {news_content}")
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news_content
    })

# 4. Load: Atualizar notícias do usuário
# Simulação para evitar efeitos colaterais sem confirmação
# for user in users:
#     response = requests.put(f"{SDW2023_API_URL}/users/{user['id']}", json=user)
#     print(f"User {user['name']} updated? {response.status_code == 200}")
