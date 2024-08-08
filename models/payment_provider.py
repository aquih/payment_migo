# coding: utf-8
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class AcquirerMigo(models.Model):
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
