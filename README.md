# GoHighLevel — Kaizen Space LLC

Conexión a la API v2 de GoHighLevel (LeadConnector) mediante Private Integration Token.

## Configuración

Credenciales en `.env` (permisos 600, ignorado por git):

| Variable | Descripción |
|---|---|
| `GHL_PIT` | Private Integration Token de la agencia |
| `GHL_API_BASE` | `https://services.leadconnectorhq.com` |
| `GHL_API_VERSION` | `2021-07-28` |

## Cuenta

- **Agencia:** Kaizen Space LLC — `IIWwKODSGg4qRPU6WUcb`
- **Nº de relación:** 0-779-899
- **Subcuentas:** 9 (ver `data/locations.json`)

## Uso

```bash
python3 scripts/ghl.py GET /locations/search limit=100
python3 scripts/ghl.py GET /companies/IIWwKODSGg4qRPU6WUcb
python3 scripts/ghl.py POST /contacts/ --json '{"locationId":"...","email":"a@b.com"}'
```

Desde Python:

```python
import sys; sys.path.insert(0, "scripts")
from ghl import request, paginate
locs = paginate("/locations/search", {"companyId": "IIWwKODSGg4qRPU6WUcb"}, key="locations")
```

Nota: la API está tras Cloudflare y bloquea el User-Agent por defecto de Python;
el cliente envía uno propio (`kaizen-ghl-client/1.0`).

## Scopes activos del token

Habilitados: `locations.readonly`, `companies.readonly`, `snapshots.readonly`.

El resto (contactos, oportunidades, calendarios, conversaciones, workflows,
formularios, productos, facturas, social planner, medios…) devuelven
`401 – The token is not authorized for this scope`. Para activarlos:
**Settings → Private Integrations → editar la integración → marcar scopes**.
