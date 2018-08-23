#!/usr/local/bin/python
import requests
import os
import json
import sys
import hcl

def tfe_token(tfe_api, config):
    with open(os.path.abspath(config), 'r') as fp:
        obj = hcl.load(fp)
    return obj.get('credentials').get(tfe_api).get('token')


def main():
    stdin_json = json.loads(sys.stdin.read())
    
    tfe_org = stdin_json.get('tfe_org')
    tfe_api = stdin_json.get('tfe_api')
    config = stdin_json.get('config')
    atlas_token = tfe_token(tfe_api, config)
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
