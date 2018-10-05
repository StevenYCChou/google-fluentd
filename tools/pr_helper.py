"""TODO(ycchou): DO NOT SUBMIT without one-line documentation for pr_helper.

TODO(ycchou): DO NOT SUBMIT without a detailed description of pr_helper.
"""

import re
import requests

google_fluentd_version = "v1.5.35"
gem_repo_name = "fluent-plugin-google-cloud"
gem_repo_pr = "232"

print("google_fluentd_version: {}".format(google_fluentd_version))
print("gem_repo_name: {}".format(gem_repo_name))
print("gem_repo_pr: {}".format(gem_repo_pr))

raw_plugin_gems_url = "https://raw.githubusercontent.com/GoogleCloudPlatform/google-fluentd/{}/plugin_gems.rb"
gem_pr_url = "https://api.github.com/repos/GoogleCloudPlatform/{}/pulls/{}"
gem_compare_url = "https://api.github.com/repos/GoogleCloudPlatform/{}/compare/{}...v{}"
download_regex_pattern = "download \"{}\", \"(.*)\""

pattern = re.compile(download_regex_pattern.format(gem_repo_name))
gems = requests.get(raw_plugin_gems_url.format(google_fluentd_version), stream=True)
for l in gems.iter_lines():
  m = pattern.match(l)
  if m:
    gem_version = m.group(1)
    print("gem version for google_fluentd {}: {}".format(google_fluentd_version, gem_version))

commit_sha = requests.get(gem_pr_url.format(gem_repo_name, gem_repo_pr)).json()['merge_commit_sha']
print("commit_sha for repo {} PR#{}: {}".format(gem_repo_name, gem_repo_pr, commit_sha))

compare_status = requests.get(gem_compare_url.format(gem_repo_name, commit_sha, gem_version)).json()['status']

if compare_status == 'identical' or compare_status == 'ahead':
  print("this package includes your PR!")
else:
  print("this package does not have your PR!")
