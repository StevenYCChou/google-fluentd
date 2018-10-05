# get the fluent-plugin-google-cloud version of google-fluentd v1.5.35 
curl https://raw.githubusercontent.com/GoogleCloudPlatform/google-fluentd/v1.5.35/plugin_gems.rb | sed -n 's/download \"fluent-plugin-google-cloud\", \"\(.*\)\"/\1/p'

# get the change of google-fluentd made from v1.5.35 to v1.5.36
curl https://api.github.com/repos/GoogleCloudPlatform/google-fluentd/compare/v1.5.35...v1.5.36 | jq '[.commits[] | .commit.message]'

