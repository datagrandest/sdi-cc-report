import sys, os
import bottle

from sdi_cc_report.sdi_cc_report_web import run

# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))

application = run('wsgi')

