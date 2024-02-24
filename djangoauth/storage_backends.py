# storage_backends.py

from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'bnr360'
    account_key = 'liHiHuaCaUOOA3SzQx7zPsMMdpjdnCLfBfw53Gz5rjrneIdIkxk2Tm9MhnZrqkl0ghdklOtDiyrw+AStTP6/eA=='
    azure_container = 'django'
    expiration_secs = None
