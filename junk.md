{% extends base_template %}

{% block head_title %}{% block page_title %}{% block breadcrumb %}
Donation List
{% endblock %}{% endblock %}{% endblock %}


{% load static %}

{% block extra_css %}
<!-- Datatable css -->
<link rel="stylesheet" href="{% static 'vendor/jquery-datatable/dataTables.min.css' %}" type="text/css" />
{% endblock %}


{% block content %}

<div class="table-responsive">
    <table id="donationBankDataTable" class="cell-border hover table-bordered table-hover text-center"
        style="width:100%">
        <thead>
            <tr>
                <th>#</th>
                <th>Donor</th>
                <th>Blood Group</th>
                <th>Contact</th>
                <th>Country</th>
                <th>Donation Type</th>
                <th>Details</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for donation in donation_list %}
            <tr class="text-dark">
                <th scope="row">{{ forloop.counter }}</th>
                <td>
                    <b>
                        {{ donation.get_donor_name }}
                    </b>
                </td>
                <td>
                    {{ donation.blood_group }}
                </td>
                <td>
                    <a href="#">
                        {{ donation.contact }}
                    </a>
                </td>
                <td>
                    {{ donation.country.name }}
                </td>
                <td>
                    {{ donation.donation_type }}
                </td>
                <td>
                    {{ donation.get_type_dynamic_short_detail }}
                </td>
                <td>
                    {{ donation.donation_progress.get_progress_status }}
                </td>
                <td>
                    <a href="/donation-bank/{{donation.slug}}/details/" class="btn btn-secondary btn-xs text-deco-none">
                        <span class="">
                            View
                        </span>
                    </a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="8" class="text-center">
                    <div class="alert alert-warning">
                        No item found!
                    </div>
                </td>
            </tr>
            {% endfor %}
        </tbody>
        <tfoot>
            <tr class="text-center">
                <th>#</th>
                <th>Donor</th>
                <th>Blood Group</th>
                <th>Contact</th>
                <th>Country</th>
                <th>Donation Type</th>
                <th>Details</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
        </tfoot>
    </table>
</div>

{% include 'donationBank/snippets/footer.html' %}

{% endblock %}

{% block extra_js %}
<input type="hidden" id="total_records_count" value="{{donation_list.count}}">
<!-- Datatable JS -->
<script type="text/javascript" src="{% static 'vendor/jquery-datatable/dataTables.min.js' %}"></script>
<script>
    $(document).ready(function () {
        $('#donationBankDataTable').DataTable({
            destroy: true,
            //"retrieve": true,
            //"order": [[ 1, 'desc' ]],
            "ordering": false,
            //"searching": false,
            //"paging": false,
            //"scrollY": 400,
            //"scrollX": 400,
            //"scrollY": '62vh',
            //"scrollX": '50vh',
            "scrollCollapse": true,
            "stateSave": true,
            "pagingType": "full_numbers",
            "language": {
                "lengthMenu": "Display _MENU_ records per page. <span class='ml-4 text-primary'>Total Records: <span class='font-13 font-bold'>" +
                    $("#total_records_count").val() + "</span></span>",
                "zeroRecords": "Nothing found - sorry",
                "info": "Showing page _PAGE_ of _PAGES_",
                "infoEmpty": "No records available",
                "infoFiltered": "(filtered from _MAX_ total records)"
            },
        });
    });
</script>
{% endblock %}