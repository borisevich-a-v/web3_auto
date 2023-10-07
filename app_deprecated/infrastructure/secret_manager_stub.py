class SecretManagerStub:
    def __init__(self, public_key, private_key):
        self.key_value_pair = {public_key: private_key}

    def get_secret_value(self, *args, **kwargs):
        return self.key_value_pair
