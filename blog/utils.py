import os
# import random
# import string
import time
# from django.utils.text import slugify


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_blog_files_path(instance, filename):
    new_filename = "{title}_{datetime}".format(
        title=instance.blog.title[:20],
        datetime=time.strftime("%Y%m%d-%H%M%S")
    )
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "Accounts/{user}/Blog/{title}/{final_filename}".format(
        user=instance.blog.user,
        title=instance.blog.title[:20],
        final_filename=final_filename
    )
