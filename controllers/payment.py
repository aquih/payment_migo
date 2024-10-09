# -*- coding: utf-8 -*-

import logging
import pprint
import werkzeug
from werkzeug.wrappers import Response

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class MigoController(http.Controller):
    _return_url = '/payment/migo/return'

    @http.route(['/payment/migo/return'], type='http', auth='public', csrf=False, save_session=False)
    def migo_return(self, **data):
        """ Process the data returned by Migo after redirection.

        :param dict data: The feedback data
        """
        if data:
            _logger.info('Migo: entering _handle_feedback_data with post data %s', pprint.pformat(data))  # debug
            tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data('migo', data)
            tx_sudo._handle_notification_data('migo', data)

        return request.redirect('/payment/status')
