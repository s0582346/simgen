# Node Tools

MCP tools that create **FactorySimPy Node** instances (the active
components — Source, Machine, Sink, Splitter, Combiner) and register them in
a shared, session-scoped model. Edge tools (Buffer, Conveyor, Fleet),
`connect`, `get_model`, `validate_model`, and `run_simulation` are a later
phase and out of scope here.

All five builders are implemented in `src/simgen/tools/nodes.py`, wrapped as
MCP tools in `src/simgen/tools/registry.py`, and covered by tests in
`tests/test_tools/`.

| Tool | FactorySimPy class | Description |
|---|---|---|
| `create_source` | `Source` | Generates flow items into the model. Params: `id`, `inter_arrival_time`, `flow_item_type` (`item`/`pallet`), `item_length`, `blocking`, `out_edge_selection`, `node_setup_time`. Ends up with 0 in_edges and 1 out_edge. `inter_arrival_time` must be non-zero when `blocking=False`.  |
| `create_sink` | `Sink` | Terminal node that collects flow items. Params: `id`, `node_setup_time`. No out_edge param at all; needs ≥1 in_edge.  |
| `create_machine` | `Machine` | Processes items. Params: `id`, `work_capacity` (positive int), `processing_delay`, `blocking`, `in_edge_selection`, `out_edge_selection`, `node_setup_time`. Needs ≥1 in_edge and ≥1 out_edge. `blocking` defaults to `True`.  |
| `create_splitter` | `Splitter` | Turns one incoming item into many. Params: `id`, `mode` (`UNPACK`/`SPLIT`), `split_quantity`, `processing_delay`, `blocking`, `in_edge_selection`, `out_edge_selection`, `node_setup_time`. `split_quantity` required (positive int) when `mode="SPLIT"`, ignored for `UNPACK`. Needs ≥1 in_edge and ≥1 out_edge.  |
| `create_combiner` | `Combiner` | Packs items from several in_edges into a container (a pallet pulled from the first in_edge). Params: `id`, `target_quantity_of_each_item` (non-empty list of positive ints), `processing_delay`, `blocking`, `out_edge_selection`, `node_setup_time`. No `in_edge_selection` — draws from all in_edges by design; the first in_edge must supply `Pallet` items at run time.  |

## Conventions for every `create_*` tool

- Reject duplicate `id` (check against `model.nodes`).
- Always pass `env=model.env`; never expose `env`/`simpy` objects in tool results.
- `in_edges`/`out_edges` always start empty — wiring happens later via `connect`.
- Return a small JSON-serializable summary (`id`, `type`, echoed params).
- Validation of constant params (numbers, edge-selection strings, counts) lives
  in `src/simgen/tools/utils.py` (`require_number`) and inline in each builder.
- Delay/selection params (`inter_arrival_time`, `processing_delay`, etc.) accept
  int/float/generator/callable in FactorySimPy. **v1: constant int/float only**;
  generators/callables are a later extension.
- Note: instantiating a Node subclass immediately calls
  `env.process(self.behaviour())`. This only *schedules* the process — the
  generator body (with its in/out-edge assertions) doesn't run until
  `env.run()`, so it's safe at tool-call time before the graph is fully wired.
