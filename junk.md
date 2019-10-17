# col-xl-12 col-lg-12 col-md-12 col-sm-12 col-12
# request.META.get('HTTP_REFERER', '/')
# Type
        - type + priority_filtered          (priority)
        - type + status_filtered            (donation_progress__progress_status)
        - type + donate_type_filtered       (donate_type)
        - type + is_verified_filtered       (is_verified)

# Priority
        - priority + type_filtered              (type)
        - priority + status_filtered            (donation_progress__progress_status)
        - priority + donate_type_filtered       (donate_type)
        - priority + is_verified_filtered       (is_verified)

# Status
        - status + type_filtered              (type)
        - status + priority_filtered          (priority)
        - status + donate_type_filtered       (donate_type)
        - status + is_verified_filtered       (is_verified)

# Donate Type
        - donate_type + type_filtered               (type)
        - donate_type + priority_filtered           (priority)
        - donate_type + status_filtered             (donation_progress__progress_status)
        - donate_type + is_verified_filtered        (is_verified)

# Is Verified
    - is_verified + type_filtered               (type)
    - is_verified + priority_filtered           (priority)
    - is_verified + status_filtered             (donation_progress__progress_status)
    - is_verified + donate_type_filtered        (donate_type)



###
 is_verified + donate_type + status + priority