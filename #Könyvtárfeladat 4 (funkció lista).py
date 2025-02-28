import sqlite3

conn=sqlite3.connect("KÖnyvtárfeladat_funkciókkal.db")
cursor=conn.cursor()

# Összefűzés és kiiratás
def könyveklistája():
    cursor.execute("""
               SELECT könyv.id, könyv.cím, könyv.kiadás_éve, szerző.név, kölcsönzés.állapot
               FROM könyv 
               JOIN szerző ON könyv.szerző_id=szerző.id
               JOIN kölcsönzés ON könyv.kölcsönzés_id=kölcsönzés.id
               """)
    for x in cursor.fetchall():
        print(x)



# Könyvadatok lekérdezése

def könyvlekérdezés():
    könyveklistája()
    x=int(input(f"Melyik könyv érdekel (Könyv id)?"))
    #x=(x,)
    cursor.execute("""
               SELECT könyv.id, könyv.cím, könyv.kiadás_éve, szerző.név, kölcsönzés.állapot
               FROM könyv 
               JOIN szerző ON könyv.szerző_id=szerző.id
               JOIN kölcsönzés ON könyv.kölcsönzés_id=kölcsönzés.id
               WHERE könyv.id=?
               """,(x,))
    adatok=cursor.fetchone()
    print(adatok)
    return x

#könyvlekérdezés()

# kölcsönzés

def kölcsönzés ():
    könyveklistája()
    x=input("Melyik könyvet szeretnéd kikölcsönözni?")
    x=(x,)
    cursor.execute("""
                   SELECT könyv.cím, könyv.kölcsönzés_id
                   FROM könyv
                   WHERE cím=?
                   """, (x) )
    y=1
    állapot=cursor.fetchone()
    print (állapot)
    if y in állapot: print("Sajnálom a könyv pont ki van kölcsönözve.")
    else: print ("Ön sikeresen kikölcsönözte a könyvet")
    conn.commit()

#kölcsönzés()


#könyvhozzáadás

def könyvhozzáadás():

# Ellenőrzés, hogy a könyv bent van-e már az adatbázisban
    x=(input("Mi a könyv címe?"),)
    if len(x)<1 : x=("The Stone Sky",)
    cursor.execute("SELECT könyv.cím FROM könyv")
    if x in cursor.fetchall(): 
        print("Ez a könyv ---", x[0],  "--- már szerepel az adatbázisunkban.")
    
    else: pass

# Megszerezzük a szerző ID-ját és ha még nincs a táblázatban, akkor beleírjuk.

    y=(input("Ki írta?"),)
    if len(y)<1 : y= ("N.K. Jemisin",)
    cursor.execute("SELECT szerző.név FROM szerző")
    if y in cursor.fetchall():
        cursor.execute ("""SELECT szerző.id FROM szerző WHERE név=?""", (y))
        y=cursor.fetchone()
        print(y)
    else:
        cursor.execute("""
                       INSERT INTO szerző (név)
                       VALUES (?)""", y)
        cursor.execute ("""SELECT szerző.id FROM szerző WHERE név=?""", (y))
        y=cursor.fetchone()
        print(y)

# Összefűzzük az adatokat, hogy a könyv listához hozzá lehessen adni.

    z=(input("Mikor adták ki?"),)
    if len(z)<1 : z= (2017,)
    könyvadatok=[x[0], z[0], y[0], 2,]
    #print(könyvadatok)
    
# Hozzáadás a sqlite-hez
    
    cursor.execute("""
                   INSERT INTO könyv (cím, kiadás_éve, szerző_id, kölcsönzés_id)
                   VALUES (?,?,?,?)""", (könyvadatok) )
    
    cursor.execute(""" SELECT szerző.név, könyv.cím, könyv.kiadás_éve, kölcsönzés.állapot
                   FROM könyv 
                   JOIN szerző ON könyv.szerző_id=szerző.id
                   JOIN kölcsönzés ON könyv.kölcsönzés_id=kölcsönzés.id
                   WHERE könyv.cím=?""", (x))
    print(cursor.fetchone())
    print("Megfelelőek a fenti adatok?\n1-Igen\n2-Nem")
    mentés=int(input())
    if mentés == 1 : conn.commit()
    else:
        print ("Akkor kezdhetjük előről...")
        könyvhozzáadás()

# Könyv törlése sqlite-ból

def könyvtörlés():
    print("Melyik sorszámú könyvet szeretné törölni az alábbikból ")
    x=könyvlekérdezés()
    print(f"Biztosan törölni szeretné a fenti könyvet?")    
    y=int(input("1-Igen/ 2-Nem"))
    if y<2:
        cursor.execute(""" DELETE FROM könyv WHERE id=?""", (x,))
        print(f"A könyvet törlöltük, ezek maradtak")
        conn.commit()
        print(f"{könyveklistája()}")
    else:
        print ("Akkor kezdhetjük előről...")
        feladatválasztó()


  
def feladatválasztó():
    lehetőségek={1: könyveklistája, 2:könyvlekérdezés, 3:kölcsönzés, 4:könyvhozzáadás, 5:könyvtörlés} 
    lehetőségek_display={1:"könyveklistája", 2:"könyvlekérdezés", 3:"könyvkölcsönzés", 4:"könyvhozzáadás", 5:"könyvtörlés"}
    def feladatválasztó_lista():
        for k, v in lehetőségek_display.items():
            print(k, v)

    print("Szolgáltalásaink:")
    feladatválasztó_lista()
    x=int(input("Mit szeretnél csinálni?"))
    lehetőségek[x]()
    

feladatválasztó()
#könyvhozzáadás()
#továbblépés=(input("Szeretnéd a listát is megnézni? y/n"))
#if továbblépés==y:könyveklistája()
#könyveklistája()


#A program eleje mindig lefut ezért mindig hozzáadódik a három könyv a listához. JAvítsd ki!!!

#2. Hibák és hiányosságok / Nem megfelelő zárójelezés és változókezelés: / A könyvlekérdezés függvényben a cursor.execute parancsban (x) helyett (x,) kellene. Enélkül hibát okozhat.

# A kölcsönzés függvény logikája hibás: Itt az if y in állapot ellenőrzés nem fog megfelelően működni, mivel a fetchone() visszatérési értéke egy tuple. Ehelyett így kellene ellenőrizni:

# A könyvhozzáadás függvény nehezen követhető: Túl sok a beágyazott ellenőrzés és input, ami megnehezíti a karbantartást. A felhasználói interakciókat érdemes külön kezelni.

# Kódismétlés: Többször előfordul, hogy cursor.execute hívásokat ismételsz hasonló célokra. Ezeket érdemes lenne külön függvényekbe szervezni.

# 3. Javított változat és javasolt fejlesztések: /A változtatások mellett érdemes lenne további funkciókat hozzáadni, például:
   #Hibakezelés (try-except blokkok).
   #Bemenet érvényesítése (üres inputok vagy érvénytelen adatok kiszűrése).
   #Kód újrastrukturálása a könnyebb olvashatóság érdekében.
