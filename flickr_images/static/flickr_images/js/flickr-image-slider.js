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

        self.$sliderContainer      = $$('.flickr-image-slider')[0];
        self.$descriptionContainer = $$('.flickr-image-description-container')[0];
        self.$currentSlide         = null;
        self.$currentDescription   = null;

        self.startRequestingImages();
        self.start();
    };

    /**
     * Start the slider.
     */
    self.start = function()
    {
        var refreshRate         = self.refreshRate,
            containerSize       = self.$sliderContainer.getSize(),
            $currentSlide       = self.$currentSlide,
            $currentDescription = self.$currentDescription,
            $newSlide,
            $newDescription,
            $imageLink,
            $image,
            image;

        if (self.imageBuffer.length > 0)
        {
            image = self.imageBuffer.shift();

            // Image
            $image = new Element('img', {
                'src': 'http://farm' + image.farm + '.staticflickr.com/' + image.server + '/' + image.id + '_' + image.secret + '_q.jpg'
            });

            // URL
            $imageLink = new Element('a', {
                'href': 'http://www.flickr.com/photos/' + image.owner.nsid + '/' + image.id,
                'target': '_blank'
            });

            // Description
            $newDescription = new Element('div', { 'class': 'flickr-image-description' });
            $newDescription.adopt(new Element('div', { 'text': image.title._content, 'class': 'flickr-image-title' }));
            $newDescription.adopt(new Element('div', { 'text': image.dates.taken, 'class': 'flickr-image-date' }));

            // Slide
            $newSlide = new Element('div', {
                'class' : 'flickr-image-slide'
            });

            $newSlide.adopt($imageLink.adopt($image));

            // Use the slide animation when replacing the current slide with a new one
            if (self.$currentSlide != null &&
                self.$currentDescription != null)
            {
                // Hide the new slide outside the container
                $newSlide.setStyles({
                    'top' : 0,
                    'left': -containerSize.x
                });

                $newDescription.setStyles({
                    'opacity': 0,
                    'visibility': 'hidden'
                });

                self.$sliderContainer.adopt($newSlide);
                self.$descriptionContainer.adopt($newDescription);

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

                self.$currentDescription.set('tween', { duration: 1000 }).fade('out');

                setTimeout(function()
                {
                    $currentSlide.destroy();
                    $currentDescription.destroy();

                    $newDescription.set('tween', { duration: 1000 }).fade('in');
                }, 1000);
            }
            else
            {
                self.$sliderContainer.adopt($newSlide);
                self.$descriptionContainer.adopt($newDescription);
            }

            self.$currentSlide       = $newSlide;
            self.$currentDescription = $newDescription;
        }
        else
        {
            refreshRate = 100;
        }

        setTimeout(function()
        {
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