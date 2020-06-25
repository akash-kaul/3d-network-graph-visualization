fetch('http://127.0.0.1:5000/all_data', {method: 'POST', headers: {'Content-Type': 'application/json'}})
    .then(function(response) {
        if (response.status != 200) {
            console.log('There was an error fetching the data');
            return;
        }
        response.json().then(function(data) {
            // console.log(data)
            const distance = 1400;
            const Graph = ForceGraph3D({controlType: 'orbit'})
                (document.getElementById("3d-graph"))
                    .cooldownTicks(200)
                    .cooldownTime(10000)
                    .nodeLabel('description')
                    .nodeAutoColorBy('group')
                    .cameraPosition({z: distance})
                    .forceEngine('ngraph')
                    .onNodeHover(node => document.getElementById('3d-graph').style.cursor = node ? 'pointer' : null)
                    .graphData(data);
            let angle = 0;
            (function myLoop(i) {
                setTimeout(function() {
                    Graph.cameraPosition({
                        x: distance * Math.sin(angle),
                        z: distance * Math.cos(angle)
                    });
                    angle += Math.PI / 300;
                    if (--i) myLoop(i);
                }, 20)
            })(500);
        });
    });
