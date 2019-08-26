<div class="col-md-12">
    <div id="carouselExampleControls" class="carousel slide" data-ride="carousel">
        <div class="carousel-inner">
            {% for campaign in campaigns %}
            <div class="carousel-item">
                {% if not campaign.image == "" %}
                <img class="d-block w-100" src="{{ campaign.image.url }}" alt="{{campaign.title}}"
                    style="height:150px;width:100px;">
                {% else %}
                <img class="d-block w-100" src="{% static 'images/raw/campaign.png' %}" alt="{{campaign.title}}"
                    style="height:150px;width:100px;">
                {% endif %}
                <div class="carousel-caption d-none d-md-block">
                    <h5>{{campaign.title}}</h5>
                    <p>Held Date: {{ campaign.held_date }}</p>
                    <p>End Date: {{ campaign.end_date }}</p>
                </div>
            </div>
            {% empty %}
            <div class="alert alert-warning">
                No campaigns found!
            </div>
            {% endfor %}
        </div>
        <a class="carousel-control-prev" href="#carouselExampleControls" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="sr-only">Previous</span>
        </a>
        <a class="carousel-control-next" href="#carouselExampleControls" role="button" data-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="sr-only">Next</span>
        </a>
    </div>
</div>