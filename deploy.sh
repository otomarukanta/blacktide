cat << EOF >> ./scrapinghub.yml
apikeys:
  default: ${SCRAPINGHUB_APIKEY}
EOF

shub deploy
