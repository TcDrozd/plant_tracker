$(document).ready(function() {
    // Add CSRF token to AJAX requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    // Water plant button click handler
    $('.water-plant-btn').on('click', function() {
        const btn = $(this);
        const plantId = btn.data('plant-id');
        const card = btn.closest('.plant-card');
        
        // Add watering animation
        btn.html('<i class="fas fa-spinner fa-spin me-2"></i>Watering...');
        card.find('.fa-tint').addClass('watering-animation');
        
        // Make AJAX request to water the plant
        $.ajax({
            url: `/plant/${plantId}/water/`,
            type: 'POST',
            success: function(response) {
                if (response.status === 'success') {
                    // Format the date
                    const date = new Date(response.last_watered);
                    const options = { month: 'short', day: 'numeric', year: 'numeric' };
                    const formattedDate = date.toLocaleDateString('en-US', options);
                    
                    // Update the UI
                    card.find('.last-watered-date').text(formattedDate);
                    card.find('.days-since-watered').text(response.days);
                    
                    // Reset button text after delay
                    setTimeout(function() {
                        btn.html('<i class="fas fa-tint me-2"></i>Water Now');
                        card.find('.fa-tint').removeClass('watering-animation');
                    }, 1000);
                }
            },
            error: function() {
                alert('Error watering plant. Please try again.');
                btn.html('<i class="fas fa-tint me-2"></i>Water Now');
            }
        });
    });

    // Water all plants in a category
    $('.water-category-btn').on('click', function() {
        const btn = $(this);
        const category = btn.data('category');
        btn.html('<i class="fas fa-spinner fa-spin me-2"></i>Watering...');
        
        $.ajax({
            url: `/water/category/${encodeURIComponent(category)}/`,
            type: 'POST',
            success: function(response) {
                if (response.status === 'success') {
                    location.reload(); // Refresh to update all plants
                }
            },
            error: function() {
                alert('Error watering category. Please try again.');
                btn.html('<i class="fas fa-tint me-2"></i>Water All');
            }
        });
    });

    // Water all plants
    $('#water-all-btn').on('click', function() {
        const btn = $(this);
        btn.html('<i class="fas fa-spinner fa-spin me-2"></i>Watering...');
        
        $.ajax({
            url: '/water/all/',
            type: 'POST',
            success: function(response) {
                if (response.status === 'success') {
                    location.reload(); // Refresh to update all plants
                }
            },
            error: function() {
                alert('Error watering all plants. Please try again.');
                btn.html('<i class="fas fa-tint me-2"></i>Water All Plants');
            }
        });
    });
    // Persistent collapse states
    $('.category-header').on('click', function() {
        const target = $(this).data('bs-target');
        const isExpanded = $(target).hasClass('show');
        localStorage.setItem(target, isExpanded ? 'false' : 'true');
    });

    // Restore states on load
    $('.collapse').each(function() {
        const state = localStorage.getItem('#' + this.id);
        if (state === 'false') {
            $(this).removeClass('show');
            $(`[data-bs-target="#${this.id}"] .collapse-icon`)
                .removeClass('fa-chevron-down')
                .addClass('fa-chevron-right');
        }
    });

    // Toggle all categories
    $('.toggle-all-categories').click(function() {
        const allExpanded = $('.collapse.show').length === $('.collapse').length;
        $('.collapse').collapse(allExpanded ? 'hide' : 'show');
        
        // Update icons
        $('.collapse-icon').toggleClass('fa-chevron-down fa-chevron-right', allExpanded);
        
        // Update localStorage
        $('.collapse').each(function() {
            localStorage.setItem('#' + this.id, allExpanded ? 'false' : 'true');
        });
    });
});