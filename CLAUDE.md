# Go High Level — parte técnica de GHL

Repo de la agencia de Joan Kaizen (Kaizen Space LLC). Todo lo técnico de GoHighLevel: conexión a la API,
subcuentas de clientes y emails del Programa OASIS. Ver README.md para el uso del cliente `scripts/ghl.py`.

## Cómo trabajar con Joan
- Directo y orientado a resultados. Respuestas cortas.
- Instrucciones exactas, clic a clic, no teoría.
- Si algo falla: primero la causa y el efecto en lenguaje llano, luego la solución.
- Nada de soluciones complejas. Si hay una opción simple, esa.
- Copy de emails: conversacional e imperfecto, "como escribiendo desde el sofá". Nada que suene a IA.

## Qué hay aquí
- `scripts/ghl.py`: cliente de la API v2 (Private Integration Token).
- `emails-oasis/`: secuencia semanal de OASIS (ver `CALENDARIO.md`).
- `data/` y `backups/` son locales y NO están en el repo (pueden tener datos de clientes).

## Claves
- Van en variables de entorno (ver `.env.example`): token de agencia y uno por subcuenta de cliente.
- En local, en `.env`. En la nube, en las variables del entorno. Nunca dentro de un archivo del repo.
- La nube necesita acceso de red a services.leadconnectorhq.com.

## Antes de escribir en GHL
Antes de modificar algo de una subcuenta de cliente, guarda una copia de cómo estaba y confirma con Joan.

## Regla de estado (obligatoria, sin que Joan lo pida)
Cada vez que termines algo con resultado (un cambio hecho, una decisión, un bloqueo nuevo), actualiza ESTADO.md:
- Edita la línea del cliente afectado. El archivo refleja cómo están las cosas AHORA, no es un diario.
- Mueve lo terminado a "Hecho recientemente" con la fecha. Borra lo de hace más de un mes.
- Después haz commit y push. La Madre profesional (repo kaizen-hub) lee este archivo.
