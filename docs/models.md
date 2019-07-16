=================== Choices Map =================

# User Gender Choices

    MALE        = 'M'
    FEMALE      = 'F'
    OTHERS      = 'O'

# Blood Group Choices

    A_POSITIVE  = 'A+'
    A_NEGATIVE  = 'A-'
    B_POSITIVE  = 'B+'
    B_NEGATIVE  = 'B-'
    O_POSITIVE  = 'O+'
    O_NEGATIVE  = 'O-'
    AB_POSITIVE  = 'AB+'
    AB_NEGATIVE  = 'AB-'

# Account Type Choices

    REGULAR     = 0
    PREMIUM     = 1


==================== Notification Utils ====================
# Respond to donation
    - category = 'donationRespond_Create'
    - identifier = slug (donation)
    - subject = f"{respondent} has responded to your donation post"

================== Models =================

# User

    - username          (CharField)
    - first_name        (CharField)
    - last_name         (CharField)
    - email             (EmailField)
    - password          (CharField)
    - groups            (ManyToManyField)       to - Group
    - user_permissions  (ManyToManyField)       to - Permission
    - is_staff          (BooleanField)
    - is_active         (BooleanField)
    - is_superuser      (BooleanField)
    - last_login        (DateTimeField)
    - date_joined       (DateTimeField)

# Profile

    - user              (OneToOneField)         to - User (profile)
    - slug              (SlugField)
    - gender            (CharField)
    - dob               (DateField)
    - blood_group       (CharField)
    - contact           (CharField)
    - address           (TextField)
    - about             (TextField)
    - facebook          (URLField)
    - linkedin          (URLField)
    - website           (URLField)
    - image             (ImageField)
    - account_type      (PositiveSmallIntegerField)
    - is_volunteer      (BooleanField)
    - created_at        (DateTimeField)
    - updated_at        (DateTimeField)
