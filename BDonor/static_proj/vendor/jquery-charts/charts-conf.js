! function ($) {

    $(function () {

        // sparkline
        var sr, sparkline = function ($re) {
            $(".sparkline").each(function () {
                var $data = $(this).data();
                if ($re && !$data.resize) return;
                ($data.type == 'pie') && $data.sliceColors && ($data.sliceColors = eval($data.sliceColors));
                ($data.type == 'bar') && $data.stackedBarColor && ($data.stackedBarColor = eval($data.stackedBarColor));
                $data.valueSpots = {
                    '0:': $data.spotColor
                };
                $(this).sparkline('html', $data);
            });
        };
        $(window).resize(function (e) {
            clearTimeout(sr);
            sr = setTimeout(function () {
                sparkline(true)
            }, 500);
        });
        sparkline(false);


        // easypie
        $('.easypiechart').each(function () {
            var $this = $(this),
                $data = $this.data(),
                $step = $this.find('.step'),
                $target_value = parseInt($($data.target).text()),
                $value = 0;
            $data.barColor || ($data.barColor = function ($percent) {
                $percent /= 100;
                return "rgb(" + Math.round(200 * $percent) + ", 200, " + Math.round(200 * (1 - $percent)) + ")";
            });
            $data.onStep = function (value) {
                $value = value;
                $step.text(parseInt(value));
                $data.target && $($data.target).text(parseInt(value) + $target_value);
            }
            $data.onStop = function () {
                $target_value = parseInt($($data.target).text());
                $data.update && setTimeout(function () {
                    $this.data('easyPieChart').update(100 - $value);
                }, $data.update);
            }
            $(this).easyPieChart($data);
        });
    });
}(window.jQuery);



// Blood Group Wise

// Donation

var donationBloodGroupBarChart = document.getElementById('donationBloodGroupBarChart').getContext('2d');

var myDonationBloodGroupBarChart = new Chart(donationBloodGroupBarChart, {
    type: 'bar',
    data: {
        labels: ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        datasets: [{
            label: "Donations",
            backgroundColor: 'rgb(23, 125, 255)',
            borderColor: 'rgb(23, 125, 255)',
            data: [
                $("#donation_a_pos").val(), 
                $("#donation_a_neg").val(), 
                $("#donation_b_pos").val(), 
                $("#donation_b_neg").val(), 
                $("#donation_ab_pos").val(), 
                $("#donation_ab_neg").val(), 
                $("#donation_o_pos").val(), 
                $("#donation_o_neg").val()
            ],
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
    }
});

// Donation Request

var donationRequestBloodGroupBarChart = document.getElementById('donationRequestBloodGroupBarChart').getContext('2d');

var myDonationRequestBloodGroupBarChart = new Chart(donationRequestBloodGroupBarChart, {
    type: 'bar',
    data: {
        labels: ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        datasets: [{
            label: "Donation Requests",
            backgroundColor: 'rgb(23, 125, 255)',
            borderColor: 'rgb(23, 125, 255)',
            data: [
                $("#donation_request_a_pos").val(),
                $("#donation_request_a_neg").val(),
                $("#donation_request_b_pos").val(),
                $("#donation_request_b_neg").val(),
                $("#donation_request_ab_pos").val(),
                $("#donation_request_ab_neg").val(),
                $("#donation_request_o_pos").val(),
                $("#donation_request_o_neg").val()
            ],
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
    }
});


// Blood Donation Statistics

// Donation

var bloodDonationBarChart = document.getElementById('bloodDonationBarChart').getContext('2d');

var myBloodDonationBarChart = new Chart(bloodDonationBarChart, {
    type: 'bar',
    data: {
        labels: ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        datasets: [{
            label: "Donations",
            backgroundColor: 'rgb(23, 125, 255)',
            borderColor: 'rgb(23, 125, 255)',
            data: [
                $("#blood_donation_a_pos").val(),
                $("#blood_donation_a_neg").val(),
                $("#blood_donation_b_pos").val(),
                $("#blood_donation_b_neg").val(),
                $("#blood_donation_ab_pos").val(),
                $("#blood_donation_ab_neg").val(),
                $("#blood_donation_o_pos").val(),
                $("#blood_donation_o_neg").val()
            ],
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
    }
});

// Donation Request

var bloodDonationRequestBarChart = document.getElementById('bloodDonationRequestBarChart').getContext('2d');

var myBloodDonationRequestBarChart = new Chart(bloodDonationRequestBarChart, {
    type: 'bar',
    data: {
        labels: ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        datasets: [{
            label: "Donation Requests",
            backgroundColor: 'rgb(23, 125, 255)',
            borderColor: 'rgb(23, 125, 255)',
            data: [
                $("#blood_donation_request_a_pos").val(),
                $("#blood_donation_request_a_neg").val(),
                $("#blood_donation_request_b_pos").val(),
                $("#blood_donation_request_b_neg").val(),
                $("#blood_donation_request_ab_pos").val(),
                $("#blood_donation_request_ab_neg").val(),
                $("#blood_donation_request_o_pos").val(),
                $("#blood_donation_request_o_neg").val()
            ],
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
    }
});


// Organ Donation Statistics

// Donation

var organDonationBarChart = document.getElementById('organDonationBarChart').getContext('2d');

var myOrganDonationBarChart = new Chart(organDonationBarChart, {
    type: 'bar',
    data: {
        labels: ["Heart", "Kidney", "Pancreas", "Lungs", "Liver", "Intestines"],
        datasets: [{
            label: "Donations",
            backgroundColor: 'rgb(23, 125, 255)',
            borderColor: 'rgb(23, 125, 255)',
            data: [
                $("#organ_donation_heart").val(),
                $("#organ_donation_kidney").val(),
                $("#organ_donation_pancreas").val(),
                $("#organ_donation_lungs").val(),
                $("#organ_donation_liver").val(),
                $("#organ_donation_intestines").val()
            ],
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
    }
});

// Donation Request

var organDonationRequestBarChart = document.getElementById('organDonationRequestBarChart').getContext('2d');

var myOrganDonationRequestBarChart = new Chart(organDonationRequestBarChart, {
    type: 'bar',
    data: {
        labels: ["Heart", "Kidney", "Pancreas", "Lungs", "Liver", "Intestines"],
        datasets: [{
            label: "Donation Requests",
            backgroundColor: 'rgb(23, 125, 255)',
            borderColor: 'rgb(23, 125, 255)',
            data: [
                $("#organ_donation_request_heart").val(),
                $("#organ_donation_request_kidney").val(),
                $("#organ_donation_request_pancreas").val(),
                $("#organ_donation_request_lungs").val(),
                $("#organ_donation_request_liver").val(),
                $("#organ_donation_request_intestines").val()
            ],
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
    }
});


// Tissue Donation Statistics

// Donation

var tissueDonationBarChart = document.getElementById('tissueDonationBarChart').getContext('2d');

var myTissueDonationBarChart = new Chart(tissueDonationBarChart, {
    type: 'bar',
    data: {
        labels: ["Bones", "Ligaments", "Tendons", "Fascia", "Veins", "Nerves", "Corneas", "Sclera", "Heart Valves", "Skin"],
        datasets: [{
            label: "Donations",
            backgroundColor: 'rgb(23, 125, 255)',
            borderColor: 'rgb(23, 125, 255)',
            data: [
                $("#tissue_donation_bones").val(),
                $("#tissue_donation_ligaments").val(),
                $("#tissue_donation_tendons").val(),
                $("#tissue_donation_fascia").val(),
                $("#tissue_donation_veins").val(),
                $("#tissue_donation_nerves").val(),
                $("#tissue_donation_corneas").val(),
                $("#tissue_donation_sclera").val(),
                $("#tissue_donation_heart_valves").val(),
                $("#tissue_donation_skin").val()
            ],
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
    }
});

// Donation Request

var tissueDonationRequestBarChart = document.getElementById('tissueDonationRequestBarChart').getContext('2d');

var myTissueDonationRequestBarChart = new Chart(tissueDonationRequestBarChart, {
    type: 'bar',
    data: {
        labels: ["Bones", "Ligaments", "Tendons", "Fascia", "Veins", "Nerves", "Corneas", "Sclera", "Heart Valves", "Skin"],
        datasets: [{
            label: "Donation Request",
            backgroundColor: 'rgb(23, 125, 255)',
            borderColor: 'rgb(23, 125, 255)',
            data: [
                $("#tissue_donation_request_bones").val(),
                $("#tissue_donation_request_ligaments").val(),
                $("#tissue_donation_request_tendons").val(),
                $("#tissue_donation_request_fascia").val(),
                $("#tissue_donation_request_veins").val(),
                $("#tissue_donation_request_nerves").val(),
                $("#tissue_donation_request_corneas").val(),
                $("#tissue_donation_request_sclera").val(),
                $("#tissue_donation_request_heart_valves").val(),
                $("#tissue_donation_request_skin").val()
            ],
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
    }
});