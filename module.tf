data "external" "oauth_token" {
  program = ["python", "${path.module}/scripts/oauth_tokens.py"]

  query = {
    # arbitrary map from strings to strings, passed
    # to the external program as the data query.
    username = "${var.repo_user}"

    tfe_org     = "${var.tfe_org}"
    atlas_token = "${var.atlas_token}"
  }
}

data "template_file" "module" {
  template = "${file("${path.module}/module.json.tpl")}"

  vars {
    repo_org       = "${var.github_organization}"
    repo_name      = "${var.repo}"
    oauth_token_id = "${data.external.oauth_token.result.oauth_id}"
  }
}

data "external" "module_publish" {
  program = ["python", "${path.module}/scripts/module_publish.py"]

  query = {
    module_config = "${data.template_file.module.rendered}"
    tfe_org       = "${var.tfe_org}"
    atlas_token   = "${var.atlas_token}"
  }
}
