#!/usr/bin/env bash
URL="https://api.github.com/repos/${GITHUB_REPO}/pulls/${PR_NUMBER}/files"
FILES=$(curl -s -X GET -G $URL | jq -r '.[] | .filename')

cat<<EOF
CHANGED FILES:
$FILES

EOF

echo ${FILES}
if [[ "${FILES}" =~ (pyhtzee\/.+\.py|setup\.py) ]]; then
  echo "Detected changed python files... Exiting with FAILURE code"
  exit 1
fi
echo "No python changes... Exiting with SUCCESS code"
exit 0
