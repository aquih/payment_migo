# -*- coding: utf-8 -*-

import logging
import pprint
import werkzeug
from werkzeug.wrappers import Response

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class MigoController(http.Controller):
    _return_url = '/payment/migopayments/return'

    @http.route(['/payment/migopayments/return'], type='http', auth='public', csrf=False, save_session=False)
    def migo_return(self, **data):
        """ Migo """
        if data:
            _logger.info('Migo: entering form_feedback with post data %s', pprint.pformat(data))  # debug
            request.env['payment.transaction'].sudo().form_feedback(post, 'data')

        return request.redirect("/payment/process")
