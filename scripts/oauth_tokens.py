#!/usr/local/bin/python
import requests
import os
import json
import sys


def parse_output(output, user):
    d = output.get('data')
    return [item.get("id") for item in d if item.get("attributes").get("service-provider-user") == user].pop()

def main():
    stdin_json = json.loads(sys.stdin.read())
    username = stdin_json.get('username')
    atlas_token = stdin_json.get('atlas_token')
    tfe_org = stdin_json.get('tfe_org')

    headers = {"Authorization": "Bearer {0}".format(atlas_token)}
    resp = requests.get("https://app.terraform.io/api/v2/organizations/{0}/oauth-tokens".format(tfe_org), 
                    headers=headers)

    oauth_id = parse_output(resp.json(), username)
    if not oauth_id:
        sys.stderr.write("Could not find oauth token. {0}".format(json.dumps(parse_output(resp.json(), username), separators=(',', ':'), indent=4, sort_keys=True)))
        sys.exit(1)


    print json.dumps(dict(oauth_id=oauth_id), 
                        separators=(',', ':'), 
                        indent=4, 
                        sort_keys=True)

if __name__ == '__main__':
    main()
