"""Airflow webserver configuration."""
from flask_appbuilder.const import AUTH_DB

# Authentication type
AUTH_TYPE = AUTH_DB

# Custom CSS injection for white navbar text
CUSTOM_CSS = """
<style>
/* Force white text in navbar */
nav.navbar a,
nav.navbar span,
nav.navbar .nav-link,
nav.navbar .navbar-brand,
.navbar-nav a,
.navbar-nav span,
[data-testid="navbar"] a,
header a,
.ant-menu a,
.ant-menu-item,
.ant-menu-title-content {
    color: #ffffff !important;
}
nav.navbar a:hover,
.navbar-nav a:hover {
    color: #e0e0e0 !important;
}
/* Dropdown menus */
.dropdown-toggle,
.nav-item.dropdown a {
    color: #ffffff !important;
}
</style>
"""

# Inject into page
try:
    from airflow.configuration import conf
    conf.set("webserver", "extra_head_content", CUSTOM_CSS)
except:
    pass
