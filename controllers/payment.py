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
    def migo_return(self, **post):
        """ Migo """
        _logger.info('Migo: entering form_feedback with post data %s', pprint.pformat(post))  # debug
        request.env['payment.transaction'].sudo().form_feedback(post, 'migo')
        _logger.warn(post)

        return werkzeug.utils.redirect("/payment/process")