# devicemanagement

This project demonstrates configuration management with AAP

Playbooks
- config-retrieval
  - extracts configuration via netconf
  - checks changes against a baseline branch
  - Alerts EDA via a kafka channel (see rulebooks eda-config-alert.yml)
  - Runs compliance rules against config values (see https://github.com/bfarr-rh/device_compliance/blob/master/golden_config/groups/srlinux/auth.json)
- config-doc
  - creates a table of contents against all config and runs as a second playbook as part of the workflow https://github.com/bfarr-rh/devicedata
