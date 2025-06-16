from kullanicilar.model.model import kullanici 


kullanicilar = [
    
         kullanici(id= 1,   name="baris", email="baris@gmail.com"),
         kullanici(id= 2,   name="umut", email="umut@gmail.com"),
         kullanici(id= 3,   name="mami", email="mami@gmail.com"),
         kullanici(id= 4,   name="dogan", email="dogan@gmail.com"),
]

def get_all_kullanicilar():
    return kullanicilar


def get_kullanici_id(kullanici_id: int):
    for kullanici in kullanicilar:
        if kullanici.id == kullanici_id:
            return kullanici

    return{"error": "kullanici bulunamadi."}


        

