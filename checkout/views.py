from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe
from django.contrib import messages
from checkout.models import Checkout
from priceplan.models import Plan
from accounts.models import  UserProfile
from django.core.mail import EmailMultiAlternatives
import datetime
from dateutil.relativedelta import relativedelta
from django.http import HttpResponseRedirect
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request, slug):
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    # print(request.user.userstripe.stripe_id)
    customer_id = request.user.userstripe.stripe_id
    if request.method == 'POST':
        plan_qs = Plan.objects.filter(slug=slug)
        if plan_qs.exists():
            selected_plan = plan_qs.first()
            token = request.POST['stripeToken']
            amount = selected_plan.amount
            currency = selected_plan.currency
            description = selected_plan.description
            # Creating Charge from user's card
            try:
                customer = stripe.Customer.retrieve(customer_id)
                customer.sources.create(source=token)
                charge = stripe.Charge.create(
                    amount=amount * 100,
                    currency=currency,
                    description=description,
                    customer=customer,
                )
                # print(charge.amount)
                # Create Checkout object
                # instance = Checkout.objects.create(user=request.user, plan=selected_plan)
                instance = Checkout.objects.create(
                    user=request.user, plan=selected_plan, created_at=datetime.datetime.now())
                profile_qs = UserProfile.objects.filter(user=request.user)
                if profile_qs.exists():
                    profile_qs.update(account_type=1)
                expiration_date = (
                    instance.created_at + relativedelta(months=selected_plan.expiration_cycle)).strftime("%d-%m-%Y")
                # Sending Email
                mail_msg = f"Hello {request.user.profile.get_username()} ! <br> You have successfully subscribed to BDonor for {selected_plan.expiration_cycle} month. Your subscription will expire after {expiration_date} <br> Have a good day. <br>Thanks for being with us."
                mail_subject = f'BDonor Subscription'
                mail_from = 'admin@bdonor.com'
                mail_text = 'Please do not Reply'
                subject = mail_subject
                from_email = mail_from
                to = [request.user.email]
                text_content = mail_text
                html_content = mail_msg
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.add_message(request, messages.SUCCESS,
                                    f"Your payment has been made successfully! {amount} {currency} has been charged. You are now a premium user of BDonor. Your subscription will expire after {expiration_date}.")
                return HttpResponseRedirect(reverse('home'))
            except stripe.error.CardError as e:
                pass
        else:
            messages.add_message(request, messages.WARNING,
                                "Price plan doesn't exists!")
    # Starts Base Template Context
    if request.user.is_superuser:
        base_template = 'admin-site/base.html'
    else:
        base_template = 'base.html'
    # Ends Base Template Context
    context = {
        'publishKey': publishKey,
        'base_template': base_template
    }
    template = 'checkout/checkout.html'
    return render(request, template, context)
