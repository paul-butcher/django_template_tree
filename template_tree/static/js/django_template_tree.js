
/*
* The tree is heavily based on the d3 collapsible tree example.
*
* Nodes expand out of and collapse into their parent.
*
* http://mbostock.github.io/d3/talk/20111018/tree.html
* */

var diagonal = d3.svg.diagonal()
  .projection(function(d) {
      return [d.y, d.x];
  });


function update(source) {
  var duration = d3.event && d3.event.altKey ? 5000 : 500;

  // Compute the new tree layout.
  var nodes = tree.nodes(root);

  updateNodes(
      source,
      vis.selectAll("g.node").data(nodes, function(d) { return d.id || (d.id = ++i); }),
      duration
  );

  // Update the links…
  var link = vis.selectAll("path.link")
      .data(tree.links(nodes), function(d) { return d.target.id; });

  // Enter any new links at the parent's previous position.
  link.enter().insert("svg:path", "g")
      .attr("class", "link")
      .attr("d", function(d) {
        var o = {x: source.x0, y: source.y0};
        return diagonal({source: o, target: o});
      });

  // Transition links to their new position.
  link.transition()
      .duration(duration)
      .attr("d", diagonal);

  // Transition exiting nodes to the parent's new position.
  link.exit().transition()
      .duration(duration)
      .attr("d", function(d) {
        var o = {x: source.x, y: source.y};
        return diagonal({source: o, target: o});
      })
      .remove();

  // Stash the old positions for transition.
  nodes.forEach(function(d) {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}


function updateNodes(source, node, transition_duration){
    //Deal with the nodes portion of the tree.

  var nodeEnter = node.enter().append("svg:g")
      // A container for the label, this is positioned according to the tree data
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
      .on("click", function(d) { toggle(d); update(d); });

  text = nodeEnter.append("svg:text")
      // The label itself
      .attr("x", 10) // Add enough to get it away from the left-hand edge
      .attr("dy", ".35em")
      .attr("text-anchor",  "start")
      .text(function(d) { return d.name });

  text.each(
      // The label background
      function(d){
          var width = this.getComputedTextLength();
          d.node_width = width;
          var parent = d3.select(this.parentNode);
          parent.insert('svg:rect', ':first-child')
            .attr('fill', function(d) { return d._children ? "lightsteelblue" : "#dbe4f0"; })
            //Add 5 units of padding to left and right of the text
            .attr('width', width + 10)
            .attr('x', '5')
            .attr('height', '1.5em')
            .attr('y', '-0.75em')
            // A pleasing rounded corner
            .attr('rx', '0.25em');

            parent.append("path")
            .attr("d", d3.svg.symbol().type('cross'))
            .attr('transform', 'translate(' + (width + 25) + ')')
            .attr('stroke', '#808ea1')
            .attr('fill', '#808ea1')
;
      });

  // Transition nodes to their new position.
  nodeUpdate = node.transition()
      .duration(transition_duration)
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

  // Nodes that are fully open are black-on-light
  // Nodes with hidden children are white-on-dark
  nodeUpdate.select('rect')
      .attr('fill', function(d) { return d._children ? "#808ea1" : "#dbe4f0"; });

  nodeUpdate.select('text')
      .attr('fill', function(d) { return d._children ? "#fff" : "#000"; });

  // Nodes with hidden children have a visible plus sign
  nodeUpdate.select('path')
      .attr('visibility', function(d) { return d._children ? "visible" : "hidden"; });

  // Transition exiting nodes to the parent's new position.
  node.exit().transition()
      .duration(transition_duration)
      .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
      .remove();

}
// Toggle children.
function toggle(d) {
  if (d.children) {
    d._children = d.children;
    d.children = null;
  } else {
    d.children = d._children;
    d._children = null;
  }
}
