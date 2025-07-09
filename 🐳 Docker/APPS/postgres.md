```yaml
services:
  postgres:
    image: postgres
    restart: always
    volumes:
    - ./db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: postgres
    ports:
    - "5432:5432"
```