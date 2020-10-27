# -*- coding: utf-8 -*-
"""
Views of config app
"""

import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from obp.api import API, APIError
from base.utils import exception_handle, error_once_only
from .forms import DynamicEndpointsForm
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt


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
        except APIError as err:
            error_once_only(self.request, Exception("OBP-API server is not running or do not response properly. "
                                                   "Please check OBP-API server.    "
                                                   "Details: " + str(err)))
        except BaseException as err:
            error_once_only(self.request, (Exception("Unknown Error. Details:" + str(err))))
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
                                        "$ref":"#/definitions/user"
                                    }
                                }],
                                "responses":{
                                    "201":{
                                        "description":"create user successful and return created user object",
                                        "schema":{
                                            "$ref":"#/definitions/user"
                                        }
                                    },
                                    "500":{
                                        "description":"unexpected error",
                                        "schema":{
                                            "$ref":"#/responses/unexpectedError"
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
                                            "$ref":"#/definitions/user"
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
                                            "$ref":"#/definitions/APIError"
                                        }
                                    },
                                    "500":{
                                        "description":"unexpected error",
                                        "schema":{
                                            "$ref":"#/responses/unexpectedError"
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
                                            "$ref":"#/definitions/users"
                                        }
                                    },
                                    "404":{
                                        "description":"user not found",
                                        "schema":{
                                            "$ref":"#/definitions/APIError"
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
                                        "$ref":"#/definitions/user"
                                    }
                                }],
                                "responses":{
                                    "200":{
                                        "description":"create user successful and return created user object",
                                        "schema":{
                                            "$ref":"#/definitions/user"
                                        }
                                    },
                                    "500":{
                                        "description":"unexpected error",
                                        "schema":{
                                            "$ref":"#/responses/unexpectedError"
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
                                        "description":"unexpected error",
                                        "schema":{
                                            "$ref":"#/responses/unexpectedError"
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
                                "$ref":"#/definitions/user"
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
                            "description":"unexpected error",
                            "schema":{
                                "$ref":"#/definitions/APIError"
                            }
                        },
                        "invalidRequest":{
                            "description":"invalid request",
                            "schema":{
                                "$ref":"#/definitions/APIError"
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
    parameters_Json_editor = request.POST.get('parameters_Json_editor')
    api = API(request.session.get('obp'))
    urlpath = '/management/dynamic-endpoints'
    result = api.post(urlpath, payload=json.loads(parameters_Json_editor) )
    return result


@exception_handle
@csrf_exempt
def dynamicendpoints_delete(request):
    dynamic_endpoint_id = request.POST.get('dynamic_endpoint_id')

    api = API(request.session.get('obp'))
    urlpath = '/management/dynamic-endpoints/{}'.format(dynamic_endpoint_id)
    result = api.delete(urlpath)
    return result
