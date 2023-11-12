import os 
from werkzeug.security import check_password_hash, generate_password_hash

passw = "abc123"

a = (generate_password_hash(passw))

print(a)

print(check_password_hash(a, passw))