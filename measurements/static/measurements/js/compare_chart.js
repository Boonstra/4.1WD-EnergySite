compare_chart = function()
{
    var self = {};

    /**
     * Initialize.
     */
    self.init = function()
    {
        self.graphData1   = [];
        self.graphLabels1 = [];
        self.graphData2   = [];
        self.graphLabels2 = [];

        self.$comparisonMethodField = $$('.comparison-method');
        self.$deviceModelField      = $$('.device-model');
        self.$deviceCategoryField   = $$('.device-category');
        self.$zipcodeField          = $$('.zipcode');

        self.getGraphData();
    };

    /**
     * Retrieves the data for the graph.
     */
    self.getGraphData = function()
    {
        var comparisonMethodFieldValue = self.$comparisonMethodField[0].getSelected().get('value'),
            deviceModelFieldValue      = self.$deviceModelField[0].getSelected().get('value'),
            deviceCategoryFieldValue   = self.$deviceCategoryField[0].getSelected().get('value'),
            zipcodeFieldValue          = self.$zipcodeField[0].get('value');

        new Request({
            url: 'http://localhost:8888/api/measurements/',
            method: 'get',
            onSuccess: function(responseText){
                var labelAndData = self.parseJSONMeasurementsAsLabelAndData(JSON.parse(responseText));

                self.graphLabels2 = labelAndData['labels'];
                self.graphData2   = labelAndData['data'];

                self.drawLineGraph();
            },
            onFailure: function(){
                console.log('Request failed');
            }
        }).send('comparison_method=' + comparisonMethodFieldValue + '&' +
                'device_model=' + deviceModelFieldValue + '&' +
                'device_category_id=' + deviceCategoryFieldValue + '&' +
                'zipcode=' + zipcodeFieldValue);

        self.drawLineGraph();
    };

    /**
     * Draws the line graph.
     */
    self.drawLineGraph = function()
    {
        function getAnchors(p1x, p1y, p2x, p2y, p3x, p3y) {
            var l1 = (p2x - p1x) / 2,
                l2 = (p3x - p2x) / 2,
                a = Math.atan((p2x - p1x) / Math.abs(p2y - p1y)),
                b = Math.atan((p3x - p2x) / Math.abs(p2y - p3y));
            a = p1y < p2y ? Math.PI - a : a;
            b = p3y < p2y ? Math.PI - b : b;
            var alpha = Math.PI / 2 - ((a + b) % (Math.PI * 2)) / 2,
                dx1 = l1 * Math.sin(alpha + a),
                dy1 = l1 * Math.cos(alpha + a),
                dx2 = l2 * Math.sin(alpha + b),
                dy2 = l2 * Math.cos(alpha + b);
            return {
                x1: p2x - dx1,
                y1: p2y + dy1,
                x2: p2x + dx2,
                y2: p2y + dy2
            };
        }

        // Grab the data
        var labels       = [],
            data         = [],
            measurements = JSON.parse('[{"time": 1, "value": 0.03}, {"time": 2, "value": 0.035}, {"time": 3, "value": 0.045000000000000005}, {"time": 4, "value": 0.065}, {"time": 5, "value": 0.125}, {"time": 6, "value": 0.15000000000000002}, {"time": 7, "value": 0.15000000000000002}, {"time": 8, "value": 0.55}, {"time": 9, "value": 0.45}, {"time": 10, "value": 0.33999999999999997}]');

        for (var measurementsIndex = 0; measurementsIndex < measurements.length; measurementsIndex++)
        {
            data.push(Math.round(measurements[measurementsIndex].value * 100) / 100);

            for (var timesIndex = 0; timesIndex < times.length; timesIndex++)
            {
                if (times[timesIndex].pk === measurements[measurementsIndex].time)
                {
                    labels.push(times[timesIndex].fields.time);
                }
            }
        }

        // Draw
        var width = 800,
            height = 250,
            leftgutter = 30,
            bottomgutter = 20,
            topgutter = 20,
            colorhue = .6 || Math.random(),
            color = "hsl(" + [colorhue, .5, .5] + ")",
            r = Raphael("compare-chart", width, height),
            txt = {font: '12px Helvetica, Arial', fill: "#fff"},
            txt1 = {font: '10px Helvetica, Arial', fill: "#000"},
            txt2 = {font: '12px Helvetica, Arial', fill: "#000"},
            X = (width - leftgutter) / labels.length,
            max = Math.max.apply(Math, data),
            Y = (height - bottomgutter - topgutter) / max;
        r.drawGrid(leftgutter + X * .5 + .5, topgutter + .5, width - leftgutter - X, height - topgutter - bottomgutter, 10, 10, "#000");
        var path = r.path().attr({stroke: color, "stroke-width": 4, "stroke-linejoin": "round"}),
            bgp = r.path().attr({stroke: "none", opacity: .3, fill: color}),
            label = r.set(),
            lx = 0, ly = 0,
            is_label_visible = false,
            leave_timer,
            blanket = r.set();
        label.push(r.text(60, 12, "").attr(txt));
        label.push(r.text(60, 27, "").attr(txt1).attr({fill: color}));
        label.hide();
        var frame = r.popup(100, 100, label, "right").attr({fill: "#000", stroke: "#666", "stroke-width": 2, "fill-opacity": .7}).hide();

        var p, bgpp;
        for (var i = 0, ii = labels.length; i < ii; i++) {
            var y = Math.round(height - bottomgutter - Y * data[i]),
                x = Math.round(leftgutter + X * (i + .5)),
                t = r.text(x, height - 6, labels[i]).attr(txt).toBack();
            if (!i) {
                p = ["M", x, y, "C", x, y];
                bgpp = ["M", leftgutter + X * .5, height - bottomgutter, "L", x, y, "C", x, y];
            }
            if (i && i < ii - 1) {
                var Y0 = Math.round(height - bottomgutter - Y * data[i - 1]),
                    X0 = Math.round(leftgutter + X * (i - .5)),
                    Y2 = Math.round(height - bottomgutter - Y * data[i + 1]),
                    X2 = Math.round(leftgutter + X * (i + 1.5));
                var a = getAnchors(X0, Y0, x, y, X2, Y2);
                p = p.concat([a.x1, a.y1, x, y, a.x2, a.y2]);
                bgpp = bgpp.concat([a.x1, a.y1, x, y, a.x2, a.y2]);
            }
            var dot = r.circle(x, y, 4).attr({fill: "#333", stroke: color, "stroke-width": 2});
            blanket.push(r.rect(leftgutter + X * i, 0, X, height - bottomgutter).attr({stroke: "none", fill: "#fff", opacity: 0}));
            var rect = blanket[blanket.length - 1];
            (function (x, y, data, lbl, dot) {
                var timer, i = 0;
                rect.hover(function () {
                    clearTimeout(leave_timer);
                    var side = "right";
                    if (x + frame.getBBox().width > width) {
                        side = "left";
                    }
                    var ppp = r.popup(x, y, label, side, 1),
                        anim = Raphael.animation({
                            path: ppp.path,
                            transform: ["t", ppp.dx, ppp.dy]
                        }, 200 * is_label_visible);
                    lx = label[0].transform()[0][1] + ppp.dx;
                    ly = label[0].transform()[0][2] + ppp.dy;
                    frame.show().stop().animate(anim);
                    label[0].attr({text: data}).show().stop().animateWith(frame, anim, {transform: ["t", lx, ly]}, 200 * is_label_visible);
                    label[1].attr({text: ""}).show().stop().animateWith(frame, anim, {transform: ["t", lx, ly]}, 200 * is_label_visible);
                    dot.attr("r", 6);
                    is_label_visible = true;
                }, function () {
                    dot.attr("r", 4);
                    leave_timer = setTimeout(function () {
                        frame.hide();
                        label[0].hide();
                        label[1].hide();
                        is_label_visible = false;
                    }, 1);
                });
            })(x, y, data[i], labels[i], dot);
        }
        p = p.concat([x, y, x, y]);
        bgpp = bgpp.concat([x, y, x, y, "L", x, height - bottomgutter, "z"]);
        path.attr({path: p});
        bgp.attr({path: bgpp});
        frame.toFront();
        label[0].toFront();
        label[1].toFront();
        blanket.toFront();
    };

    /**
     *
     */
    self.parseJSONMeasurementsAsLabelAndData = function(measurements)
    {
        var labels       = [],
            data         = [];

        for (var measurementsIndex = 0; measurementsIndex < measurements.length; measurementsIndex++)
        {
            data.push(Math.round(measurements[measurementsIndex].value * 100) / 100);

            for (var timesIndex = 0; timesIndex < times.length; timesIndex++)
            {
                if (times[timesIndex].pk === measurements[measurementsIndex].time)
                {
                    labels.push(times[timesIndex].fields.time);
                }
            }
        }

        return {label: labels, data: data};
    };

    window.addEvent('domready', function()
    {
        self.init();
    });
}();