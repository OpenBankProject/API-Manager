const schema = {};
const json = [
    {
        key: 'url',
        value: 'http://localhost:8080'
    },
    {
        "key":"outBoundMapping",
        "value":{
            "cc":{
                "cId":"outboundAdapterCallContext.correlationId"
            },
            "bankId":"bankId.value + 'helloworld'",
            "originalJson":"$root"
        }
    },
    {
        "key":"inBoundMapping",
        "value":{
            "inboundAdapterCallContext$default":{
                "correlationId":"correlation_id_value",
                "sessionId":"session_id_value"
            },
            "status$default":{
                "errorCode":"",
                "backendMessages":[]
            },
            "data":{
                "bankId":{
                    "value":"result.bank_id"
                },
                "shortName":"result.name",
                "fullName":"'full: ' + result.name",
                "logoUrl":"result.logo",
                "websiteUrl":"result.website",
                "bankRoutingScheme[0]":"result.routing.routing_scheme",
                "bankRoutingAddress[0]":"result.routing.routing_address",
                "swiftBic":"result.swift_bic",
                "nationalIdentifier":"result.national"
            }
        }
    }];

const options = {
    mode: 'code',
    modes: ['code', 'text', 'tree', 'preview']
};

// create the editor
const container = document.getElementById('jsoneditor');
const editor = new JSONEditor(container, options, json);