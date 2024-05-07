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
- 🗃️ [SQLite Database](https://www.sqlite.org/) for storing usernames and hashed passwords.
- 🛠️ [SQLAlchemy](https://www.sqlalchemy.org/) as an ORM for working with the database.
- 🛡️ [Pydantic](https://docs.pydantic.dev) for data validation.
- 🐋 [Docker Compose](https://www.docker.com) deploy and manage your application using Docker-compose, allowing for seamless containerization and orchestration of your services.

## Quick start / Usage

#### 1. run local without reverse-proxy
- cloe repo
```bash
git clone https://github.com/matsjfunke/fastapi-login-traefik.git
```
- start container
```bash
docker-compose -f docker-compose.yml up --build
```
- than access the localhost:8000 and submit username and password, then enter your credentials at localhost:8000/login 
- now with the cookies you obtained through logging in you can access the /hello and /users endpoints
 

#### 2. run on server
- clone repo
- change line 34 of docker.compose.staging.yml
    - "traefik.http.routers.db-access.rule=Host(`your-domain.com`)" # change `your-domain.com` to your domain
- start docker 
```bash
git clone https://github.com/matsjfunke/fastapi-login-traefik.git
docker-compose -f docker-compose.staging.yml up
```
- than access the localhost:8000 and submit username and password, then enter your credentials at localhost:8000/login 
- now with the cookies you obtained through logging in you can access the /hello and /users endpoints

  
## Test
use the test script to check if the login works
```bash
pip install selenium
python tests/loging-test.py
```

## TODOS
- add a [PostgreSQL](https://www.postgresql.org) database example
