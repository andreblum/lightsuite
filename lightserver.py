from flask import Flask, make_response
from klikaanklikuit import KlikAanKlikUit
app = Flask(__name__)

k = KlikAanKlikUit(0b01011011000111101001110010)

@app.route('/light/<name>/<on>')
def index(name, on):
    print 'got name %s on %s' % (name, on)
    if name == 'window':
        if on == 'on':
            k.lampOn(k.VENSTERBANK)
        else:
            k.lampOff(k.VENSTERBANK)
    elif name == 'piano':
        if on == 'on':
            k.lampOn(k.SCHEMERLAMP)
        else:
            k.lampOff(k.SCHEMERLAMP)
    elif name == 'corner':
        if on == 'on':
            k.lampOn(k.HOEKLAMP)
        else:
            k.lampOff(k.HOEKLAMP)

    return make_response()


if __name__ == "__main__":
    app.run(debug=True, host="10.0.1.35", port=8080)
