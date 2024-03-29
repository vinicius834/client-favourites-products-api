# Client Favourites Products API

## Build

```bash
docker-compose build --no-cache
```

## Run

```bash
docker-compose up --force-recreate
```
## Create Authentication Token

```bash
docker exec -it client-favourites-products-api sh -c 'python manage.py createsuperuser --username test --email test@example.com --no-input && python manage.py drf_create_token test'
```

## Usage

```bash
POST localhost:8000/client/
{
    "name": "test",
    "email": "test@test.com"
}

PUT localhost:8000/client/<id>
{
    "name": "test",
    "email": "test@test.com"
}

GET localhost:8000/client/ # get the client list
GET localhost:8000/client/<id> # return a client
DELETE localhost:8000/client/<id> # delete a client

GET localhost:8000/product/<id> # return a product
GET localhost:8000/product/<page_number> # return a list of products


PATCH localhost:8000/client/<client_id>/favourite_product/ # add favourite product to client favourite list
{
    "product_id": "1bf0f365-fbdd-4e21-9786-da459d78dd1f"
}

DELETE localhost:8000/client/<client_id>/favourite_product/<product_id> # remove product from client favourite list

```

## Run tests

```bash
docker exec -it client-favourites-products-api sh -c 'python manage.py test --noinput --settings=api.test_settings'
```

