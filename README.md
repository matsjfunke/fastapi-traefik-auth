# fastapi-login-traefik
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

is a simple example / template for authentication (login)   

## Technology Stack and Features
- ⚡ [FastAPI](https://fastapi.tiangolo.com) a high-performance, web framework for building APIs with Python 3.7+.
- 📞 [Traefik](https://traefik.io) a modern reverse proxy and load balancer, providing automatic HTTPS encryption and certificate management.
- 🥷 [Jinja2Templates](https://fastapi.tiangolo.com/advanced/templates/) for rendering dynamic HTML content, making it easy to create user interfaces.
- 🍪 [python-jose](https://python-jose.readthedocs.io/en/latest/) for secure user authentication using JSON Web Tokens (JWT), ensuring that only authenticated users can access protected routes.
- 🔒 [passlib](https://pypi.org/project/passlib/) for secure password hashing and verification.
- 🐋 [Docker Compose](https://www.docker.com) deploy and manage your application using Docker-compose, allowing for seamless containerization and orchestration of your services.

## Quick start / Usage

### direct on server
- clone repo
- change line 34 of docker.compose.staging.yml
    - "traefik.http.routers.db-access.rule=Host(`your-domain.com`)" # change `your-domain.com` to your domain
- start docker 
```bash
git clone https://github.com/matsjfunke/fastapi-login-traefik.git
docker-compose -f docker-compose.staging.yml up
```
than access the page https:/your-domain.com and enter the credentails "user1" and "foo" from the [json-db](https://github.com/matsjfunke/fastapi-login-traefik/blob/main/app/user_db.json)

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

## TODOS
- get local test to work & replace ngnix-proxy with [traefik](https://doc.traefik.io/traefik/getting-started/quick-start/) in docker-compose.yml
- add a [PostgreSQL](https://www.postgresql.org) database with [Pydantic](https://docs.pydantic.dev) for data validation, instead of json as "database"
- add working tests and document usage in README
