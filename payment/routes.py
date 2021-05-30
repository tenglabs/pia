from flask import render_template, request, redirect
from payment import app, db
from payment.models import CustomerPayment
from .piastrixlib import PiastrixClient
import logging

logging.basicConfig(level=logging.DEBUG)

secret_key = 'SecretKey01'
shop_id = '5'


@app.route("/", methods=['POST', 'GET'])
def home():
    get_check = request.args.get('currency')
    piastrix = PiastrixClient(shop_id, secret_key)

    if get_check == 'USD':
        if request.method == 'POST':

            shop_amount = request.form.get('amount')
            payer_currency = '840'
            shop_currency = '840'

            shop_order_id = '101'  # можно генерировать на основе id обьекта если сначала создавать модель
            description = request.form.get('description')
            extra_fields = {

                            'description': description,
                            'payer_account': request.form.get('account')

                            }

            response = piastrix.bill(payer_currency, shop_amount, shop_currency, shop_order_id, extra_fields)
            app.logger.info(response)
            url = response['url']
            api_id = response['id']

            payment = CustomerPayment(
                                      amount=shop_amount,
                                      currency=shop_currency,
                                      description=description,
                                      api_id=api_id

                                      )
            db.session.add(payment)
            db.session.commit()

            return redirect(url)

    if get_check == 'EUR':
        if request.method == 'POST':

            amount = request.form.get('amount')
            currency = '978'
            shop_order_id = '101'
            description = request.form.get('description')

            data = piastrix.pay(amount, currency, shop_order_id)
            app.logger.info(data)
            # можно в принципе самому формировать подпись,
            # но я решил что использовать библиотеку будет более целесообразно.
            sign = data[0]['sign']

            # Для получения payment_id нужно словить callback, и уже на его основе создавать обьект
            payment = CustomerPayment(amount=amount, currency=currency, description=description, sign=sign)
            db.session.add(payment)
            db.session.commit()

            # Лучше сделать через AJAX , но в рамках тестового задания сойдет.
            return render_template('form.html',

                                   sign=sign,

                                   amount=amount,

                                   currency=currency,

                                   shop_id=shop_id,

                                   shop_order_id=shop_order_id,

                                   description=description,

                                   )

    if get_check == 'RUB':
        if request.method == 'POST':
            amount = request.form.get('amount')
            currency = '643'
            payway = 'advcash_rub'
            shop_order_id = '101'
            description = request.form.get('description')
            extra_fields = {'description':description}
            response = piastrix.invoice(amount, currency, shop_order_id, payway, extra_fields)
            app.logger.info(response)

            ac_account_email = response['data']['ac_account_email']
            ac_sci_name = response['data']['ac_sci_name']
            ac_amount = response['data']['ac_amount']
            ac_currency = response['data']['ac_currency']
            ac_order_id = response['data']['ac_order_id']
            ac_sign = response['data']['ac_sign']


            payment = CustomerPayment(amount=amount, currency=currency, description=description, api_id=response['id'] )
            db.session.add(payment)
            db.session.commit()

            return render_template(
                                   'invoice.html',
                                   ac_account_email=ac_account_email,
                                   ac_sci_name=ac_sci_name,
                                   ac_amount=ac_amount,
                                   ac_currency=ac_currency,
                                   ac_order_id=ac_order_id,
                                   ac_sign=ac_sign


                                   )

    return render_template('home.html', get_check=get_check)


@app.route("/payments/list", methods=['POST', 'GET'])
def payment_list():
    payments = CustomerPayment.query.all()
    return render_template('list.html', payments=payments)


# Поскольку callback приходит только в случае успешной оплаты и отсутсвует тестовый режим,
# нет возможности отловить данные
# @app.route("/api/callback", methods=['POST', 'GET'])
# def callback():
    # print(request.form.keys()[0])
