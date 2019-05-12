#!/usr/bin/expect -f

# . ./openrc.sh; ansible-playbook --ask-become-pass webServer.yaml
#. ./openrc.sh; ansible-playbook --ask-become-pass appServer.yaml
# . ./openrc.sh; ansible-playbook --ask-become-pass melb_dbServer.yaml
. ./openrc.sh;ansible-playbook --ask-become-pass syd_dbServer.yaml
#Pass: ZjdkNDcxNDE4ODEzM2Ji
