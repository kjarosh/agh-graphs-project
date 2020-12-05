# Graph representation

The graph is represented using the
[`Graph`](https://networkx.org/documentation/stable/reference/classes/graph.html)
class from `networkx`.
A single node should contain the following attributes:
* `layer` &mdash; number of the layer this node is on,
* `position` &mdash; a 2D position of the node,
* `label` &mdash; node label.

The `layer` is an integer and for further layers is incremented.
The initial layer is layer 0.

Nodes are identified by their names, which are generated as random UUIDs.

# Contributing

When contributing ensure that your code complies with
[PEP 8](https://www.python.org/dev/peps/pep-0008/).

## Adding productions

In order to add a new production, create a file `agh_graphs/productions/<name>.py`
with a class which extends `agh_graphs.production.Production`.
Consult the docs from the module `agh_graphs.production` for details.

Each production should have tests written and added to
`tests/productions/test_<production name>.py`.

## Adding derivations

In order to add a new derivation, place your code in
`agh_graphs/derivations/<name>.py`. It should be a runnable Python module,
so ensure you have a `if __name__ == '__main__'` condition.

Tests for the new derivation should be placed in
`tests/derivations/test_<derivation name>.py`.
