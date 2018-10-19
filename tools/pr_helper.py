"""TODO(ycchou): DO NOT SUBMIT without one-line documentation for pr_helper.

TODO(ycchou): DO NOT SUBMIT without a detailed description of pr_helper.
"""

from __future__ import print_function

import argparse
import re
import requests

argp = argparse.ArgumentParser(description='Check whether a version of code includes a PR.')
argp.add_argument(
    '--org',
    required=False,
    default='GoogleCloudPlatform',
    help='The org of the repositories. Default is GoogleCloudPlatform.')
argp.add_argument(
    '--release_repo',
    required=True,
    help='The repo name includes your main code.')
argp.add_argument(
    '--release_version',
    required=True,
    help='A git tag version for the repo you want to examine.')
argp.add_argument(
    '--pr_repo',
    required=False,
    help='The repo name of the PR. Default value is the same as release_repo.')
argp.add_argument(
    '--pr_number',
    required=True,
    help='The number of the Github pull request.')

args = argp.parse_args()

org = args.org
release_repo = args.release_repo
release_version = args.release_version

pr_repo = release_repo
if args.pr_repo is not None:
  pr_repo = args.pr_repo

pr_number = args.pr_number

print("Input:")
print("  release:")
print("    org: {}, repo: {}, version: {}".format(org, release_repo, release_version))
print("  PR:")
print("    repo: {}".format(pr_repo))
print("    #: {}".format(pr_number))

raw_plugin_gems_url = "https://raw.githubusercontent.com/" + org + "/{}/{}/plugin_gems.rb"
pr_url = "https://api.github.com/repos/" + org + "/{}/pulls/{}"
compare_url = "https://api.github.com/repos/" + org + "/{}/compare/{}...{}"
download_regex_pattern = "download \"{}\", \"(.*)\""

if release_repo == pr_repo:
  commit_sha = requests.get(pr_url.format(pr_repo, pr_number)).json()['merge_commit_sha']
  print("commit_sha for repo {} PR#{}: {}".format(pr_repo, pr_number, commit_sha))
  compare_status = requests.get(compare_url.format(pr_repo, commit_sha, release_version)).json()['status']

  if compare_status == 'identical' or compare_status == 'ahead':
    print("this package includes your PR!")
  else:
    print("this package does not have your PR!")
  exit(0)

plugin_gems_rb = requests.get(raw_plugin_gems_url.format(release_repo, release_version), stream=True)

pattern = re.compile(download_regex_pattern.format(pr_repo))

for l in plugin_gems_rb.iter_lines():
  m = pattern.match(l)
  if m:
    gem_version = m.group(1)
    print("{} version {} contains upstream {}'s version {}".format(release_repo, release_version, pr_repo, gem_version))

upstream_version = "v{}".format(gem_version)

commit_sha = requests.get(pr_url.format(pr_repo, pr_number)).json()['merge_commit_sha']
print("commit_sha for repo {} PR#{}: {}".format(pr_repo, pr_number, commit_sha))

compare_status = requests.get(compare_url.format(pr_repo, commit_sha, upstream_version)).json()['status']

if compare_status == 'identical' or compare_status == 'ahead':
  print("this package includes your PR!")
else:
  print("this package does not have your PR!")
