from seleniumrequests import Firefox
import os
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parents[0]
print(BASE_DIR)
browser = Firefox(executable_path=os.path.join(BASE_DIR, 'geckodriver.exe'))
browser.get('http://127.0.0.1:8000/')

assert 'Вход в систему' in browser.title
