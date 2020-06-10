 
 
 $("#year").text(new Date().getFullYear());

 $(".carousel").carousel({
        interval: 2000,
        pause: "hover"
      });

//lightbox init
      $(document).on("click", '[data-toggle="lightbox"]', function(e) {
        e.preventDefault();
        $(this).ekkoLightbox();
      });



