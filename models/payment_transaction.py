# coding: utf-8
import logging

from werkzeug import urls

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from odoo.addons.payment_migo.controllers.payment import MigoController

import requests

_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    
    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider != 'visanet':
            return res
        
        data = {
            'amount': values['amount'],
            'userId': values['reference'],
            'channel': 'web',
            'client': self.migo_client,
            'createdBy': 'Odoo',
            'ads': [],
        }
        _logger.warning(data)

        uid_url = 'https://sb-mw.migopayments.com/transactions'
        if ( self.provider_id.state == 'enabled' ):
            uid_url = 'https://mw.migopayments.com/transactions'
        
        r = requests.post(uid_url, json=data, headers={'Authorization': self.migo_token})
        resultado = r.json()
        _logger.warning(resultado)
        
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        rendering_values = {
            'return_url': urllib.parse.urljoin(base_url, MigoController._return_url),
            'migo_order_id': resultado['uid'],
        }

        tx = self.env['payment.transaction'].sudo().search([('reference', '=', values['reference'])])
        tx.migo_uid = resultado['uid']
        
        return rendering_values

    @api.model
    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'migo':
            return tx

        reference = notification_data.get('uid')
        if not reference:
            error_msg = _('Migo: received data with missing reference (%s)') % (reference)
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        tx = self.search([('migo_uid', '=', reference), ('provider_code', '=', 'migo')])
        _logger.info(tx)

        if not tx or len(tx) > 1:
            error_msg = _('Migo: received data for reference %s') % (reference)
            if not tx:
                error_msg += _('; no order found')
            else:
                error_msg += _('; multiple order found')
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'migo':
            return

        self.provider_reference = notification_data.get('uid')

        status_code = notification_data.get('status', 'denied')
        if status_code == 'approved':
            self._set_done()
        else:
            error = 'Migo: error '+status_code
            _logger.info(error)
            self._set_error(_("Your payment was refused (code %s). Please try again.", status_code))
