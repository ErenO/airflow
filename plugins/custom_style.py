"""Custom Airflow plugin to inject CSS for white navbar text."""
from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint

# Create blueprint
custom_style_bp = Blueprint(
    'custom_style',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/custom_style'
)


class CustomStylePlugin(AirflowPlugin):
    name = 'custom_style'
    flask_blueprints = [custom_style_bp]
    appbuilder_views = []
    appbuilder_menu_items = []
