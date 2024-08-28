from hashlib import sha1

def compute_hash(email):
	return sha1(email.encode('utf-8')).hexdigest()

def compute_certificate_id(email):
	email_clean = email.lower().strip()
	return compute_hash(email_clean + '_')


cohort = 2024
course = 'mlops-zoomcamp'
my_id = compute_certificate_id('ndirangumuturi749@gmail.com')
url = f"https://certificate.datatalks.club/{course}/{cohort}/{my_id}.pdf"

print('url:', url)
print("my id:", my_id)
