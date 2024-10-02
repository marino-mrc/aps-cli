import requests
import sys
import typer 
import os
from requests.auth import HTTPBasicAuth


def is_bit_set(x, n):
    #return x & 2 ** n != 0 
    # a more bitwise- and performance-friendly version:
    return x & 1 << n != 0

def print_msg(msg, debug_msg=False, debug_status=False):
    if debug_msg == False:
        typer.echo(msg)
    elif debug_status == True:
        typer.echo(msg)

# Returns 2 values:
# 1. error state = {True, False}
# 2. A message containing the response from the server or the exception message in case of errors
def do_get(url, username=None, password=None, headers=None, params=None, debug=False, verify=False):
    response = None
    basicAuth = None
    if username != None and password != None:
        basicAuth = HTTPBasicAuth(username, password)
    try:
        if debug == True:
            print_msg("GET Request --> {}\nParams = {}\nAuthentication = {}".format(url, params, basicAuth))
        if basicAuth != None:
            response = requests.get(url, auth=basicAuth, params=params, headers=headers, timeout=15, verify=verify)
        else:
            response = requests.get(url, params=params, headers=headers, timeout=15, verify=verify)
        response.raise_for_status()
        if debug == True and response is not None:
            print_msg("GET Response <-- {}".format(response.content))
        return False, response
    except requests.exceptions.HTTPError as error:
        error_message = "HttpError: {}".format(error)
    except requests.exceptions.TooManyRedirects as error:
        error_message = "TooManyRedirectsError: {}".format(error)
    except requests.Timeout as error:
        error_message = "TimeoutError: {}".format(error)
    except requests.exceptions.RequestException as error:
        error_message = "ConnectionError: {}".format(error)
    except Exception as error:
        error_message = "GenericError: {}".format(error)
    return True, error_message

# Returns 2 values:
# 1. error state = {True, False}
# 2. A message containing the response from the server or the exception message in case of errors
def do_post(url, username=None, password=None, headers=None, data=None, files=None, json=None, debug=False, verify=False):
    response = None
    basicAuth = None
    if username != None and password != None:
        basicAuth = HTTPBasicAuth(username, password)
    try:
        if debug == True:
            print_msg("POST Request --> {} - Authentication = {}".format(url, basicAuth))
        if basicAuth != None:
            response = requests.post(url, auth=basicAuth, headers=headers, data=data, files=files, json=json, timeout=15, verify=verify)
        else:
            response = requests.post(url, headers=headers, data=data, files=files, json=json, timeout=15, verify=verify)
        
        response.raise_for_status()
        if debug == True and response is not None:
            print_msg("POST Response <-- {}".format(response.text))
        return False, response
    # Additional code will only run if the request is successful
    except requests.exceptions.HTTPError as error:
        error_message = "HttpError: {}".format(error)
    except requests.exceptions.TooManyRedirects as error:
        error_message = "TooManyRedirectsError: {}".format(error)
    except requests.Timeout as error:
        error_message = "TimeoutError: {}".format(error)
    except requests.exceptions.RequestException as error:
        error_message = "ConnectionError: {}".format(error)
    except Exception as error:
        error_message = "GenericError: {}".format(error)
    return True, error_message

def do_delete(url, headers=None, params=None, verify=True):
    response = None
    try:
        response = requests.delete(url, headers=headers, params=params, timeout=15, verify=verify)
        response.raise_for_status()
        return False, response
        # Additional code will only run if the request is successful
    except requests.exceptions.HTTPError as error:
        message = "HttpError: {}".format(error)
    except requests.exceptions.TooManyRedirects as error:
        message = "TooManyRedirectsError: {}".format(error)
    except requests.Timeout as error:
        message = "TimeoutError: {}".format(error)
    except requests.exceptions.RequestException as error:
        message = "ConnectionError: {}".format(error)
    except Exception as error:
        message = "GenericError: {}".format(error)
    return True, error_message