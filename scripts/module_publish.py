#!/usr/local/bin/python
import requests
import os
import json
import sys
import hcl

def sanitize_path(config):
    path = os.path.expanduser(config)
    path = os.path.expandvars(path)
    path = os.path.abspath(path)
    return path

def tfe_token(tfe_api, config):
    with open(sanitize_path(config), 'r') as fp:
        obj = hcl.load(fp)
    return obj.get('credentials').get(tfe_api).get('token')

class GOTOException(Exception): pass

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
               "Content-Type": "application/vnd.api+json"}

    with open("/tmp/module_publish.log", "a") as log:
        log.write(json.dumps(data, separators=(',', ':'), indent=4, sort_keys=True))

    resp = requests.post("https://{0}/api/v2/registry-modules".format(tfe_api), 
                    headers=headers,
                    data=json.dumps(data))


    data = json.dumps(resp.json(), separators=(',', ':'), indent=4, sort_keys=True)
    with open("/tmp/module_publish.log", "a") as log:
        log.write(data)

    status_code = resp.status_code
    try:
        if status_code not in [200, 201]:
            for _error in data.get("errors"):
                if _error.get("meta").get("duplicate_module"):
                    raise GOTOException("Module Exists!")
            sys.stderr.write(str(resp.status_code))
            sys.stderr.write(resp.text)
            sys.exit(1)
    except GOTOException, e:
        status_code = 204
    

    print json.dumps(dict(status=str(resp.status_code)), 
                        separators=(',', ':'), 
                        indent=4, 
                        sort_keys=True)

if __name__ == '__main__':
    main()
