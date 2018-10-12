"""TODO(ycchou): DO NOT SUBMIT without one-line documentation for pr_helper.

TODO(ycchou): DO NOT SUBMIT without a detailed description of pr_helper.
"""

from __future__ import print_function

import argparse
import re
import requests

argp = argparse.ArgumentParser(description='Check whether a gem is included in a version of google_fluentd.')
argp.add_argument(
    '--google_fluentd_version',
    required=True,
    help='the tag of google_fluentd_version.')
argp.add_argument(
    '--gem_name',
    required=True,
    help='the name of the gem.')
argp.add_argument(
    '--gem_repo_pull_number',
    required=True,
    help='the pull request number for the github repo of the gem.')

args = argp.parse_args()

google_fluentd_version = args.google_fluentd_version
gem_name = args.gem_name
gem_repo_pr = args.gem_repo_pull_number

print("google_fluentd_version: {}".format(google_fluentd_version))
print("gem_name: {}".format(gem_name))
print("gem_repo_pr: {}".format(gem_repo_pr))

raw_plugin_gems_url = "https://raw.githubusercontent.com/GoogleCloudPlatform/google-fluentd/{}/plugin_gems.rb"
gem_pr_url = "https://api.github.com/repos/GoogleCloudPlatform/{}/pulls/{}"
gem_compare_url = "https://api.github.com/repos/GoogleCloudPlatform/{}/compare/{}...v{}"
download_regex_pattern = "download \"{}\", \"(.*)\""

plugin_gems_rb = requests.get(raw_plugin_gems_url.format(google_fluentd_version), stream=True)

pattern = re.compile(download_regex_pattern.format(gem_name))

for l in plugin_gems_rb.iter_lines():
  m = pattern.match(l)
  if m:
    gem_version = m.group(1)
    print("gem version for google_fluentd {}: {}".format(google_fluentd_version, gem_version))

commit_sha = requests.get(gem_pr_url.format(gem_name, gem_repo_pr)).json()['merge_commit_sha']
print("commit_sha for repo {} PR#{}: {}".format(gem_name, gem_repo_pr, commit_sha))

compare_status = requests.get(gem_compare_url.format(gem_name, commit_sha, gem_version)).json()['status']

if compare_status == 'identical' or compare_status == 'ahead':
  print("this package includes your PR!")
else:
  print("this package does not have your PR!")
