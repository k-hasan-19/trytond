#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

import encodings.idna
import urllib
import socket

from trytond.config import CONFIG
from trytond.transaction import Transaction


class URLMixin(object):

    def get_url(self):
        from trytond.model import Model
        from trytond.wizard import Wizard
        from trytond.report import Report
        url_part = {}

        hostname = CONFIG['hostname'] or unicode(socket.getfqdn(), 'utf8')
        url_part['hostname'] = '.'.join(encodings.idna.ToASCII(part) for part in
            hostname.split('.'))
        url_part['port'] = CONFIG['netport']

        if isinstance(self, Model):
            url_part['type'] = 'model'
        elif isinstance(self, Wizard):
            url_part['type'] = 'wizard'
        elif isinstance(self, Report):
            url_part['type'] = 'report'
        else:
            raise NotImplementedError

        url_part['name'] = self._name
        url_part['database'] = Transaction().cursor.database_name

        host_part = '%(hostname)s:%(port)s' % url_part
        local_part = urllib.quote('%(database)s/%(type)s/%(name)s' % url_part)
        return 'tryton://%s/%s' % (host_part, local_part)