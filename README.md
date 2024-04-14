# fastapi-login-traefik
is a simple example / template for authentication (login)   

## Technology Stack and Features
- ⚡ [FastAPI](https://fastapi.tiangolo.com) for the Python API.
- 📞 [Traefik](https://traefik.io) as a reverse proxy for SSL termination.
- 🥷 [Jinja2Templates](https://fastapi.tiangolo.com/advanced/templates/) for html frontend.
- 🐋 [Docker Compose](https://www.docker.com)
- 🔒 [passlib](https://pypi.org/project/passlib/) for Secure password hashing.
- 🍪 [python-jose](https://python-jose.readthedocs.io/en/latest/) for JWT token authentication.

## Quick start
### local:
- clone repo
- change line 34 of docker.compose.staging.yml
    - "traefik.http.routers.db-access.rule=Host(`your-domain.com`)" # change `your-domain.com` to your domain
- rsync to server
- start docker 
```bash
git clone https://github.com/matsjfunke/fastapi-login-traefik.git
rsync -av -e "ssh -i ~/.ssh/your-key.pem"  --exclude=__pycache__ --exclude=env  fastapi-login-traefik your-usr@your-server.com:dir
docker-compose -f docker-compose.staging.yml up
```
than access the page https:/your-domain.com and enter the credentails "user1" and "foo" from the [json-db](https://github.com/matsjfunke/fastapi-login-traefik/blob/main/app/user_db.json)

### direct on server
- clone repo
- change line 34 of docker.compose.staging.yml
    - "traefik.http.routers.db-access.rule=Host(`your-domain.com`)" # change `your-domain.com` to your domain
- start docker 
```bash
git clone https://github.com/matsjfunke/fastapi-login-traefik.git
docker-compose -f docker-compose.staging.yml up
```

## TODOS
- add local [traefik](https://doc.traefik.io/traefik/getting-started/quick-start/)
- add a [PostgreSQL](https://www.postgresql.org) database with [Pydantic](https://docs.pydantic.dev) for data validation, instead of json as "database"
- add better tests
