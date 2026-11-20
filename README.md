# GLPI Ticket Generator

Asynchronous Python script that generates large volumes of realistic tickets in [GLPI](https://glpi-project.org/) through its REST API. Built for load testing, populating test environments and feeding analytics dashboards (Power BI).

## Features

- Random incidents and service requests, assigned to predefined users
- Random entities and ITIL categories
- Realistic lifecycle: *New* and *Closed* statuses with computed dates
- Full GLPI REST authentication flow (App-Token, User-Token, Session-Token)
- High throughput with `asyncio` + `aiohttp`, bounded concurrency and a `tqdm` progress bar

## Requirements

- Python 3.8+
- A GLPI instance with the REST API enabled
- A valid App token and User token

```bash
pip install aiohttp tqdm
```

## Configuration

Settings live at the top of `script.py`:

```python
glpi_url = "http://127.0.0.1/glpi/apirest.php"
app_token = "VOTRE_APP_TOKEN"
user_token = "VOTRE_USER_TOKEN"
total_tickets = 100000
concurrent_requests = 100
```

Users, entities and categories are defined in `users_ids`, `entity_ids`, `categories_demande` and `categories_incident`.

## Usage

```bash
python3 script.py
```

## Example generated ticket

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

## Use cases

- Load testing a GLPI instance
- Seeding test and demo environments
- Producing realistic data for ITSM dashboards (resolution time, categories, volumes)

## License

MIT
