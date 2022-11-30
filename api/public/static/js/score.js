
$(function () {

    var Speedometer = $('#speedometer').SonicGauge({
        label: 'Score Credit',
        start: { angle: -225, num: -100 },
        end: { angle: 45, num: 100 },
        markers: [
            {
                gap: 20,
                line: { "width": 20, "stroke": "none", "fill": "#eeeeee" },
                text: { "space": 22, "text-anchor": "middle", "fill": "#333333", "font-size": 18 }
            }, {
                gap: 10,
                line: { "width": 12, "stroke": "none", "fill": "#aaaaaa" },
                text: { "space": 18, "text-anchor": "middle", "fill": "#333333", "font-size": 12 }
            }, {
                gap: 5,
                line: { "width": 8, "stroke": "none", "fill": "#999999" }
            }
        ],
        animation_speed: 200
    });

    // Cycle gauge up and down

    function cycleGauge(el, delay, increment, min, max, current, target) {

        if (typeof current == "undefined") {
            current = min;
        }

        if (typeof target == "undefined") {
            target = max;
        }

        if (current < target) {
            current += increment;
        }
        else if (current > target) {
            current -= increment;
        }
        else {
            cycleGauge(el, delay, increment, min, max, current, target == min ? max : min);
            return;
        }

        el.SonicGauge('val', current);
        setTimeout(function () {
            cycleGauge(el, delay, increment, min, max, current, target);
        }, delay);

    }

});
