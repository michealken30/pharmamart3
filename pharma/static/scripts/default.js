<script>
    document.addEventListener('DOMContentLoaded', function() {
        var addToCartForms = document.querySelectorAll('.add-to-cart-form');

        addToCartForms.forEach(function(form) {
            form.addEventListener('submit', function(event) {
                // Prevent the default form submission behavior
                event.preventDefault();

                // Store the current scroll position
                var scrollPosition = window.scrollY;

                // Perform any additional logic (e.g., add the product to the cart)
                // You may need to make an AJAX request here

                // Submit the form programmatically
                form.submit();

                // Scroll back to the stored position after form submission
                window.scrollTo(0, scrollPosition);
            });
        });
    });
</script>