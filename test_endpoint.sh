#!/bin/bash

emergency() {
    set +x

    if [ "$1" == "STAGE" ];
    then
        ENV_ENDPOINT="https://alura-drf-school-stage.sorocaba.sp.gov.br/emergency/"
    else
        ENV_ENDPOINT="http://alura-drf-school-local.sorocaba.sp.gov.br:8000/emergency/"
    fi

    # TODO use another geom format: WKT
    # -F "geom=SRID=31983;POINT (334084.6591700006 7396449.925171347)" \

    curl -i -X POST -F "photo01=@/home/jecampos/universal/projects/pms/defesa_civil/images/flood01.jpg" \
         -F "nivel_agua=ALTO" \
         -F "data_pedido_ajuda=2024-10-04T12:37:45.983520-03:00" \
         -F "nome_completo=Test cUrl 01" \
         -F "cpf=17856324980" \
         -F "telefone01=15991234470" \
         -F "telefone02=" \
         -F "endereco_ajuda=Rua Test cUrl 01" \
         -F "complemento=158" \
         -F "pedido_relatado=Help! Flood!!" \
         -F "adultos=1" \
         -F "criancas=0" \
         -F "idosos=0" \
         -F "deficientes=0" \
         -F "acamados=0" \
         -F "animais=0" \
         -F "beira_corrego=false" \
         $ENV_ENDPOINT
}

student() {
    #URL=$BASE_ENDPOINT/school/students/
    #set -x
    #curl -i -H 'Accept-Language: pt-br' -u $CREDENTIALS -X GET $URL

    generic_get "school/students/"
}

course() {
    generic_get "school/courses/"
}

generic_get() {
    URL="$BASE_ENDPOINT/$1"

    set -x
    # curl -v -i -H 'Accept-Language: pt-br' -u $CREDENTIALS -X GET $URL
    curl -H 'Accept-Language: pt-br' -u $CREDENTIALS -X GET $URL
    # To test other content type
    #curl -u $CREDENTIALS -H "Accept: application/xml" -X GET $URL/school/students/201/
    #curl -u $CREDENTIALS -H "Accept: application/yaml" -X GET $URL/school/students/201/
    
}

auth() {
    set +x

    if [ "$1" == "NO_AUTH" ];
    then
        AUTH_HEADER=""
    elif [ "$1" == "INVALID_AUTH" ];
    then
        AUTH_HEADER="Authorization: INVALID $API_AUTHORIZATION_TOKEN WRONG"
    elif [ "$1" == "IGNORE_AUTH" ];
    then
        AUTH_HEADER="Authorization: IGNORED $API_AUTHORIZATION_TOKEN"
    elif [ "$1" == "ERR_AUTH" ];
    then
        AUTH_HEADER="Authorization: Api-Key MY_CUSTOM_FAKE_TOKEN"
    else
        AUTH_HEADER="Authorization: Api-Key $API_AUTHORIZATION_TOKEN"
    fi
    URL="$BASE_ENDPOINT/emergency/protected_test_custom_auth/"
    echo "$URL -- $AUTH_HEADER"

    curl -i -X GET $URL -H "$AUTH_HEADER"
}

API_USER="$(cat .env | grep API_USER | cut -d = -f2 | sed -n '1,1p')"
API_PASS="$(cat .env | grep API_PASS | cut -d = -f2 | sed -n '1,1p')"
CREDENTIALS="$API_USER:$API_PASS"

case $2 in
    "LOCAL") BASE_ENDPOINT="http://alura-drf-school-local.sorocaba.sp.gov.br:8000";;
    "DEV") BASE_ENDPOINT="https://alura-drf-school-dev.sorocaba.sp.gov.br";;
    "STAGE") BASE_ENDPOINT="https://alura-drf-school-stage.sorocaba.sp.gov.br";;
    "PROD") BASE_ENDPOINT="https://alerta-defesa-civil-api.sorocaba.sp.gov.br";;
    *) echo "USAGE: [LOCAL | DEV | STAGE | PROD]. $2 *NOT* found!!"
esac

case $1 in
    "emergency") emergency $2;;
    "student") student $2;;
    "course") course $2;;
    "gen_get") generic_get $3 $4;;
    "auth") auth $3;;
    *) echo "USAGE: [emergency | guideline | flood | auth | help] [LOCAL | DEV | STAGE | PROD]. $1 *NOT* found!!"
esac
