#!/bin/bash
# gettoken.sh
# Test program to get a login token from a server then loop
# getting protected data from that same server.
# If the token has expired, re-negotiate a new token
# and continue the loop.
#
# This is test code only.
#
# David Cook, 2020
#

USERACCT='fred'
USERPASS='password'
SERVER=localhost:5000

get_token(){
  token=$(curl --user ${USERACCT}:${USERPASS} http://${SERVER}/login 2>/dev/null | \
     jq .token | sed 's/"//g')
}

# MAIN
get_token

for x in {1..40}
do
  sleep 2
  tmp=$(curl http://${SERVER}/protected?token=${token} 2>/dev/null | \
      jq .message | sed 's/"//g')
  echo "#${x} : ${tmp}"

  invalid=$(echo ${tmp} | grep "FAIL" | wc -l)
  if [ ${invalid} -ne 0 ]; then
     echo "Token has expired ... re-negotiating."
     get_token
     [ ${#token} -gt 100 ] && echo " -- token renegotiation successful"
     tmp=$(curl http://${SERVER}/protected?token=${token} 2>/dev/null | \
         jq .message | sed 's/"//g')
     echo "#${x} : ${tmp}"
  fi

done

#
# EOF
#

