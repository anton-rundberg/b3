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

## Testing

1. Make sure the project is running locally
2. `make test`

See the makefile for additional arguments and shortcuts.

## Deploying

### Getting started deploying with the b3

1. Set host file vars

Replace `...` with ip of host

Set distribution of server and the ssh user per host
```
ansible_user=ubuntu
ansible_distribution=ubuntu
```

2. Set inventories vars

Set
```
REGISTRY_URL=
```
in
deploy/inventories/group_vars/all/vars.yml

Set
```
DOCKER_ID=
DOCKER_EMAIL=
DOCKER_PASSWORD=
```
in
deploy/inventories/group_vars/all/vault.yml

Set
```
DOMAIN_NAME=

django_env: 
  DB_USER=
  DB_HOST=
  DB_NAME=
```
in
deploy/inventories/group_vars/dev/vars.yml
deploy/inventories/group_vars/prod/vars.yml

Set
```
vault_RABBITMQ_USER: 
vault_RABBITMQ_PASSWORD: 
vault_SECRET_KEY: 
vault_DB_PASSWORD: 
```
in
deploy/inventories/group_vars/dev/vault.yml
deploy/inventories/group_vars/prod/vault.yml

3. Create .vault_pass file in /deploy/ and add it to 1password
4. `ansible-vault encrypt inventories/group_vars/all/vault.yml`
5. `ansible-vault encrypt inventories/group_vars/dev/vault.yml`
6. `ansible-vault encrypt inventories/group_vars/prod/vault.yml`
7. Remove this section from the README
8. Deploy!

### Building image manually

Note: Building locally on Apple Silicon will conflict with AMD64 EC2 instances

1. `git checkout main`
2. `git pull`
3. `docker-compose build`
4. `docker tag django-b3:latest DOCKER_REPO_URL:TAG`
5. `docker push DOCKER_REPO_URL:TAG`
6. `cd deploy`
7. `make run limit=dev`

For releases, push a new docker tag by creating and pushing a git tag prefixed with `release-`.

### Deploy

Deploys and provisioning is done using Ansible. In order to deploy you need to have Ansible installed on your machine. For macOS do `brew install ansible`. Please don't hesitate to ask or read the Ansible playbooks and documentation to understand what is done on each deploy.

Deploying to dev:

1. Wait for CI to build the latest docker image / build docker image and push it to repository
2. cd deploy
3. Create file `.vault_pass` containing the password found in 1password
4. `make run limit=dev`

Deploying to prod:

1. `git tag release-<todays date>-<two digit build number> && git push origin release-<todays date>-<two digit build number>`
2. Wait for CI to build the tagged docker image
3. cd deploy
4. Create file `.vault_pass` containing the password found in 1password
5. `make run limit=prod app-version=release-<todays date>-<two digit build number>`


## Infrastructure

See [infrastructure/README.md](infrastructure/README.md)


## How-to dump from dev

1. SSH to dev server
2. `docker run -it --rm --name pg-dump postgres:14 bash`
3. `pg_dump -h POSTGRES_HOSTNAME -U b3 b3 > dev_DATE.sql`
4. SSH to dev server in another window
5. `docker cp pg-dump:/dev_DATE.sql .`
6. Disconnect from server
7. scp `SERVER_IP:~/dev_DATE.sql .`
8. `docker cp dev_DATE.sql postgres-b3:/tmp/`
9. `docker exec -it postgres-b3 bash`
10. `psql -U postgres`
11. `drop database b3;`
12. `create database b3;`
13. `exit;`
14. `psql -U postgres -d b3 < /tmp/dev_DATE.sql`
