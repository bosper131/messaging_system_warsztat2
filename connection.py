from psycopg2 import connect
from settings import dbinfo


def get_connection(settings=None,autocommit = True):
    if settings is None:
        settings = dbinfo
    cnx = connect(**settings)  #jak masz podkreslone i "shadows" i on to rozumie jako nazwę własną stąd trzeba pamietać żeby nie nazywać tak zmiennej ale w samych funkcjach to luz, można
    cnx.autocommit = autocommit
    return cnx

if __name__=="__main__":   #sprawdzasz tylko czy to działa w pewien sposób na małym kodzie, uruchamiamy gdy tylko ten plik odpalamy a nie wszystkie importowalne
    connection = get_connection()
    connection.close()