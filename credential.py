class Credential:
    """Class to store the credential of a service"""
    default_kwargs = {
        "userid": "",   # empty string or None?
        "url": "",      # empty string or None?
        "alias": "",    # empty string or None?
    }

    def __init__(self, service, passwd, **kwargs):
        #TODO: attribute 'service' should be unique
        self.service = service
        self.passwd = passwd

        for key, val in self.default_kwargs.items():
            setattr(self, key, kwargs.get(key, val))

    def __repr__(self):
        string = f"{self.service} credentials"
        if self.userid:
            string += f" for the user '{self.userid}'"
        return string


if __name__ == "__main__":
    fb = Credential("Facebook", "p@55w0rd", userid="johnsmith", url="https://facebook.com")
    print(fb)

