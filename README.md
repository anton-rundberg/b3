# README

## Getting started with the b3

4. If using AWS set find replace `{{AWS_ACCOUNT_ID}}` for CircleCI
5. Enable docker builds in CI on main by uncommenting `publish_latest_image` in `.circleci/config.yml`
6. Remove this section from the README
7. Start coding!

## Starting the project locally

1. Enable pre-commit `pre-commit install`
2. Set up local `.env` file containing at least the env vars seen in sample file below.
3. `make`
4. Run db migrations `make migrate`

Example `.env` working with the current local docker-compose setup:

```
ENV=LOCAL
DEBUG=True

DB_PASSWORD=supersecret
SECRET_KEY=loremipsumdolorsitamet
```

## Setting up the first admin user

1. `make createsuperuser email=my-email@example.com`

If you're deploying to a non-local environment you can set up a one-time-user 2FA token using `make addstatictoken email=my-email@example.com` and afterwards create your TOTP device in the admin panel.

## Doing local API testing with an external client like Postman

1. Using the credentials for the previously setup admin user
2. Login to the Django admin portal at localhost:8000/admin
3. Navigate to the interactive Swagger documentation at localhost:8000/docs
4. Use any endpoint that you'd like :)

## Testing

1. Make sure the project is running locally
2. `make test`

See the makefile for additional arguments and shortcuts.

