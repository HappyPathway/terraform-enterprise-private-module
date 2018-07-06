#!/usr/local/bin/python
import requests
import os
import json
import sys

def main():
    stdin_json = json.loads(sys.stdin.read())
    atlas_token = stdin_json.get('atlas_token')
    tfe_org = stdin_json.get('tfe_org')
    module_config = stdin_json.get("module_config")
    data = json.loads(module_config)
    #with open("/tmp/module_config.json", "w") as config_output:
    #    config_output.write(json.dumps(data))

    headers = {"Authorization": "Bearer {0}".format(atlas_token),
               "Content-Type": "application/vnd.api+json    "}
    resp = requests.post("https://app.terraform.io/api/v2/registry-modules", 
                    headers=headers,
                    data=json.dumps(data))


    data = json.dumps(resp.json(), separators=(',', ':'), indent=4, sort_keys=True)
    with open("/tmp/module_publish.log", "a") as log:
        log.write(data)

    if resp.status_code not in [200, 201]:
        sys.stderr.write(str(resp.status_code))
        sys.stderr.write(resp.text)
        sys.exit(1)

    print json.dumps(dict(status=str(resp.status_code)), 
                        separators=(',', ':'), 
                        indent=4, 
                        sort_keys=True)

if __name__ == '__main__':
    main()
