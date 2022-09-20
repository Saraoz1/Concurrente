import time
from unittest import result
import json
import requests
import mysql.connector
import threading
from pytube import YouTube

def download_video():
    urls_video = ["https://www.youtube.com/watch?v=bp_IXqYRgYw","https://www.youtube.com/watch?v=fTNdKMxrWj8","https://www.youtube.com/watch?v=R2CMwGzsYgQ","https://www.youtube.com/watch?v=3eY024i_1NA","https://www.youtube.com/watch?v=6HfmxmHhvKs"]
    destino = ("home/esaaa/Descargas/kkkk/")
    for link in urls_video:
      yt = YouTube(link)
      video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first() 
      save_video(video,destino)


def save_video(video,destino):    
    video.download(destino)
    print("El video ha sido descargado en la ruta: "+destino)

def get_service2():
    x=0
    nombres=[]
    for x in range(0,50) : 
        response = requests.get('https://randomuser.me/api/')
        if response.status_code == 200:
            print(x)
            results = response.json().get('results')
            name = results[0].get('name').get('first')
            nombres.append(name)
            print(nombres)

def get_service():
    urlPoke = 'https://pokeapi.co/api/v2/pokemon?limit=5000&offset=0'
    data = requests.get(urlPoke)
    if data.status_code == 200:
        data = data.json()
        results = data.get('results', [])
        if results:
            print("Iniciando insercion de pokemones")
            for x in results:
                name = x['name']
                write_db(name)
            print("fin de subproceso pokemon")
            return results


def write_db(name):
 conexion = mysql.connector.connect(
        user='root',
        password='1234',
        host='localhost',
        database='Poke',
        port='3306'
    )
 mycursor = conexion.cursor()
 sql = "INSERT INTO pokemon(pokemon) VALUES ('{0}')".format(name)
 mycursor.execute(sql)
 conexion.commit()

if __name__ == "__main__":
    
        th1 = threading.Thread(target=get_service2)
        th1.start()
        th1.join()
        
        th2 = threading.Thread(target=get_service)
        th2.start()

        th3 = threading.Thread(target=download_video)
        th3.start()

    
        th2.join()
        th3.join()
        print("fin de los subprocesos")