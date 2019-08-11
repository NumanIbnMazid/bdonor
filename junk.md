{% extends base_template %}

{% load static %}

{% block head_title %}{% block page_title %}{% block breadcrumb %}
Checkout
{% endblock %}{% endblock %}{% endblock %}

{% block content %}

<!-- Example card Information:
Card Number: 4242424242424242
Expiration: 01/19
CVC: 123 -->

<div class="row">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <div class="card-title text-center">Checkout</div>
            </div>
            <div class="card-body">
                <div class="text-center">
                    <small class="text-muted">
                        Please fill the <span class="text-info"><i>required</i></span> fields properly
                    </small>
                </div>
                <form action="" method="POST" id="payment-form" class="form">
                    {% csrf_token %}

                    <div class="text-center">
                        <span class="payment-errors text-danger font-15 font-bold"></span>
                    </div>

                    <div class="form-group">
                        <label for="card-number">
                            Card Number
                            <small class="text-info"><i class="field_priority">(required)</i></small>
                        </label>
                        <input type="text" class="form-control" id="card_number" maxlength="16" size="20"
                            data-stripe="number" placeholder="">
                        <small id="cardHelp" class="form-text text-muted text-center">
                            ex: 4242424242424242
                        </small>
                    </div>
                    <div class="form-group">
                        <label>
                            <span>
                                Expiration (MM/YY)
                                <small class="text-info"><i class="field_priority">(required)</i></small>
                            </span>
                        </label>
                        <div>
                            <input type="text" size="4" data-stripe="exp_month" maxlength="2" placeholder="MM"
                                id="exp_month">
                            <span> / </span>
                            <input type="text" size="4" data-stripe="exp_year" maxlength="2" placeholder="YY"
                                id="exp_year">
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="expiration-date">
                            CVC
                            <small class="text-info"><i class="field_priority">(required)</i></small>
                        </label>
                        <input type="text" size="4" data-stripe="CVC" class="form-control" maxlength="3" id="cvc">
                    </div>
                    <button type="submit" class="btn btn-success m-2" id="submitBtn">
                        Make Payment
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>

{% endblock %}

{% block extra_js %}
<!-- stripe version 2 js -->
<script type="text/javascript" src="https://js.stripe.com/v2/"></script>
{% comment %}
<!-- https://js.stripe.com/v2/ -->
<script type="text/javascript" src="{% static 'vendor/stripe/stripe-v2.js' %}"></script>
{% endcomment %}

<script type="text/javascript">
    Stripe.setPublishableKey('{{publishKey}}');

    function stripeResponseHandler(status, response) {
        var $form = $('#payment-form');
        if (response.error) {
            //$form.find('.payment-errors').text(response.error.message);
            $form.find('.submit').prop('disabled', false);
            //== Class definition
            var SweetAlertMessages = function () {
                var initDemos = function () {
                    //== Sweetalert Demo 4
                    $(document).ready(function (e) {
                        swal({
                            title: "ERROR!",
                            text: response.error.message,
                            icon: "error",
                            buttons: {
                                confirm: {
                                    text: "OK",
                                    value: true,
                                    visible: true,
                                    className: "btn btn-success",
                                    closeModal: true
                                },
                            }
                        });
                    });
                };
                return {
                    //== Init
                    init: function () {
                        initDemos();
                    },
                };
            }();
            //== Class Initialization
            jQuery(document).ready(function () {
                SweetAlertMessages.init();
            });
            
        } else {
            var token = response.id;

            $form.append($('<input type="hidden" name="stripeToken">').val(token));

            $form.get(0).submit();
        }
    };
</script>

<script type="text/javascript">
    $(function () {
        var $form = $('#payment-form');
        $form.submit(function (event) {
            // Disable the submit button to prevent repeated clicks;
            $form.find('.submit').prop('disabled', true);

            // Request a token  from stripe:
            Stripe.card.createToken($form, stripeResponseHandler);

            // Prevent the form from being submitted;
            return false;
        });
    });
</script>

<script type="text/javascript" src="{% static 'assets/js/form-validator/checkout-form.js' %}"></script>

{% endblock %}