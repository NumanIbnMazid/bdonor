# Raw

# Overall
context['total_donation'] = Donation.objects.filter().offers()
context['total_donation_request'] = Donation.objects.filter().requests()
context['total_donation_pending'] = Donation.objects.filter(
).is_pending().offers()
context['total_donation_request_pending'] = Donation.objects.filter(
).is_pending().requests()
context['total_donation_successful'] = Donation.objects.filter(
).is_done().offers()
context['total_donation_request_successful'] = Donation.objects.filter(
).is_done().offers()
# Blood Group Wise Donation Offers
context['donation_a_pos'] = Donation.objects.filter(
    blood_group__iexact="A+").offers()
context['donation_a_neg'] = Donation.objects.filter(
    blood_group__iexact="A-").offers()
context['donation_b_pos'] = Donation.objects.filter(
    blood_group__iexact="B+").offers()
context['donation_b_neg'] = Donation.objects.filter(
    blood_group__iexact="B-").offers()
context['donation_ab_pos'] = Donation.objects.filter(
    blood_group__iexact="AB+").offers()
context['donation_ab_neg'] = Donation.objects.filter(
    blood_group__iexact="AB-").offers()
context['donation_o_pos'] = Donation.objects.filter(
    blood_group__iexact="O+").offers()
context['donation_o_neg'] = Donation.objects.filter(
    blood_group__iexact="O-").offers()
# Blood Group Wise Donation Requests
context['donation_request_a_pos'] = Donation.objects.filter(
    blood_group__iexact="A+").requests()
context['donation_request_a_neg'] = Donation.objects.filter(
    blood_group__iexact="A-").requests()
context['donation_request_b_pos'] = Donation.objects.filter(
    blood_group__iexact="B+").requests()
context['donation_request_b_neg'] = Donation.objects.filter(
    blood_group__iexact="B-").requests()
context['donation_request_ab_pos'] = Donation.objects.filter(
    blood_group__iexact="AB+").requests()
context['donation_request_ab_neg'] = Donation.objects.filter(
    blood_group__iexact="AB-").requests()
context['donation_request_o_pos'] = Donation.objects.filter(
    blood_group__iexact="O+").requests()
context['donation_request_o_neg'] = Donation.objects.filter(
    blood_group__iexact="O-").requests()
# Donation Type
context['donation_blood'] = Donation.objects.filter(
).blood_type().offers()
context['donation_organ'] = Donation.objects.filter(
).organ_type().offers()
context['donation_tissue'] = Donation.objects.filter(
).tissue_type().offers()
context['donation_request_blood'] = Donation.objects.filter(
).blood_type().requests()
context['donation_request_organ'] = Donation.objects.filter(
).organ_type().requests()
context['donation_request_tissue'] = Donation.objects.filter(
).tissue_type().requests()
# Blood Donation Offers
context['blood_donation_a_pos'] = Donation.objects.filter(
    blood_group__iexact="A+").blood_type().offers()
context['blood_donation_a_neg'] = Donation.objects.filter(
    blood_group__iexact="A-").blood_type().offers()
context['blood_donation_b_pos'] = Donation.objects.filter(
    blood_group__iexact="B+").blood_type().offers()
context['blood_donation_b_neg'] = Donation.objects.filter(
    blood_group__iexact="B-").blood_type().offers()
context['blood_donation_ab_pos'] = Donation.objects.filter(
    blood_group__iexact="AB+").blood_type().offers()
context['blood_donation_ab_neg'] = Donation.objects.filter(
    blood_group__iexact="AB-").blood_type().offers()
context['blood_donation_o_pos'] = Donation.objects.filter(
    blood_group__iexact="O+").blood_type().offers()
context['blood_donation_o_neg'] = Donation.objects.filter(
    blood_group__iexact="O-").blood_type().offers()
# Blood Donation Requests
context['blood_donation_request_a_pos'] = Donation.objects.filter(
    blood_group__iexact="A+").blood_type().requests()
context['blood_donation_request_a_neg'] = Donation.objects.filter(
    blood_group__iexact="A-").blood_type().requests()
context['blood_donation_request_b_pos'] = Donation.objects.filter(
    blood_group__iexact="B+").blood_type().requests()
context['blood_donation_request_b_neg'] = Donation.objects.filter(
    blood_group__iexact="B-").blood_type().requests()
context['blood_donation_request_ab_pos'] = Donation.objects.filter(
    blood_group__iexact="AB+").blood_type().requests()
context['blood_donation_request_ab_neg'] = Donation.objects.filter(
    blood_group__iexact="AB-").blood_type().requests()
context['blood_donation_request_o_pos'] = Donation.objects.filter(
    blood_group__iexact="O+").blood_type().requests()
context['blood_donation_request_o_neg'] = Donation.objects.filter(
    blood_group__iexact="O-").blood_type().requests()
# Organ Donation Offers
context['organ_donation_heart'] = Donation.objects.filter(
    organ_name__iexact="Heart").organ_type().offers()
context['organ_donation_kidney'] = Donation.objects.filter(
    organ_name__iexact="Kidney").organ_type().offers()
context['organ_donation_pancreas'] = Donation.objects.filter(
    organ_name__iexact="Pancreas").organ_type().offers()
context['organ_donation_lungs'] = Donation.objects.filter(
    organ_name__iexact="Lungs").organ_type().offers()
context['organ_donation_liver'] = Donation.objects.filter(
    organ_name__iexact="Liver").organ_type().offers()
context['organ_donation_intestines'] = Donation.objects.filter(
    organ_name__iexact="Intestines").organ_type().offers()
# Organ Donation Requests
context['organ_donation_request_heart'] = Donation.objects.filter(
    organ_name__iexact="Heart").organ_type().requests()
context['organ_donation_request_kidney'] = Donation.objects.filter(
    organ_name__iexact="Kidney").organ_type().requests()
context['organ_donation_request_pancreas'] = Donation.objects.filter(
    organ_name__iexact="Pancreas").organ_type().requests()
context['organ_donation_request_lungs'] = Donation.objects.filter(
    organ_name__iexact="Lungs").organ_type().requests()
context['organ_donation_request_liver'] = Donation.objects.filter(
    organ_name__iexact="Liver").organ_type().requests()
context['organ_donation_request_intestines'] = Donation.objects.filter(
    organ_name__iexact="Intestines").organ_type().requests()
# Tissue Donation Offers
context['tissue_donation_bones'] = Donation.objects.filter(
    tissue_name__iexact="Bones'").tissue_type().offers()
context['tissue_donation_ligaments'] = Donation.objects.filter(
    tissue_name__iexact="Ligaments").tissue_type().offers()
context['tissue_donation_tendons'] = Donation.objects.filter(
    tissue_name__iexact="Tendons").tissue_type().offers()
context['tissue_donation_fascia'] = Donation.objects.filter(
    tissue_name__iexact="Fascia").tissue_type().offers()
context['tissue_donation_veins'] = Donation.objects.filter(
    tissue_name__iexact="Veins").tissue_type().offers()
context['tissue_donation_nerves'] = Donation.objects.filter(
    tissue_name__iexact="Nerves").tissue_type().offers()
context['tissue_donation_corneas'] = Donation.objects.filter(
    tissue_name__iexact="Corneas").tissue_type().offers()
context['tissue_donation_sclera'] = Donation.objects.filter(
    tissue_name__iexact="Sclera").tissue_type().offers()
context['tissue_donation_heart_valves'] = Donation.objects.filter(
    tissue_name__iexact="Heart Valves").tissue_type().offers()
context['tissue_donation_skin'] = Donation.objects.filter(
    tissue_name__iexact="Skin").tissue_type().offers()
# Tissue Donation Requests
context['tissue_donation_request_bones'] = Donation.objects.filter(
    tissue_name__iexact="Bones'").tissue_type().requests()
context['tissue_donation_request_ligaments'] = Donation.objects.filter(
    tissue_name__iexact="Ligaments").tissue_type().requests()
context['tissue_donation_request_tendons'] = Donation.objects.filter(
    tissue_name__iexact="Tendons").tissue_type().requests()
context['tissue_donation_request_fascia'] = Donation.objects.filter(
    tissue_name__iexact="Fascia").tissue_type().requests()
context['tissue_donation_request_veins'] = Donation.objects.filter(
    tissue_name__iexact="Veins").tissue_type().requests()
context['tissue_donation_request_nerves'] = Donation.objects.filter(
    tissue_name__iexact="Nerves").tissue_type().requests()
context['tissue_donation_request_corneas'] = Donation.objects.filter(
    tissue_name__iexact="Corneas").tissue_type().requests()
context['tissue_donation_request_sclera'] = Donation.objects.filter(
    tissue_name__iexact="Sclera").tissue_type().requests()
context['tissue_donation_request_heart_valves'] = Donation.objects.filter(
    tissue_name__iexact="Heart Valves").tissue_type().requests()
context['tissue_donation_request_skin'] = Donation.objects.filter(
    tissue_name__iexact="Skin").tissue_type().requests()




































# Query + Date From + Date To

# Overall
context['total_donation'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().offers()
context['total_donation_request'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().requests()
context['total_donation_pending'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
).is_pending().offers()
context['total_donation_request_pending'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
).is_pending().requests()
context['total_donation_successful'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
).is_done().offers()
context['total_donation_request_successful'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
).is_done().offers()
# Blood Group Wise Donation Offers
context['donation_a_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="A+").offers()
context['donation_a_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="A-").offers()
context['donation_b_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="B+").offers()
context['donation_b_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="B-").offers()
context['donation_ab_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="AB+").offers()
context['donation_ab_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="AB-").offers()
context['donation_o_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="O+").offers()
context['donation_o_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="O-").offers()
# Blood Group Wise Donation Requests
context['donation_request_a_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="A+").requests()
context['donation_request_a_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="A-").requests()
context['donation_request_b_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="B+").requests()
context['donation_request_b_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="B-").requests()
context['donation_request_ab_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="AB+").requests()
context['donation_request_ab_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="AB-").requests()
context['donation_request_o_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="O+").requests()
context['donation_request_o_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="O-").requests()
# Donation Type
context['donation_blood'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().blood_type().offers()
context['donation_organ'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter().organ_type().offers()
context['donation_tissue'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
).tissue_type().offers()
context['donation_request_blood'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
).blood_type().requests()
context['donation_request_organ'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
).organ_type().requests()
context['donation_request_tissue'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
).tissue_type().requests()
# Blood Donation Offers
context['blood_donation_a_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="A+").blood_type().offers()
context['blood_donation_a_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="A-").blood_type().offers()
context['blood_donation_b_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="B+").blood_type().offers()
context['blood_donation_b_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="B-").blood_type().offers()
context['blood_donation_ab_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="AB+").blood_type().offers()
context['blood_donation_ab_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="AB-").blood_type().offers()
context['blood_donation_o_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="O+").blood_type().offers()
context['blood_donation_o_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="O-").blood_type().offers()
# Blood Donation Requests
context['blood_donation_request_a_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="A+").blood_type().requests()
context['blood_donation_request_a_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="A-").blood_type().requests()
context['blood_donation_request_b_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="B+").blood_type().requests()
context['blood_donation_request_b_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="B-").blood_type().requests()
context['blood_donation_request_ab_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="AB+").blood_type().requests()
context['blood_donation_request_ab_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="AB-").blood_type().requests()
context['blood_donation_request_o_pos'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="O+").blood_type().requests()
context['blood_donation_request_o_neg'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    blood_group__iexact="O-").blood_type().requests()
# Organ Donation Offers
context['organ_donation_heart'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Heart").organ_type().offers()
context['organ_donation_kidney'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Kidney").organ_type().offers()
context['organ_donation_pancreas'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Pancreas").organ_type().offers()
context['organ_donation_lungs'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Lungs").organ_type().offers()
context['organ_donation_liver'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Liver").organ_type().offers()
context['organ_donation_intestines'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Intestines").organ_type().offers()
# Organ Donation Requests
context['organ_donation_request_heart'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Heart").organ_type().requests()
context['organ_donation_request_kidney'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Kidney").organ_type().requests()
context['organ_donation_request_pancreas'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Pancreas").organ_type().requests()
context['organ_donation_request_lungs'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Lungs").organ_type().requests()
context['organ_donation_request_liver'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Liver").organ_type().requests()
context['organ_donation_request_intestines'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    organ_name__iexact="Intestines").organ_type().requests()
# Tissue Donation Offers
context['tissue_donation_bones'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Bones'").tissue_type().offers()
context['tissue_donation_ligaments'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Ligaments").tissue_type().offers()
context['tissue_donation_tendons'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Tendons").tissue_type().offers()
context['tissue_donation_fascia'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Fascia").tissue_type().offers()
context['tissue_donation_veins'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Veins").tissue_type().offers()
context['tissue_donation_nerves'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Nerves").tissue_type().offers()
context['tissue_donation_corneas'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Corneas").tissue_type().offers()
context['tissue_donation_sclera'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Sclera").tissue_type().offers()
context['tissue_donation_heart_valves'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Heart Valves").tissue_type().offers()
context['tissue_donation_skin'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Skin").tissue_type().offers()
# Tissue Donation Requests
context['tissue_donation_request_bones'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Bones'").tissue_type().requests()
context['tissue_donation_request_ligaments'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Ligaments").tissue_type().requests()
context['tissue_donation_request_tendons'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Tendons").tissue_type().requests()
context['tissue_donation_request_fascia'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Fascia").tissue_type().requests()
context['tissue_donation_request_veins'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Veins").tissue_type().requests()
context['tissue_donation_request_nerves'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Nerves").tissue_type().requests()
context['tissue_donation_request_corneas'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Corneas").tissue_type().requests()
context['tissue_donation_request_sclera'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Sclera").tissue_type().requests()
context['tissue_donation_request_heart_valves'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Heart Valves").tissue_type().requests()
context['tissue_donation_request_skin'] = Donation.objects.search(
    query).filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(
    tissue_name__iexact="Skin").tissue_type().requests()
