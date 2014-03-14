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

        self.$container = $$('.flickr-image-slider');

        self.startRequestingImages();
        self.start();
    };

    /**
     * Start the slider.
     */
    self.start = function()
    {

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