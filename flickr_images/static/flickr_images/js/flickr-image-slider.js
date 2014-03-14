var flickr_image_slider = function()
{
    var self = {};

    /**
     * Initialize
     */
    self.init = function()
    {
        self.page              = 1;
        self.refreshRate       = 5000;
        self.imageRequest      = null;
        self.imageBuffer       = [];
        self.requestImageTimer = null;

        self.$container    = $$('.flickr-image-slider')[0];
        self.$currentSlide = null;

        self.startRequestingImages();
        self.start();
    };

    /**
     * Start the slider.
     */
    self.start = function()
    {
        var refreshRate   = self.refreshRate,
            containerSize = self.$container.getSize(),
            animation,
            $newSlide,
            $imageLink,
            $image,
            image;

        if (self.imageBuffer.length > 0)
        {
            image = self.imageBuffer.shift();

            console.log(image);

            // Image
            $image = new Element('img', {
                'src': 'http://farm' + image.farm + '.staticflickr.com/' + image.server + '/' + image.id + '_' + image.secret + '_q.jpg'
            });

            // URL
            $imageLink = new Element('a', {
                'href': 'http://www.flickr.com/photos/' + image.owner.nsid + '/' + image.id,
                'target': '_blank'
            });

            // Slide
            $newSlide = new Element('div', {
                'class' : 'flickr-image-slide'
            });

            $newSlide.adopt($imageLink.adopt($image));

            // Use the slide animation when replacing the current slide with a new one
            if (self.$currentSlide != null)
            {
                // Hide the new slide outside the container
                $newSlide.setStyles({
                    'top' : 0,
                    'left': -containerSize.x
                });

                self.$container.adopt($newSlide);

                // Slide current slide out
                new Fx.Tween(self.$currentSlide, {
                    duration  : 1000,
                    transition: 'linear',
                    property  : 'left'
                }).start(0, containerSize.x);

                // Slide new slide in
                new Fx.Tween($newSlide, {
                    duration  : 1000,
                    transition: 'linear',
                    property  : 'left'
                }).start(-containerSize.x, 0);
            }
            else
            {
                self.$container.adopt($newSlide);
            }

            self.$currentSlide = $newSlide;
        }
        else
        {
            refreshRate = 100;
        }

        setTimeout(function()
        {
            if (self.page > 5) return;

            self.start();
        }, refreshRate);
    };

    /**
     * Starts calling the request images method every second to keep the image buffer filled.
     */
    self.startRequestingImages = function()
    {
        self.requestImages();

        setInterval(function()
        {
            console.log(typeof self.imageRequest, self.imageBuffer.length);
            if (self.imageBuffer.length <= 2)
            {
                self.requestImages();
            }
        }, 1000);
    };

    /**
     * Send a request for an image and store it in the image buffer.
     */
    self.requestImages = function()
    {
        var perPage = self.page > 1 ? 5 : 1;

        if (self.imageRequest != null)
        {
            return;
        }

        self.imageRequest = new Request({
            url: 'http://localhost:8888/api/flickr-images/',
            method: 'get',
            onSuccess: function(data)
            {
                var json;

                try
                {
                    json = JSON.parse(data);

                    if (typeof json.refresh_rate === 'number')
                    {
                        self.refreshRate = json.refresh_rate;
                    }

                    if (typeOf(json.images) === 'array')
                    {
                        self.imageBuffer = self.imageBuffer.concat(json.images);
                    }
                }
                catch(e){ }
            },
            onComplete: function()
            {
                self.imageRequest = null;
            }
        });

        self.imageRequest.send('page=' + self.page + '&per_page=' + perPage);

        self.page++;
    };

    window.addEvent('domready', function()
    {
        self.init();
    });

    return self;
}();