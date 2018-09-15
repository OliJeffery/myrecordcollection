$( document ).ready(
	function() {
		resizeGrid()
		$('#content').attr('style','opacity:1; transition: opacity 1s ease-in;');
	}
)

$(window).resize(function() {
    if(this.resizeTO) clearTimeout(this.resizeTO);
    this.resizeTO = setTimeout(function() {
        $(this).trigger('resizeEnd');
    }, 500);
});

$(window).bind('resizeEnd', function() {
    resizeGrid();
});

function resizeGrid() {
	var grid = $('.preview');
	grid.each(
		function() {
			var square = $(this);
			square_width = square.width();
			square.height(square_width);
			currentImage = square.find('.image');
			var lazyImage = currentImage.data('lazyLoad');
			currentImage.prop('style','background-image: url("'+lazyImage+'");').width(square_width).height(square_width);
		}
	);
	console.log('Grid resized');
}


console.log('Only sick music makes money nowadays')