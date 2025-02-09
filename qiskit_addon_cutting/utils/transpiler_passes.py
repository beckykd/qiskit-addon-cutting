# This code is a Qiskit project.

# (C) Copyright IBM 2023.

# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# Reminder: update the RST file in docs/apidocs when adding new interfaces.
"""Transpiler passes useful for circuit knitting."""

from qiskit.circuit import Reset, Qubit
from qiskit.dagcircuit import DAGOpNode
from qiskit.transpiler.basepasses import TransformationPass


class RemoveFinalReset(TransformationPass):
    """Remove reset when it is the final instruction on a qubit wire."""

    def run(self, dag):
        """Run the RemoveFinalReset pass on ``dag``.

        Args:
            dag (DAGCircuit): the DAG to be optimized.

        Returns:
            DAGCircuit: the optimized DAG.
        """
        for output_node in dag.output_map.values():
            if isinstance(output_node.wire, Qubit):
                pred = next(dag.predecessors(output_node))
                if isinstance(pred, DAGOpNode) and isinstance(pred.op, Reset):
                    dag.remove_op_node(pred)
        return dag


class ConsolidateResets(TransformationPass):
    """Consolidate a run duplicate resets in to a single reset."""

    def run(self, dag):
        """Run the ConsolidateResets pass on ``dag``.

        Args:
            dag (DAGCircuit): the DAG to be optimized.

        Returns:
            DAGCircuit: the optimized DAG.
        """
        resets = dag.op_nodes(Reset)
        for reset in resets:
            successor = next(dag.successors(reset))
            if isinstance(successor, DAGOpNode) and isinstance(successor.op, Reset):
                dag.remove_op_node(reset)
        return dag
