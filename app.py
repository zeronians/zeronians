import requests
from flask import Flask, render_template
import colorama
from colorama import Fore, Style

app = Flask(__name__)
colorama.init(autoreset=True)

def check_ssl_certificate(domain):
    try:
        response = requests.get(f"https://{domain}", timeout=5)
        response.raise_for_status()
        return True  # True indicates valid SSL/TLS
    except requests.exceptions.SSLError as e:
        return False  # False indicates SSL/TLS certificate error
    except requests.exceptions.RequestException as e:
        return False  # False indicates other error

@app.route('/')
def index():
    domains_to_check = ["wearedrome.com"]

    results = {}  # Store the results in a dictionary

    for domain in domains_to_check:
        status = check_ssl_certificate(domain)
        results[domain] = status

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
