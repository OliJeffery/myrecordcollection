$( document ).ready(
	function() {
		var thumbs = $('.image')
		var time = 10;
		thumbs.each(
			function() {
				var currentImage = $(this);
				setTimeout(function() {
					var lazyImage = currentImage.data('lazyLoad');
					currentImage.prop('style','background-image: url("'+lazyImage+'")');
					console.log(lazyImage);
				},time);
				time += 10;
			}
		)
	}
)

console.log('Only sick music makes money nowadays')