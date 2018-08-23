data "template_file" "module" {
  template = "${file("${path.module}/module.json.tpl")}"

  vars {
    repo_org       = "${var.github_organization}"
    repo_name      = "${var.repo}"
    oauth_token_id = "${var.oauth_token}"
  }
}

data "external" "module_publish" {
  program = ["python", "${path.module}/scripts/module_publish.py"]

  query = {
    module_config = "${data.template_file.module.rendered}"
    tfe_org       = "${var.tfe_org}"
    tfe_api = "${var.tfe_api}"
    config = "${var.config}"
    repo_name      = "${var.repo}"
  }
}
