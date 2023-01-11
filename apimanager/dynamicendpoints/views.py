# -*- coding: utf-8 -*-
"""
Views of config app
"""

import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from obp.api import API, APIError
from base.utils import exception_handle, error_once_only
from .forms import DynamicEndpointsForm
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

DEFINITIONS_USER = "#/definitions/user"
UNEXPECTED_ERROR = "unexpected error"
RESPONSES_UNEXPECTED_ERROR = "#/responses/unexpectedError"
DEFINITIONS_API_ERROR = "#/definitions/APIError"

class IndexView(LoginRequiredMixin, FormView):
    """Index view for config"""
    template_name = "dynamicendpoints/index.html"
    form_class = DynamicEndpointsForm
    success_url = reverse_lazy('dynamicendpoints-index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        api = API(self.request.session.get('obp'))
        urlpath = '/management/dynamic-endpoints'
        dynamic_endpoints =[]
        try:
            response = api.get(urlpath)
            if 'code' in response and response['code'] >= 400:
                error_once_only(self.request, response['message'])
            else:
                dynamic_endpoints=response['dynamic_endpoints']
                #Accessing API-Explorer URL, parameters API-Collection Id and selected Language
                for locale in dynamic_endpoints:
                    locale["dynamicendpoint_on_api_explorer_url"] = f"{settings.API_EXPLORER}/?api-dynamic_endpoint-id={locale['dynamic_endpoint_id']}"
        except APIError as err:
            messages.error(self.request, err)
        except Exception as err:
            error_once_only(self.request, err)
        else:
            # set the default endpoint there, the first item will be the new endpoint.
            default_dynamic_endpoint = {
                "dynamic_endpoint_id":"Try the new endpoint: ",
                "swagger_string":{
                    "swagger":"2.0",
                    "info":{
                        "version":"0.0.1",
                        "title":"Example Title",
                        "description":"Example Description",
                        "contact":{
                            "name":"Example Company",
                            "email":"simon@example.com",
                            "url":"https://www.tesobe.com/"
                        }
                    },
                    "host":"localhost:8080",
                    "basePath":"/user",
                    "schemes":["http"],
                    "consumes":["application/json"],
                    "produces":["application/json"],
                    "paths":{
                        "/save":{
                            "post":{
                                "parameters":[{
                                    "name":"body",
                                    "in":"body",
                                    "required":True,
                                    "schema":{
                                        "$ref":DEFINITIONS_USER
                                    }
                                }],
                                "responses":{
                                    "201":{
                                        "description":"create user successful and return created user object",
                                        "schema":{
                                            "$ref": DEFINITIONS_USER
                                        }
                                    },
                                    "500":{
                                        "description":UNEXPECTED_ERROR,
                                        "schema":{
                                            "$ref":RESPONSES_UNEXPECTED_ERROR
                                        }
                                    }
                                }
                            }
                        },
                        "/getById/{userId}":{
                            "get":{
                                "description":"get reuested user by user ID",
                                "parameters":[{
                                    "$ref":"#/parameters/userId"
                                }],
                                "consumes":[],
                                "responses":{
                                    "200":{
                                        "description":"the successful get requested user by user ID",
                                        "schema":{
                                            "$ref":DEFINITIONS_USER
                                        }
                                    },
                                    "400":{
                                        "description":"bad request",
                                        "schema":{
                                            "$ref":"#/responses/invalidRequest"
                                        }
                                    },
                                    "404":{
                                        "description":"user not found",
                                        "schema":{
                                            "$ref":DEFINITIONS_API_ERROR
                                        }
                                    },
                                    "500":{
                                        "description":UNEXPECTED_ERROR,
                                        "schema":{
                                            "$ref":RESPONSES_UNEXPECTED_ERROR
                                        }
                                    }
                                }
                            }
                        },
                        "/listUsers":{
                            "get":{
                                "description":"get list of users",
                                "consumes":[],
                                "responses":{
                                    "200":{
                                        "description":"get all users",
                                        "schema":{
                                            "$ref":DEFINITIONS_USER
                                        }
                                    },
                                    "404":{
                                        "description":"user not found",
                                        "schema":{
                                            "$ref":DEFINITIONS_API_ERROR
                                        }
                                    }
                                }
                            }
                        },
                        "/updateUser":{
                            "put":{
                                "parameters":[{
                                    "name":"body",
                                    "in":"body",
                                    "required":True,
                                    "schema":{
                                        "$ref":DEFINITIONS_USER
                                    }
                                }],
                                "responses":{
                                    "200":{
                                        "description":"create user successful and return created user object",
                                        "schema":{
                                            "$ref":DEFINITIONS_USER
                                        }
                                    },
                                    "500":{
                                        "description":UNEXPECTED_ERROR,
                                        "schema":{
                                            "$ref":RESPONSES_UNEXPECTED_ERROR
                                        }
                                    }
                                }
                            }
                        },
                        "/delete/{userId}":{
                            "delete":{
                                "description":"delete user by user ID",
                                "parameters":[{
                                    "$ref":"#/parameters/userId"
                                }],
                                "consumes":[],
                                "responses":{
                                    "204":{
                                        "description":"the successful delete user by user ID"
                                    },
                                    "400":{
                                        "description":"bad request",
                                        "schema":{
                                            "$ref":"#/responses/invalidRequest"
                                        }
                                    },
                                    "500":{
                                        "description":UNEXPECTED_ERROR,
                                        "schema":{
                                            "$ref":RESPONSES_UNEXPECTED_ERROR
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "definitions":{
                        "user":{
                            "type":"object",
                            "properties":{
                                "id":{
                                    "type":"integer",
                                    "description":"user ID"
                                },
                                "first_name":{
                                    "type":"string"
                                },
                                "last_name":{
                                    "type":"string"
                                },
                                "age":{
                                    "type":"integer"
                                },
                                "career":{
                                    "type":"string"
                                }
                            },
                            "required":["first_name","last_name","age"]
                        },
                        "users":{
                            "description":"array of users",
                            "type":"array",
                            "items":{
                                "$ref":DEFINITIONS_USER
                            }
                        },
                        "APIError":{
                            "description":"content any error from API",
                            "type":"object",
                            "properties":{
                                "errorCode":{
                                    "description":"content error code relate to API",
                                    "type":"string"
                                },
                                "errorMessage":{
                                    "description":"content user-friendly error message",
                                    "type":"string"
                                }
                            }
                        }
                    },
                    "responses":{
                        "unexpectedError":{
                            "description":UNEXPECTED_ERROR,
                            "schema":{
                                "$ref":DEFINITIONS_API_ERROR
                            }
                        },
                        "invalidRequest":{
                            "description":"invalid request",
                            "schema":{
                                "$ref":DEFINITIONS_API_ERROR
                            }
                        }
                    },
                    "parameters":{
                        "userId":{
                            "name":"userId",
                            "in":"path",
                            "required":True,
                            "type":"string",
                            "description":"user ID"
                        }
                    }
                }
            }
            dynamic_endpoints.insert(0,default_dynamic_endpoint)
            
            # replace all the json list to json object.
            for i in range(len(dynamic_endpoints)):
                dynamic_endpoints[i]['swagger_string'] = json.dumps(dynamic_endpoints[i]['swagger_string'])
            context.update({
                'dynamic_endpoints': dynamic_endpoints
            })
        return context

@exception_handle
@csrf_exempt
def dynamicendpoints_save(request):
    parameters_Json_editor_dynamic = request.POST.get('parameters_Json_editor')
    api = API(request.session.get('obp'))
    urlpath = '/management/dynamic-endpoints'
    result = api.post(urlpath, payload=json.loads(parameters_Json_editor_dynamic) )
    return result


@exception_handle
@csrf_exempt
def dynamicendpoints_delete(request):
    dynamic_endpoint_id = request.POST.get('dynamic_endpoint_id')

    api = API(request.session.get('obp'))
    urlpath = '/management/dynamic-endpoints/{}'.format(dynamic_endpoint_id)
    result = api.delete(urlpath)
    return result
