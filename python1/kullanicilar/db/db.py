from kullanicilar.model.model import kullaniciInDB

fake_kullanici_db = {
    "test@example.com": kullaniciInDB(
        id=1,
        email="test@example.com",
        name="baris",
        hashed_password="$2b$12$Tw1JBtsMpGaw732WhSPLmecBzSPy0bdkLBGz6kPupMSnBK1hPt4/a",  # şifre: 123
        is_admin=True  # Admin kullanıcı
    ),
    "user@example.com": kullaniciInDB(
        id=2,
        email="user@example.com", 
        name="umut",
        hashed_password="$2b$12$Tw1JBtsMpGaw732WhSPLmecBzSPy0bdkLBGz6kPupMSnBK1hPt4/a",  # şifre: 123
        is_admin=False  # Normal kullanıcı
    )
}