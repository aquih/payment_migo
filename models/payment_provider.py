# coding: utf-8
import logging

from odoo import api, fields, models, _

from odoo.addons.payment_migo import const

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('migo', 'Migo')], ondelete={'migo': 'set default'})
    migo_token = fields.Char('Token', required_if_provider='migo', groups='base.group_user')
    migo_client = fields.Char('Client', required_if_provider='migo', groups='base.group_user')
    
    def _migo_get_api_url(self):
        self.ensure_one()
        if self.state == 'enabled':
            return 'https://web.migopayments.com/'
        else:
            return 'https://sandbox.migopayments.com/'

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'migo':
            return default_codes
        return const.DEFAULT_PAYMENT_METHODS_CODES