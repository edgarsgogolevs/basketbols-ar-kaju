from waitress import serve
import flaskapp
from os import environ

serve(flaskapp.app, host='0.0.0.0', port=environ.get('PORT'))
