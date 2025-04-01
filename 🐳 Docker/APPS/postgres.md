```yaml
version: '3.6'
services:
  postgres:
    image: postgres
    restart: always
    volumes:
    - ./db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: qW113113e.
    ports:
    - "5432:5432"
```