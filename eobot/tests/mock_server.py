import json
import socket
from threading import Thread

try:
    # noinspection PyUnresolvedReferences
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

try:
    # noinspection PyUnresolvedReferences
    from http.server import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


mock_state = {
    "coins": {
        "BTC": {
            "Price": 100.0,
            "Image": "http://www.eobot.com/btc.png",
            "BigImage": "http://www.eobot.com/btcbig.png"
        },
        "ETH": {
            "Price": 20.0,
            "Image": "http://www.eobot.com/eth.png",
            "BigImage": "http://www.eobot.com/ethbig.png"
        }
    },
    "miners": {
        "GHS": {
            "Price": 0.5
        }
    },
    "fiat": {
        "USD": {
            "Price": 1.0
        },
        "EUR": {
            "Price": 0.85
        }
    },
    "accounts": {
        123: {
            "email": "123@example.com",
            "password": "password",
            "coins": {
                "BTC": 0.2,
                "ETH": 2.5
            },
            "miners": {
                "GHS": 10.0
            },
            "mode": "BTC",
            "speed": {
                "MiningSHA-256": 10.0
            },
            "wallets": {
                "BTC": "bitcoin-wallet",
                "ETH": "ethereum-wallet"
            }
        },
        456: {
            "email": "456@example.com",
            "password": "password",
            "coins": {
                "BTC": 0.1,
                "ETH": 2.0
            },
            "miners": {
                "GHS": 5.0
            },
            "mode": "ETH",
            "speed": {
                "MiningSHA-256": 5.0
            },
            "wallets": {
                "BTC": "wallet-bitcoin",
                "ETH": "wallet-ethereum"
            }
        }
    }
}


# noinspection PyTypeChecker,PyUnresolvedReferences
class MockServerRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, _format, *args):
        return

    # noinspection PyPep8Naming
    def do_GET(self):
        parameters = parse_qs(urlparse('http://localhost{0}'.format(self.path)).query)

        if "exchangefee" in parameters.keys():
            self.do_get_exchange_estimate(parameters)
        elif "total" in parameters.keys():
            self.do_get_balances(parameters)
        elif "coin" in parameters.keys():
            self.do_get_coin_value_or_exchange_rate(parameters)
        elif "deposit" in parameters.keys():
            self.do_get_deposit_address(parameters)
        elif "convertfrom" in parameters.keys():
            self.do_exchange_coins(parameters)
        elif "idmining" in parameters.keys():
            self.do_get_mining_mode(parameters)
        elif "idspeed" in parameters.keys():
            self.do_get_mining_speed(parameters)
        elif "idestimates" in parameters.keys():
            self.do_get_mining_estimates(parameters)
        elif "supportedcoins" in parameters.keys():
            self.do_get_supported_coins()
        elif "supportedfiat" in parameters.keys():
            self.do_get_supported_fiat()
        elif "manualwithdraw" in parameters.keys():
            self.do_manual_withdraw(parameters)
        elif "withdraw" in parameters.keys():
            self.do_set_automatic_withdraw()
        elif "mining" in parameters.keys():
            self.do_set_mining_mode(parameters)
        elif "email" in parameters.keys():
            self.do_get_user_id(parameters)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Page not found".encode())

    def do_exchange_coins(self, parameters):
        from_coin = parameters["convertfrom"]
        if isinstance(from_coin, list):
            from_coin = from_coin[0]

        amount = parameters["amount"]
        if isinstance(amount, list):
            amount = amount[0]
        amount = float(amount)

        to_coin = parameters["convertto"]
        if isinstance(to_coin, list):
            to_coin = to_coin[0]

        account_id = parameters["id"]
        if isinstance(account_id, list):
            account_id = int(account_id[0])

        add_amount = (amount * mock_state["coins"][from_coin]["Price"]) / mock_state["coins"][to_coin]["Price"]

        mock_state["accounts"][account_id]["coins"][from_coin] -= amount
        mock_state["accounts"][account_id]["coins"][to_coin] += add_amount

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps("OK").encode())

    def do_get_balances(self, parameters):
        account_id = parameters["total"]
        if isinstance(account_id, list):
            account_id = int(account_id[0])

        balances = dict(mock_state["accounts"][account_id]["coins"])

        total = 0.0
        for coin in balances.keys():
            total += balances[coin] * mock_state["coins"][coin]["Price"]

        balances["Total"] = total

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(balances).encode())

    def do_get_coin_value_or_exchange_rate(self, parameters):
        coin = parameters["coin"]
        if isinstance(coin, list):
            coin = coin[0]

        if coin in mock_state["coins"].keys():
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({coin: mock_state["coins"][coin]["Price"]}).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({coin: mock_state["fiat"][coin]["Price"]}).encode())

    def do_get_deposit_address(self, parameters):
        account_id = parameters["id"]
        if isinstance(account_id, list):
            account_id = int(account_id[0])

        coin = parameters["deposit"]
        if isinstance(coin, list):
            coin = str(coin[0])

        wallet = mock_state["accounts"][account_id]["wallets"][coin]

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({coin: wallet}).encode())

    def do_get_exchange_estimate(self, parameters):
        from_coin = parameters["convertfrom"]
        if isinstance(from_coin, list):
            from_coin = str(from_coin[0])

        to_coin = parameters["convertto"]
        if isinstance(to_coin, list):
            to_coin = str(to_coin[0])

        quantity = parameters["amount"]
        if isinstance(quantity, list):
            quantity = float(quantity[0])

        from_value = mock_state["coins"][from_coin]["Price"] \
            if from_coin in mock_state["coins"].keys() \
            else mock_state["miners"][from_coin]["Price"]

        to_value = mock_state["coins"][to_coin]["Price"] \
            if to_coin in mock_state["coins"].keys() \
            else mock_state["miners"][to_coin]["Price"]

        estimate = (float(quantity) * float(from_value)) / float(to_value)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"Result": estimate}).encode())

    def do_get_mining_mode(self, parameters):
        account_id = parameters["idmining"]
        if isinstance(account_id, list):
            account_id = int(account_id[0])

        mode = mock_state["accounts"][account_id]["mode"]

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"mining": mode}).encode())

    def do_get_mining_speed(self, parameters):
        account_id = parameters["idspeed"]
        if isinstance(account_id, list):
            account_id = int(account_id[0])

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(mock_state["accounts"][account_id]["speed"]).encode())

    def do_get_mining_estimates(self, parameters):
        account_id = parameters["idestimates"]
        if isinstance(account_id, list):
            account_id = int(account_id[0])

        speed = mock_state["accounts"][account_id]["speed"]["MiningSHA-256"]
        estimate = (speed * mock_state["miners"]["GHS"]["Price"]) / 30.0

        estimates = {
            "MiningSHA-256": estimate
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(estimates).encode())

    def do_get_supported_coins(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(mock_state["coins"]).encode())

    def do_get_supported_fiat(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(mock_state["fiat"]).encode())

    def do_manual_withdraw(self, parameters):
        coin = parameters["manualwithdraw"]
        if isinstance(coin, list):
            coin = coin[0]

        amount = parameters["amount"]
        if isinstance(amount, list):
            amount = amount[0]
        amount = float(amount)

        account_id = parameters["id"]
        if isinstance(account_id, list):
            account_id = int(account_id[0])

        mock_state["accounts"][account_id]["coins"][coin] -= amount

        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps("OK").encode())

    def do_set_automatic_withdraw(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps("OK").encode())

    def do_set_mining_mode(self, parameters):
        account_id = parameters["id"]
        if isinstance(account_id, list):
            account_id = int(account_id[0])

        mode = parameters["mining"]
        if isinstance(mode, list):
            mode = mode[0]

        mock_state["accounts"][account_id]["mode"] = mode

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps("OK").encode())

    def do_get_user_id(self, parameters):
        email = parameters["email"]
        if isinstance(email, list):
            email = email[0]

        password = parameters["password"]
        if isinstance(password, list):
            password = password[0]

        user_id = None

        for account_id in mock_state["accounts"].keys():
            if mock_state["accounts"][account_id]["email"] == email \
                    and mock_state["accounts"][account_id]["password"] == password:
                user_id = account_id
                break

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"userid": user_id}).encode())


# noinspection PyTypeChecker
class MockServer(object):
    def __init__(self):
        super(MockServer, self).__init__()
        self.port = 0
        self.thread = None
        self.server = None

    def get_free_port(self):
        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        address, port = s.getsockname()
        s.close()
        self.port = port

    def start(self):
        self.get_free_port()
        self.server = HTTPServer(('localhost', self.port), MockServerRequestHandler)

        self.thread = Thread(target=self.server.serve_forever)
        self.thread.setDaemon(True)
        self.thread.start()

        return True

    @staticmethod
    def reset():
        mock_state["accounts"][123]["coins"]["BTC"] = 0.2
        mock_state["accounts"][123]["coins"]["ETH"] = 2.5
        mock_state["accounts"][123]["miners"]["GHS"] = 10.0
        mock_state["accounts"][123]["mode"] = "BTC"

        mock_state["accounts"][456]["coins"]["BTC"] = 0.1
        mock_state["accounts"][456]["coins"]["ETH"] = 2.0
        mock_state["accounts"][456]["miners"]["GHS"] = 5.0
        mock_state["accounts"][456]["mode"] = "ETH"

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.server = None
        self.thread = None
        self.port = 0
