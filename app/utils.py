import bcrypt

def hash_password(password:str) -> str:
    # Step 1: Encode the attempted password and convert into password bytes
    pwd_byte = password.encode('utf-8')

    # Step 2: To make each passwords unique, we add salted password string into each password byte string to make it unique. So that even if multiple users share the same password, the salted string will make each like password unique
    salted_byte = bcrypt.gensalt()

    # Step 3: Hash the password
    hashed_password = bcrypt.hashpw(password=pwd_byte,salt=salted_byte)

    # Step 4: Decode the hashed password and return it
    return hashed_password.decode('utf-8')



def verify_password(attempted_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(attempted_password.encode('utf-8'), hashed_password.encode('utf-8'))