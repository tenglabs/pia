from piastrixlib import PiastrixClient

secret_key = 'SecretKey01'
shop_id = '5'

piastrix = PiastrixClient(shop_id, secret_key)

shop_amount = '1'
payer_currency = '840'
shop_currency = '840'

shop_order_id = '101'

extra_fields = {'description': 'Test description',
                'callback_url': 'https://webhook.site/7f382344-69fc-4e65-9bad-e4b57569766f',
                'payer_account': 'antypenkodev@gmail.com'}



response = piastrix.bill(payer_currency, shop_amount, shop_currency, shop_order_id, extra_fields)

print(response)