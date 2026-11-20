import asyncio
import aiohttp
import random
from datetime import datetime, timedelta
from tqdm.asyncio import tqdm

# === CONFIGURATION ===
glpi_url = "http://127.0.0.1/glpi/apirest.php"
app_token = "VOTRE_APP_TOKEN"
user_token = "VOTRE_USER_TOKEN"
total_tickets = 100000
concurrent_requests = 100

# === DONNÉES
users_ids = {
    "readonly": 42, "testappadmin": 22, "testapptech": 24, "testappuser": 23,
    "testgmaoadmin": 25, "testgmaotech": 27, "testgmaouser": 26, "testhisadmin": 28,
    "testhistech": 29, "testhisuser": 30, "testit": 41, "testlisadmin": 31,
    "testlistech": 33, "testlisuser": 32, "testnabadyadmin": 34, "testnabadytech": 36,
    "testnabadyuser": 35, "testrisadmin": 38, "testristech": 39, "testrisuser": 37,
    "testsuperadmin": 40
}

categories_demande = {
    "Demande - Acces": 1, "Demande - Autre": 5, "Demande - information": 4,
    "Demande - logiciel": 3, "Demande - Nouveau materiel": 2
}

categories_incident = {
    "Incident - autre": 10, "Incident - logiciel": 8, "Incident - materiel": 7,
    "Incident - Reseau": 6, "Incident - securite": 9
}

entity_ids = [1, 2, 3]

# === INIT SESSION ===
async def init_session(session):
    async with session.get(f"{glpi_url}/initSession", headers={
        'App-Token': app_token,
        'Authorization': f'user_token {user_token}'
    }) as resp:
        data = await resp.json()
        return data['session_token']

# === CRÉATION DE TICKET ===
async def create_ticket(i, session, session_token):
    headers = {
        'App-Token': app_token,
        'Authorization': f'user_token {user_token}',
        'Session-Token': session_token
    }

    user = random.choice(list(users_ids.keys()))
    user_id = users_ids[user]
    type_ticket = random.choice([1, 2])
    status = random.choice([1, 6])
    entity_id = random.choice(entity_ids)

    type_name = "Incident" if type_ticket == 1 else "Demande"
    title = f"[{type_name}] Ticket #{i} de {user}"
    category_name, category_id = (
        random.choice(list(categories_demande.items()))
        if type_ticket == 2 else
        random.choice(list(categories_incident.items()))
    )

    now = datetime.now()

    if status == 6:
        # Fermé : choisir une date de création aléatoire entre 3 et 7 jours avant
        closed_delta = timedelta(days=random.uniform(1, 3))
        closed_at = now
        created_at = now - closed_delta
    else:
        created_at = now
        closed_at = None

    payload = {
        "input": {
            "name": title,
            "content": f"{type_name} généré automatiquement.\nCatégorie: {category_name}\nEntité: Clinique {chr(64 + entity_id)}",
            "status": status,
            "users_id_recipient": user_id,
            "type": type_ticket,
            "itilcategories_id": category_id,
            "entities_id": entity_id,
            "users": [{"type": 1, "users_id": user_id}],
            "date": created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    }

    if closed_at:
        payload["input"]["closedate"] = closed_at.strftime('%Y-%m-%d %H:%M:%S')

    try:
        async with session.post(f"{glpi_url}/Ticket", headers=headers, json=payload) as resp:
            if resp.status != 201:
                print(f"❌ [{i}] erreur {resp.status}")
    except Exception as e:
        print(f"❌ [{i}] exception : {e}")

# === MAIN ===
async def main():
    conn = aiohttp.TCPConnector(limit=concurrent_requests)
    async with aiohttp.ClientSession(connector=conn) as session:
        session_token = await init_session(session)

        sem = asyncio.Semaphore(concurrent_requests)

        async def sem_task(i):
            async with sem:
                await create_ticket(i, session, session_token)

        await tqdm.gather(*(sem_task(i) for i in range(1, total_tickets + 1)))

        await session.get(f"{glpi_url}/killSession", headers={
            'App-Token': app_token,
            'Authorization': f'user_token {user_token}',
            'Session-Token': session_token
        })

    print(f"\n✅ {total_tickets:,} tickets créés avec succès dans GLPI.")

# === LANCEMENT ===
if __name__ == "__main__":
    asyncio.run(main())
