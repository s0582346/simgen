"""Central registration of MCP tools onto a FastMCP server.

Each tool here is a thin wrapper that delegates to
a plain builder in `simgen.tools.nodes` (which owns validation and the shared
model). As new node tools land, register them in `register_tools`.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from simgen.tools import nodes


def register_tools(mcp: FastMCP) -> FastMCP:
    """Register every block-building tool on `mcp` and return it."""

    @mcp.tool()
    def create_source(
        id: str,
        inter_arrival_time: float = 1.0,
        flow_item_type: str = "item",
        item_length: float = 1,
        blocking: bool = False,
        out_edge_selection: str = "FIRST_AVAILABLE",
        node_setup_time: float = 0,
    ) -> dict:
        """Create a Source node that generates flow items into the model.

        A Source has no in_edges and exactly one out_edge (wired later via
        connect).

        Args:
            id: unique node identifier.
            inter_arrival_time: constant time between item generations; must be
                non-zero when blocking is False.
            flow_item_type: "item" or "pallet".
            item_length: physical length assigned to each generated item;
                only used by conveyor edges (travel time = length/speed) and
                ignored by plain buffers.
            blocking: if True, wait for out_edge space; if False, discard when
                full.
            out_edge_selection: edge-selection strategy, one of
                "FIRST_AVAILABLE", "RANDOM", "ROUND_ROBIN".
            node_setup_time: constant initial setup delay.
        """
        return nodes.create_source(
            id=id,
            inter_arrival_time=inter_arrival_time,
            flow_item_type=flow_item_type,
            item_length=item_length,
            blocking=blocking,
            out_edge_selection=out_edge_selection,
            node_setup_time=node_setup_time,
        )

    @mcp.tool()
    def create_sink(
        id: str,
        node_setup_time: float = 0,
    ) -> dict:
        """Create a Sink node that collects flow items at the end of the line.

        A Sink is terminal: it has no out_edge and needs at least one in_edge
        (wired later via connect).

        Args:
            id: unique node identifier.
            node_setup_time: constant initial setup delay.
        """
        return nodes.create_sink(
            id=id,
            node_setup_time=node_setup_time,
        )

    @mcp.tool()
    def create_machine(
        id: str,
        work_capacity: int = 1,
        processing_delay: float = 0,
        blocking: bool = True,
        in_edge_selection: str = "FIRST_AVAILABLE",
        out_edge_selection: str = "FIRST_AVAILABLE",
        node_setup_time: float = 0,
    ) -> dict:
        """Create a Machine node that processes flow items.

        A Machine needs at least one in_edge and one out_edge (both wired later
        via connect).

        Args:
            id: unique node identifier.
            work_capacity: number of items processed simultaneously (one worker
                thread per item); must be a positive int.
            processing_delay: constant time to process one item.
            blocking: if True, wait for out_edge space; if False, discard when
                full.
            in_edge_selection: in-edge selection strategy, one of
                "FIRST_AVAILABLE", "RANDOM", "ROUND_ROBIN".
            out_edge_selection: out-edge selection strategy, one of
                "FIRST_AVAILABLE", "RANDOM", "ROUND_ROBIN".
            node_setup_time: constant initial setup delay.
        """
        return nodes.create_machine(
            id=id,
            work_capacity=work_capacity,
            processing_delay=processing_delay,
            blocking=blocking,
            in_edge_selection=in_edge_selection,
            out_edge_selection=out_edge_selection,
            node_setup_time=node_setup_time,
        )

    @mcp.tool()
    def create_splitter(
        id: str,
        mode: str = "UNPACK",
        split_quantity: int | None = None,
        processing_delay: float = 0,
        blocking: bool = True,
        in_edge_selection: str = "FIRST_AVAILABLE",
        out_edge_selection: str = "FIRST_AVAILABLE",
        node_setup_time: float = 0,
    ) -> dict:
        """Create a Splitter node that emits several items from one incoming item.

        A Splitter needs at least one in_edge and one out_edge (both wired later
        via connect).

        Args:
            id: unique node identifier.
            mode: "UNPACK" (emit each item inside a packed item, then the empty
                container) or "SPLIT" (split into `split_quantity` items).
            split_quantity: number of items to split into; required when
                mode="SPLIT", ignored when mode="UNPACK". Must be a positive int.
            processing_delay: constant time to process one item.
            blocking: if True, wait for out_edge space; if False, discard when
                full.
            in_edge_selection: in-edge selection strategy, one of
                "FIRST_AVAILABLE", "RANDOM", "ROUND_ROBIN".
            out_edge_selection: out-edge selection strategy, one of
                "FIRST_AVAILABLE", "RANDOM", "ROUND_ROBIN".
            node_setup_time: constant initial setup delay.
        """
        return nodes.create_splitter(
            id=id,
            mode=mode,
            split_quantity=split_quantity,
            processing_delay=processing_delay,
            blocking=blocking,
            in_edge_selection=in_edge_selection,
            out_edge_selection=out_edge_selection,
            node_setup_time=node_setup_time,
        )

    @mcp.tool()
    def create_combiner(
        id: str,
        target_quantity_of_each_item: list[int] | None = None,
        processing_delay: float = 0,
        blocking: bool = True,
        out_edge_selection: str = "FIRST_AVAILABLE",
        node_setup_time: float = 0,
    ) -> dict:
        """Create a Combiner node that packs items from several in_edges into one.

        A Combiner pulls a container (pallet) from its first in_edge, packs
        items from the other in_edges into it, and emits the packed container.
        It needs at least one in_edge and one out_edge (wired later via
        connect) and has no in_edge_selection.

        Args:
            id: unique node identifier.
            target_quantity_of_each_item: per-in_edge counts — how many items to
                pull from each in_edge per combine cycle (indexed by in_edge
                position; the first position is the pallet edge). Each entry must
                be a positive int. Defaults to [1].
            processing_delay: constant time to process one combine cycle.
            blocking: if True, wait for out_edge space; if False, discard when
                full.
            out_edge_selection: out-edge selection strategy, one of
                "FIRST_AVAILABLE", "RANDOM", "ROUND_ROBIN".
            node_setup_time: constant initial setup delay.
        """
        return nodes.create_combiner(
            id=id,
            target_quantity_of_each_item=target_quantity_of_each_item,
            processing_delay=processing_delay,
            blocking=blocking,
            out_edge_selection=out_edge_selection,
            node_setup_time=node_setup_time,
        )

    return mcp
