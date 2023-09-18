import requests
from flask import Flask, render_template
import colorama
from colorama import Fore, Style

app = Flask(__name__)
colorama.init(autoreset=True)

def read_domains_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    categories = {}
    current_category = None
    for line in lines:
        line = line.strip()
        if line:
            if not line.startswith("#"):
                if line.isupper():
                    current_category = line
                    categories[current_category] = []
                else:
                    categories[current_category].append(line)
    return categories

def check_ssl_certificate(domain):
    try:
        response = requests.get(f"https://{domain}", timeout=3)
        response.raise_for_status()
        return True  # True indicates valid SSL/TLS
    except requests.exceptions.SSLError as e:
        return False  # False indicates SSL/TLS certificate error
    except requests.exceptions.RequestException as e:
        return False  # False indicates other error

@app.route('/')
def index():
    domains_by_category = read_domains_from_file('domains.txt')

    results = {}  # Store the results in a dictionary

    for category, domains in domains_by_category.items():
        category_results = {}
        for domain in domains:
            status = check_ssl_certificate(domain)
            category_results[domain] = status
        results[category] = category_results

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
