from odoo import http, fields
from odoo.http import request

class PriceCheckerController(http.Controller):

    @http.route('/price', type='http', auth='public', csrf=False)
    def price_checker(self, **kwargs):
        barcode = kwargs.get('barcode')
        product = None
        price_usd = None
        price_lbp = None

        if barcode:
            product = request.env['product.product'].sudo().search([('barcode', '=', barcode)], limit=1)

            if product:
                company = request.env.company
                base_currency = company.currency_id
                today = fields.Date.today()

                usd_currency = request.env['res.currency'].sudo().search([('name', '=', 'USD')], limit=1)
                lbp_currency = request.env['res.currency'].sudo().search([('name', '=', 'LBP')], limit=1)

                price = product.lst_price

                # Convert from base to USD
                if usd_currency:
                    price_usd = base_currency._convert(price, usd_currency, company, today)

                # Convert from base to LBP
                if lbp_currency:
                    price_lbp = base_currency._convert(price, lbp_currency, company, today)

        return request.render('standalone_pricechecker.price_checker_template', {
            'product': product,
            'barcode': barcode or "",
            'price_usd': round(price_usd, 2) if price_usd else None,
            'price_lbp': round(price_lbp, 2) if price_lbp else None,
        })
