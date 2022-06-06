import mysql.connector

def connexionBD():
    
    conn = mysql.connector.connect(
        host = "mydbserveur.mysql.database.azure.com",
        user = "kerfalla@mydbserveur",
        port = 3306,
        database = "ProjetTransverse1DB",
        password = "....", # tu mets le mot de passe.
        ssl_ca = "C:\BaltimoreCyberTrustRoot.crt.pem"
    )

    cursor = conn.cursor()

    query = "select * from ProjetTransverse1DB.users"

    cursor.execute(query)

    print(cursor.fetchall())

def main():
    connexionBD()

if __name__ == "__main__":
    main()
    
