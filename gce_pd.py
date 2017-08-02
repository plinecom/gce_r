#!/usr/bin/env python
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

module = AnsibleModule(
    argument_spec=dict(
        name=dict(required=True),
        service_account_email=dict(),
        credentials_file=dict(),
        project_id=dict(),
        delete_on_termination=dict(required=False, choices=[True, False], default=False),
        detach_only=dict(required=False, choices=[True, False], default=False),
        disk_type=dict(required=False, choices=['pd-standard', 'pd-ssd'], default='pd-standard'),
        image=dict(default=None),
        instance_name=dict(default=None),
        mode=dict(required=False, choices=['READ_ONLY', 'READ_WRITE'], default='READ_ONLY'),
        size_gb=dict(default=10),
        snapshot=dict(default=None),
        state=dict(choices=['active', 'present', 'absent', 'deleted'], default='present'),
        zone=dict(default='us-central1-b')
    )
)


ComputeEngine = get_driver(Provider.GCE)
# Note that the 'PEM file' argument can either be the JSON format or
# the P12 format.
driver = ComputeEngine(module.params['service_account_email'],
                       module.params['credentials_file'],
                        datacenter=module.params['zone'],
                        project=module.params['project_id'])
volume = driver.create_volume(size=module.params['size_gb'],
                     name=module.params['name'],
                     location=module.params['zone'],
                     snapshot=module.params['snapshot'],
                     ex_disk_type=module.params['disk_type'],
                     ex_image_family=module.params['image'])

if module.params['instance_name'] is not None:

    attach_node = driver.ex_get_node(name=module.params['instance_name'], zone=module.params['zone'])

    driver.attach_volume(node=attach_node, volume=volume, ex_mode=module.params['mode'])



open_url('https://www.google.com', method="GET")


module.exit_json(changed=True)
