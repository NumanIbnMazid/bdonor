import os
import random
import string
import time
from django.utils.text import slugify


'''
random_string_generator is located here:
http://joincfe.com/blog/random-string-generator-in-python/
'''
# from yourapp.utils import random_string_generator

# def get_adapter(request=None):
#     return import_attribute(app_settings.ADAPTER)(request)


def random_string_generator(size=4, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_number_generator(size=4, chars='1234567890'):
    return ''.join(random.choice(chars) for _ in range(size))


def time_str_mix_slug():
    timestamp_m = time.strftime("%Y")
    timestamp_d = time.strftime("%m")
    timestamp_y = time.strftime("%d")
    timestamp_now = time.strftime("%H%M%S")
    random_str = random_string_generator()
    random_num = random_number_generator()
    bindings = (
        random_str + timestamp_d + random_num + timestamp_now +
        timestamp_y + random_num + timestamp_m
    )
    return bindings
# print(random_string_generator())

# print(random_string_generator(size=50))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_slug_generator_custom(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a subject character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.subject)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
