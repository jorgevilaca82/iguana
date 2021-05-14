enable_local_settings:
	export DJANGO_SETTINGS_MODULE="local_settings"

local_settings:
	echo "from sgi.settings import *" > local_settings.py
	enable_local_settings

configure_locale:
	locale-gen pt_BR.UTF-8
	dpkg-reconfigure locales
	update-locale LANG=pt_BR.UTF-8 LC_ALL=pt_BR.UTF-8 LANGUAGE=pt_BR.UTF-8