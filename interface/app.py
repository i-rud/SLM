from interface import Interface

_interface = Interface()

def run():
    auth = _interface.login()
    if auth:
        _interface.run()
    else:
        return

if __name__ == "__main__":
    run()
