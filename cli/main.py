from typing import Optional
import os
import requests

import typer
from datetime import datetime


base_url ='http://backend:8000'
app = typer.Typer()


@app.command()
def login(
    username:str = typer.Option(..., prompt=True),
    password: str = typer.Option(
        ..., prompt=True, hide_input=True
    )
):
    delete_token()
    # Command for user's login
    form_data = {
        "username": username,
        "password": password
    }
    response = requests.post(f'{base_url}/user/login', data=form_data)

    result = response.json()

    if response.status_code == 200:
        store_token(result['access_token'])
        typer.echo("User logged in successfully! ✅")

    elif response.status_code == 401:
        typer.echo("Invalid user credentials! ❌")

    elif response.status_code == 404:
        typer.echo("User not found! ❌")

    else:
        typer.echo(f"Oh-no! 😐: {response.json()['detail'][0]['msg']}")

@app.command()
def logout():

    token = get_token()
    if len(token) <= 0:
        print("You are not logged in!")
        raise typer.Abort()

    logout = typer.confirm("Are you sure you want to logout?")
    if not logout:
        print("Not action required! (Still logged in!)")
        raise typer.Abort()
    
    print("Signing off...")

    delete_token()
    print("Signed out! ✅")


@app.command()
def downloadfile(stations_id: int = typer.Option(..., "--station", '-s', help="Please specify AQ Station ID"), from_date: datetime = typer.Option(..., "--from", '-f', help="Please specify from date"), to_date:datetime = typer.Option(..., "--to", '-t', help="Please specify to date")):
    """
    Download a file by name.
    """

    from_date_format = from_date.strftime('%Y-%m-%d')
    to_date_format = to_date.strftime('%Y-%m-%d')

    # Demo command to run this
    # downloadfile -s 100031007 --from 2022-11-01 --to 2022-11-15

    if stations_id == None:
         typer.echo(f"Please specify correct stations_id")
         raise typer.Exit()
    
    if from_date == None or to_date == None:
         typer.echo(f"Please specify correct date range")
         raise typer.Exit()

    token = get_token()
    
    if len(token) <= 0:
        typer.echo("Please login first to get the file link!")

    else:
        print("Generating file...")
        response = requests.get(f"{base_url}/aircast/get-data-by-site?station_name={stations_id}&start_date={from_date_format}&end_date={to_date_format}", headers={"Authorization":f"Bearer {token}"})  


        if response.status_code == 200:
            data = response.json()
            typer.echo(f"Downloadable file link: {data['file_url']}")
        
        elif response.status_code == 404:
            data = response.json()
            typer.echo(f"File with name not found!")

        elif response.status_code == 503:
            data = response.json()
            typer.echo(f"API limit reached! Please upgrade to higher plan.")

        elif response.status_code == 400:
            data = response.json()
            typer.echo(data['message'])

        else:
            typer.echo(response.content)
            



def store_token(token:str):
    if not os.path.exists('config'):
        os.makedirs('config')
        print('data directory created successfully')

    with open("config", "w") as text_file:
        text_file.write(token)
        text_file.close()

def get_token():
    with open("config", "r") as text_file:
        data = text_file.read()
        text_file.close()

    return data

def delete_token():
    f = open("config", "r+") 
    f.seek(0) 
    f.truncate() 

if __name__ == "__main__":
    app()