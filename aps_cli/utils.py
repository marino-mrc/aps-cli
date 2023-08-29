import requests
import sys
import typer 
import os
from requests.auth import HTTPBasicAuth

def print_msg(msg, debug_msg=False, debug_status=False):
    if debug_msg == False:
        typer.echo(msg)
    elif debug_status == True:
        typer.echo(msg)

def do_get(url, username=None, password=None, headers=None, params=None):
    response = None
    basicAuth = None
    if username != None and password != None:
        basicAuth = HTTPBasicAuth(username, password)
    try:
        if basicAuth != None:
            response = requests.get(url, auth=basicAuth, params=params, headers=headers)
        else:
            response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as error:
        print("HttpError: ",error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)
        # This code will run if there is a 404 error
    except requests.exceptions.TooManyRedirects as error:
        print("TooManyRedirectsError: ", error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)
    except requests.Timeout as error:
        print("TimeoutError: ", error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)
    except requests.exceptions.RequestException as error:
        print("ConnectionError: ", error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)

def do_post(url, username=None, password=None, headers=None, data=None, files=None, json=None):
    response = None
    basicAuth = None
    if username != None and password != None:
        basicAuth = HTTPBasicAuth(username, password)
    try:
        if basicAuth != None:
            response = requests.post(url, auth=basicAuth, headers=headers, data=data, files=files, json=json)
        else:
            response = requests.post(url, headers=headers, data=data, files=files, json=json)
        response.raise_for_status()
        return response
        # Additional code will only run if the request is successful
    except requests.exceptions.HTTPError as error:
        print("HttpError: ",error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)
        # This code will run if there is a 404 error
    except requests.exceptions.TooManyRedirects as error:
        print("TooManyRedirectsError: ", error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)
    except requests.Timeout as error:
        print("TimeoutError: ", error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)
    except requests.exceptions.RequestException as error:
        print("ConnectionError: ", error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)


def do_delete(url, headers=None, params=None):
    response = None
    try:
        response = requests.delete(url, headers=headers, params=params)
        response.raise_for_status()
        return response
        # Additional code will only run if the request is successful
    except requests.exceptions.HTTPError as error:
        print("HttpError: ",error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)
        # This code will run if there is a 404 error
    except requests.exceptions.TooManyRedirects as error:
        print("TooManyRedirectsError: ", error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)
    except requests.Timeout as error:
        print("TimeoutError: ", error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)
    except requests.exceptions.RequestException as error:
        print("ConnectionError: ", error)
        if response is not None:
            print("Response: ", response.content)
        raise typer.Exit(1)
