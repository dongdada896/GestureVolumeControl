import os
login = os.environ['OC_LOGIN']
password = os.environ['OC_PASSWD']
email = os.environ['OC_EMAIL']
name = os.environ['OC_NAME']
surname = os.environ['OC_SURNAME']

address = os.environ['OC_ADDRESS']

additional_login = os.environ['OC_ADDITIONAL_LOGIN']
additional_password = os.environ['OC_ADDITIONAL_PASSWD']
additional_email = os.environ['OC_ADDITIONAL_EMAIL']
additional_name = os.environ['OC_ADDITIONAL_NAME']
additional_surname = os.environ['OC_ADDITIONAL_SURNAME']

admin_name = os.environ['OC_ADMIN_NAME']
admin_passwd = os.environ['OC_ADMIN_PASSWD']

# Space separated node addresses
nodes = os.environ['OC_NODES'].split(' ')

# Space separated storage addresses (with /storage export over nfs)
storages = os.environ['OC_STORAGES'].split(' ')