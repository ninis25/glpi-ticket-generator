# GLPI Ticket Generator – Async Python Script

Ce projet est un script Python asynchrone permettant de générer automatiquement un grand volume de tickets dans GLPI via son API REST. Il a été conçu pour des **tests de charge**, des **scénarios de simulation réaliste**, ou pour **alimenter des dashboards analytiques** (ex. : Power BI).

## Fonctionnalités

- Création de tickets incidents ou demandes aléatoires.
- Attribution automatique à des utilisateurs prédéfinis.
- Choix aléatoire des entités et des catégories.
- Gestion des statuts (Nouveau, Clos) avec calcul dynamique des dates.
- Support de l’API REST de GLPI avec App-Token, User-Token, et Session-Token.
- Fonctionnement asynchrone et optimisé avec `aiohttp`, `asyncio` et `tqdm`.

## Prérequis

- Python 3.8+
- Une instance GLPI accessible via HTTP/HTTPS
- API REST activée et configurée sur GLPI
- Un App Token et un User Token valides

### Dépendances Python

```bash
pip install aiohttp tqdm
```

## Utilisation

```bash
python3 script.py
```

> Le script génère par défaut 100 000 tickets en parallèle (modifiable via `total_tickets`).

## Configuration

Les paramètres sont définis en haut du fichier `script.py` :

```python
glpi_url = "http://127.0.0.1/glpi/apirest.php"
app_token = "VOTRE_APP_TOKEN"
user_token = "VOTRE_USER_TOKEN"
total_tickets = 100000
concurrent_requests = 100
```

Les utilisateurs, entités, et catégories peuvent être personnalisés dans les dictionnaires suivants :

- `users_ids`
- `categories_demande`
- `categories_incident`
- `entity_ids`

## Exemple de ticket généré

```json
{
  "name": "[Demande] Ticket #5421 de testlisuser",
  "content": "Demande générée automatiquement.\nCatégorie: Demande - Acces\nEntité: Clinique B",
  "status": 1,
  "type": 2,
  "users_id_recipient": 32,
  "itilcategories_id": 1,
  "entities_id": 2,
  "date": "2025-05-26 14:22:31"
}
```

## Résultats attendus

- Génération rapide de plusieurs milliers de tickets.
- Aucune surcharge du serveur grâce à la gestion des connexions concurrentes.
- Données réalistes exploitables dans Power BI ou autres outils d’analyse.

## Cas d’usage

- Tests de charge sur GLPI
- Simulations de tickets pour environnement de test
- Alimentation de dashboards statistiques (temps de traitement, catégories, etc.)

## Licence

Ce projet est distribué sous licence MIT. Utilisation libre à des fins de test ou développement.

---

Développé dans un cadre de projet ITSM autour de GLPI.
