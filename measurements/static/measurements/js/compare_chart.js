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

        self.$comparisonMethodField.addEvent('change', function(){ self.reloadGraphData(); });
        self.$deviceModelField.addEvent('change', function(){ self.reloadGraphData(); });
        self.$deviceCategoryField.addEvent('change', function(){ self.reloadGraphData(); });
        self.$zipcodeField.addEvent('change', function(){ self.reloadGraphData(); });

        self.reloadGraphData();
    };

    /**
     * Retrieves the data for the graph.
     */
    self.reloadGraphData = function()
    {
        console.log('reloading graph');

        var comparisonMethodFieldValue = self.$comparisonMethodField[0].getSelected().get('value'),
            deviceModelFieldValue      = self.$deviceModelField[0].getSelected().get('value'),
            deviceCategoryFieldValue   = self.$deviceCategoryField[0].getSelected().get('value'),
            zipcodeFieldValue          = self.$zipcodeField[0].get('value');

        new Request({
            url: 'http://localhost:8888/api/measurements/',
            method: 'get',
            onSuccess: function(responseText)
            {
                var json          = JSON.parse(responseText),
                    labelAndData1 = self.parseJSONMeasurementsAsLabelAndData(json['current_user_measurements']),
                    labelAndData2 = self.parseJSONMeasurementsAsLabelAndData(json['average_measurements']);

                self.graphLabels1 = labelAndData1['labels'];
                self.graphData1   = labelAndData1['data'];
                self.graphLabels2 = labelAndData2['labels'];
                self.graphData2   = labelAndData2['data'];

                self.drawLineGraph();
            },
            onFailure: function()
            {
                console.log('Request failed');
            }
        }).send('comparison_method=' + comparisonMethodFieldValue + '&' +
                'device_model=' + deviceModelFieldValue + '&' +
                'device_category_id=' + deviceCategoryFieldValue + '&' +
                'zipcode=' + zipcodeFieldValue);
    };

    /**
     * Draws the line graph.
     */
    self.drawLineGraph = function()
    {
        $('compare-chart').set('html', '');

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
        var labels1 = self.graphLabels1,
            data1   = self.graphData1,
            labels2 = self.graphLabels2,
            data2    = self.graphData2;

        // Draw
        var width = 800,
            height = 250,
            leftgutter = 30,
            bottomgutter = 20,
            topgutter = 20,
            colorhue1 = .6 || Math.random(),
            colorhue2 = .3 || Math.random(),
            color1 = "hsl(" + [colorhue1, .5, .5] + ")",
            color2 = "hsl(" + [colorhue2, .5, .5] + ")",
            r = Raphael("compare-chart", width, height),
            txt = {font: '12px Helvetica, Arial', fill: "#000"},
            X = (width - leftgutter) / labels2.length,
            max = Math.max.apply(Math, data2),
            Y = (height - bottomgutter - topgutter) / max;
        r.drawGrid(leftgutter + X * .5 + .5, topgutter + .5, width - leftgutter - X, height - topgutter - bottomgutter, 10, 10, "#000");
        var path1 = r.path().attr({stroke: color1, "stroke-width": 4, "stroke-linejoin": "round"}),
            path2 = r.path().attr({stroke: color2, "stroke-width": 4, "stroke-linejoin": "round"}),
            label = r.set(),
            lx = 0, ly = 0,
            is_label_visible = false,
            leave_timer,
            blanket = r.set();
        label.push(r.text(0, 0, "").attr(txt));
        label.hide();

        var frame = r.popup(100, 100, label, "right").attr({fill: "#fff", stroke: "#666", "stroke-width": 2, "fill-opacity": .7}).hide();

        (function()
        {
            var p, bgpp;
            for (var i = 0, ii = labels1.length; i < ii; i++) {
                var y = Math.round(height - bottomgutter - Y * data1[i]),
                    x = Math.round(leftgutter + X * (i + .5)),
                    t = r.text(x, height - 6, labels1[i]).attr(txt).toBack();
                if (!i) {
                    p = ["M", x, y, "C", x, y];
                    bgpp = ["M", leftgutter + X * .5, height - bottomgutter, "L", x, y, "C", x, y];
                }
                if (i && i < ii - 1) {
                    var Y0 = Math.round(height - bottomgutter - Y * data1[i - 1]),
                        X0 = Math.round(leftgutter + X * (i - .5)),
                        Y2 = Math.round(height - bottomgutter - Y * data1[i + 1]),
                        X2 = Math.round(leftgutter + X * (i + 1.5));
                    var a = getAnchors(X0, Y0, x, y, X2, Y2);
                    p = p.concat([a.x1, a.y1, x, y, a.x2, a.y2]);
                    bgpp = bgpp.concat([a.x1, a.y1, x, y, a.x2, a.y2]);
                }
                var dot = r.circle(x, y, 4).attr({fill: "#333", stroke: color1, "stroke-width": 2});
                blanket.push(r.rect(leftgutter + X * i, 0, X, height - bottomgutter).attr({stroke: "none", fill: "#fff", opacity: 0}));
                var rect = blanket[blanket.length - 1];
                (function (x, y, data, lbl, dot) {
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
                        dot.attr("r", 6);
                        is_label_visible = true;
                    }, function () {
                        dot.attr("r", 4);
                        leave_timer = setTimeout(function () {
                            frame.hide();
                            label[0].hide();
                            is_label_visible = false;
                        }, 1);
                    });
                })(x, y, data1[i], labels1[i], dot);
            }

            p = p.concat([x, y, x, y]);
            bgpp = bgpp.concat([x, y, x, y, "L", x, height - bottomgutter, "z"]);
            path1.attr({path: p});
            frame.toFront();
            label[0].toFront();
            blanket.toFront();
        })();

        (function()
        {
            var p, bgpp;
            for (var i = 0, ii = labels2.length; i < ii; i++) {
                var y = Math.round(height - bottomgutter - Y * data2[i]),
                    x = Math.round(leftgutter + X * (i + .5)),
                    t = r.text(x, height - 6, labels2[i]).attr(txt).toBack();
                if (!i) {
                    p = ["M", x, y, "C", x, y];
                    bgpp = ["M", leftgutter + X * .5, height - bottomgutter, "L", x, y, "C", x, y];
                }
                if (i && i < ii - 1) {
                    var Y0 = Math.round(height - bottomgutter - Y * data2[i - 1]),
                        X0 = Math.round(leftgutter + X * (i - .5)),
                        Y2 = Math.round(height - bottomgutter - Y * data2[i + 1]),
                        X2 = Math.round(leftgutter + X * (i + 1.5));
                    var a = getAnchors(X0, Y0, x, y, X2, Y2);
                    p = p.concat([a.x1, a.y1, x, y, a.x2, a.y2]);
                    bgpp = bgpp.concat([a.x1, a.y1, x, y, a.x2, a.y2]);
                }
                var dot = r.circle(x, y, 4).attr({fill: "#333", stroke: color1, "stroke-width": 2});
                blanket.push(r.rect(leftgutter + X * i, 0, X, height - bottomgutter).attr({stroke: "none", fill: "#fff", opacity: 0}));
                var rect = blanket[blanket.length - 1];
                (function (x, y, data, lbl, dot) {
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
                        dot.attr("r", 6);
                        is_label_visible = true;
                    }, function () {
                        dot.attr("r", 4);
                        leave_timer = setTimeout(function () {
                            frame.hide();
                            label[0].hide();
                            is_label_visible = false;
                        }, 1);
                    });
                })(x, y, data2[i], labels2[i], dot);
            }

            p = p.concat([x, y, x, y]);
            bgpp = bgpp.concat([x, y, x, y, "L", x, height - bottomgutter, "z"]);
            path2.attr({path: p});
            frame.toFront();
            label[0].toFront();
            blanket.toFront();
        })();
    };

    /**
     * Parse measurements as labels and data
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

        return {labels: labels, data: data};
    };

    window.addEvent('domready', function()
    {
        self.init();
    });
}();