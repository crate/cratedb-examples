# Disable telemetry using Scarf.
# https://about.scarf.sh/
# https://github.com/apache/superset/issues/25639
ENABLE_TELEMETRY = False

# Superset specific config
ROW_LIMIT = 5000

# Flask App Builder configuration
# Your App secret key will be used for securely signing the session cookie
# and encrypting sensitive information on the database
# Make sure you are changing this key for your deployment with a strong key.
# Alternatively you can set it with `SUPERSET_SECRET_KEY` environment variable.
# You MUST set this for production environments or the server will not refuse
# to start and you will see an error in the logs accordingly.
SECRET_KEY = 'VcKzHS4g2h+dP33tCbqOghtKaU37wvFECMhVqrfccaoI/17qh/j3+VDV'

# Configure JWT subsystem to not enforce that the sub claim is a string.
# https://github.com/crate/cratedb-examples/issues/741
# https://github.com/apache/superset/issues/30995
# https://github.com/dpgaspar/Flask-AppBuilder/issues/2287
JWT_VERIFY_SUB = False

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).
# Note that the connection information to connect to the datasources
# you want to explore are managed directly in the web UI
# The check_same_thread=false property ensures the sqlite client does not attempt
# to enforce single-threaded access, which may be problematic in some edge cases
# When not configured, the default location is `~/.superset/superset.db`.
# See also https://superset.apache.org/docs/installation/configuring-superset/.
# SQLALCHEMY_DATABASE_URI = 'sqlite:////path/to/superset.db?check_same_thread=false'

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = False
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = ''
