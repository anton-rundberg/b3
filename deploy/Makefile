# Structure inspired from following file:
# https://github.com/paulRbr/ansible-makefile/blob/master/Makefile

playbook	?= deploy
env			?= inventories/hosts
pass-file	?= .vault_pass
limit		?= dev
app-version ?= latest

ifeq ("$(pass-file)", "")
	opts	?= $(args)
else
	opts	?= $(args) --vault-password-file=$(pass-file)
endif
ifneq ("$(app-version)", "")
	opts	:= $(opts) --extra-vars="DOCKER_IMAGE_TAG=$(app-version)"
endif
ifneq ("$(extra-vars)", "")
	opts	:= $(opts) --extra-vars="$(extra-vars)"
endif
ifneq ("$(limit)", "")
	opts	:= $(opts) --limit="$(limit)"
endif
ifneq ("$(tags)", "")
	opts	:= $(opts) --tags="$(tags)"
endif
ifneq ("$(verbosity)", "")
	opts	:= $(opts) -$(verbosity)
endif

.PHONY: dry-run
dry-run: ## make dry-run [playbook=deploy] [env=inventories/hosts] [tag=<ansible tag>] [limit=<ansible host limit>] [args=<ansible-playbook arguments>] [verbosity=v] # Run a playbook in dry run mode
	@env=$(env) ansible-playbook --inventory-file="$(env)" --diff --check $(opts) "./playbooks/$(playbook).yml"

.PHONY: run
run: mandatory-vault-pass ## make run [playbook=deploy] [env=inventories/hosts] [tags=<ansible tags>] [limit=<ansible host limit>] [args=<ansible-playbook arguments>] [extra-vars="var1=a var2=b"] [verbosity=v] # Run a playbook
	@env=$(env) ansible-playbook --inventory-file="$(env)" --diff $(opts) "./playbooks/$(playbook).yml"

.PHONY: list
list: ## make list [env=inventories/hosts] # List hosts inventory
	@[ -f "$(env)" ] && cat "$(env)" || \
	([ -f "$(env)/hosts" ] && cat "$(env)/hosts")

.PHONY: list-tags
list-tags: ## make list-tags # List all available tags
	@ansible-playbook --list-tags "./playbooks/$(playbook).yml"

group ?=all
.PHONY: facts
facts: ## make facts group=all [env=inventories/hosts] [args=<ansible arguments>] # Gather facts from your hosts
	@env=$(env) ansible --module-name="setup" --inventory-file="$(env)" $(opts) --tree="out/" $(group)

.PHONY: cmdb
cmdb: ## make cmdb # Create HTML inventory report
	@ansible-cmdb "out/" > list-servers.html

.PHONY: mandatory-vault-pass
mandatory-vault-pass:
	@([ ! -z $(pass-file) ] && [ -f "$(pass-file)" ]) || \
	(echo "Mandatory vault password file missing (default is looking for: '.vault_pass')" && \
	exit 1)

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
