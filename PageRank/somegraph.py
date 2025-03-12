from manim import *
import numpy as np

class PageRankGraph(Scene):
    def construct(self):
        # Define the graph
        # We'll create 5 nodes for a manageable but interesting demonstration
        nodes = []
        node_labels = []
        
        # Position the nodes in a pentagon shape
        radius = 2.4
        angles = np.linspace(0, 2*PI, 6)[:-1]  # 5 angles
        
        for i, angle in enumerate(angles):
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            # Create node (circle with no fill)
            node = Circle(radius=0.5, color=BLUE, fill_opacity=0)
            node.move_to([x, y, 0])
            nodes.append(node)
            
            # Create node label
            label = Text(f"{i+1}").scale(0.7).move_to(node.get_center())
            node_labels.append(label)
        
        # Original edges for the directed graph
        edges = [
            (0, 1), (0, 3), (1, 0), (1, 4), (2, 3),
            (3, 2), (3, 4), (4, 0), (4, 3)
        ]
        
        arrows = []
        # Dictionary to map edge to arrow index for later reference
        edge_to_arrow = {}
        
        for idx, (start, end) in enumerate(edges):
            # Calculate the direction vector
            start_pos = nodes[start].get_center()
            end_pos = nodes[end].get_center()
            
            # Adjust start and end positions to be on the circle boundaries
            direction = normalize(end_pos - start_pos)
            start_adjusted = start_pos + direction * 0.5  # radius of the circle
            end_adjusted = end_pos - direction * 0.5
            
            # Create the arrow
            arrow = CurvedArrow(start_adjusted, end_adjusted, angle = TAU/4, color=WHITE)
            arrows.append(arrow)
            
            # Map this edge to the arrow index
            edge_to_arrow[(start, end)] = idx
        
        # Group all graph elements together
        graph_group = VGroup(*nodes, *node_labels, *arrows)
        
        # Show nodes and labels
        self.play(
            *[Create(node) for node in nodes],
            *[Write(label) for label in node_labels]
        )

        self.wait(1)
        
        # Show arrows
        self.play(*[Create(arrow) for arrow in arrows])

        self.wait(4)
        ### This is the finish point for the production of the connected graph
        
        # Scale down the graph and move it to the top left
        target_position = UP * 2 + LEFT * 5
        self.play(
            graph_group.animate.scale(0.5).move_to(target_position)
        )
        
        self.wait(1)
        
        # Create a copy of the graph that completely overlaps the original
        graph_copy = graph_group.copy()
        # The copy is already in the same position as the original
        
        # Transform the copy to the center of the screen
        self.play(Write(graph_copy))
        
        self.wait(2)
        
        # Create adjacency matrix (transposed from original)
        n = len(nodes)
        adjacency = np.zeros((n, n))
        for start, end in edges:
            adjacency[end, start] = 1  # Transposed - now rows are arrivals, columns are departures
            
        # Create a title for the adjacency matrix
        adj_matrix_title = Text("Adjacency Matrix").scale(0.8)
        adj_matrix_title.to_edge(UP)
        
        # Create the matrix visualization with entries 0 and 1
        adj_matrix = Matrix(
            [[str(int(adjacency[i, j])) for j in range(n)] for i in range(n)],
            h_buff=1.5,
            v_buff=1.0
        )
        adj_matrix.scale(0.75)
        
        # Create row and column labels
        row_labels = VGroup(*[Text(f"{i+1}", font_size=20) for i in range(n)])
        col_labels = VGroup(*[Text(f"{i+1}", font_size=20) for i in range(n)])
        
        # Position labels
        for i, label in enumerate(row_labels):
            label.next_to(adj_matrix.get_rows()[i], LEFT, buff=0.5)
        
        for i, label in enumerate(col_labels):
            label.next_to(adj_matrix.get_columns()[i], UP, buff=0.5)
        
        # Add row and column headers (switched from original)
        row_header = Text("To", font_size=24).next_to(row_labels, LEFT, buff=0.5)
        col_header = Text("From", font_size=24).next_to(col_labels, UP, buff=0.5)
        
        # Group matrix elements
        matrix_group = VGroup(adj_matrix, row_labels, col_labels, row_header, col_header)
        matrix_group.move_to(LEFT * .2 + DOWN * .3)
        
        # Transition from graph to adjacency matrix
        self.play(
            FadeIn(adj_matrix_title),
            Transform(graph_copy, adj_matrix)
        )
        
        self.play(
            Write(row_labels),
            Write(col_labels),
            Write(row_header),
            Write(col_header)
        )
        
        self.wait(4)
        
        # Now we'll highlight matrix entries and corresponding arrows in the original graph
        # Select a few edges to demonstrate
        demo_edges = [(0, 1), (1, 0), (3, 2)]
        
        highlight_circle = None  # Initialize variable for the highlight circle
        explanation_text = None  # Initialize variable for the explanation text
        
        for i, (start, end) in enumerate(demo_edges):
            # Reset colors of all arrows first
            for arrow in arrows:
                arrow.set_color(WHITE)
            
            # Highlight the corresponding arrow in the original graph
            arrow_idx = edge_to_arrow[(start, end)]
            arrows[arrow_idx].set_color(YELLOW)
            
            # Get the position of the matrix entry in the transposed matrix
            entry_idx = end * n + start  # Transposed indices
            entry = adj_matrix.get_entries()[entry_idx]
            
            # Create new circle and text for this entry
            new_highlight_circle = Circle(radius=0.3, color=YELLOW)
            new_highlight_circle.move_to(entry.get_center())
            
            new_explanation_text = Text(
                f"Node {end+1} ← Node {start+1} = 1",
                font_size=20,
                color=YELLOW
            ).to_edge(DOWN, buff=0.5)
            
            # If this is the first demonstration, create the circle and text
            if i == 0:
                self.play(
                    Create(new_highlight_circle),
                    Write(new_explanation_text)
                )
                highlight_circle = new_highlight_circle
                explanation_text = new_explanation_text
            else:
                # Otherwise, replace the existing circle and text
                self.play(
                    ReplacementTransform(highlight_circle, new_highlight_circle),
                    ReplacementTransform(explanation_text, new_explanation_text)
                )
                highlight_circle = new_highlight_circle
                explanation_text = new_explanation_text
            
            self.wait(2)
        
        # Clean up last highlight and text
        self.play(
            FadeOut(highlight_circle),
            FadeOut(explanation_text)
        )
        
        # Add a general explanation of the adjacency matrix using LaTeX
        explanation = MathTex(
            r"\text{Adjacency Matrix } A_{ij} = \begin{cases} 1 & \text{if there is a link from node } j \text{ to node } i \\ 0 & \text{otherwise} \end{cases}"
        ).scale(0.7).move_to(DOWN * 3.3)
        
        self.play(Write(explanation))
        self.wait(2)
        
        # Transition to the transition matrix with teleport probability
        matrix_title = Text("Transition Matrix with Teleport Probability").scale(0.7)
        matrix_title.to_edge(UP)
        
        # Calculate the transition probabilities
        teleport_prob = 1/4
        n = len(nodes)
        P = np.zeros((n, n))
        
        # Fill the matrix according to the graph structure
        for i in range(n):
            outgoing_count = sum(1 for e in edges if e[0] == i)
            if outgoing_count > 0:
                standard_prob = (1 - teleport_prob) / outgoing_count
                for start, end in edges:
                    if start == i:
                        P[end, start] = standard_prob  # Column-major format for Markov matrices
            
            # Add teleport probability
            for j in range(n):
                P[j, i] += teleport_prob / n
        
        # Create the matrix visualization
        transition_matrix = Matrix(
            [[f"{P[i, j]:.2f}" for j in range(n)] for i in range(n)],
            h_buff=1.5,
            v_buff=1.0
        )
        transition_matrix.scale(0.6)
        transition_matrix.center()
        
        # Transition to the transition matrix
        self.play(
            FadeOut(adj_matrix_title),
            FadeOut(explanation),
            FadeOut(matrix_group),
            FadeIn(matrix_title),
            GrowFromPoint(transition_matrix, graph_group.get_center())
        )
        
        # Add explanation for the matrix
        explanation = Text(
            "P(j|i) = 0.75 × (1/outlinks_from_i) + 0.25 × (1/N)", 
            font_size=24
        ).to_edge(DOWN, buff=1)
        
        self.play(Write(explanation))
        
        # Wait for final view
        self.wait(2)


# Create a separate scene for explaining the PageRank computation
class PageRankComputation(Scene):
    def construct(self):
        # Create title
        title = Text("PageRank Computation", color=BLUE).scale(0.8).to_edge(UP)
        self.play(Write(title))
        
        # Explanation text
        explanation = VGroup(
            Text("PageRank models a random surfer who:"),
            Text("• Follows links with probability 0.75"),
            Text("• Randomly teleports with probability 0.25")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(explanation, run_time=2))
        
        # PageRank formula
        formula_title = Text("PageRank Formula:").scale(0.7)
        formula_title.next_to(explanation, DOWN, buff=0.8).align_to(explanation, LEFT)
        
        formula = MathTex(
            r"PR(p_i) = \frac{1-d}{N} + d \sum_{p_j \in M(p_i)} \frac{PR(p_j)}{L(p_j)}"
        ).next_to(formula_title, DOWN, buff=0.3)
        
        legend = VGroup(
            Text("Where:", font_size=24),
            Text("• PR(pi) is the PageRank of page i", font_size=24),
            Text("• d is the damping factor (0.75 in our case)", font_size=24),
            Text("• N is the total number of pages (5 in our example)", font_size=24),
            Text("• M(pi) is the set of pages that link to page i", font_size=24),
            Text("• L(pj) is the number of outbound links from page j", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7).next_to(formula, DOWN, buff=0.5)
        
        self.play(Write(formula_title))
        self.play(Write(formula))
        self.play(Write(legend, run_time=3))
        
        # Final message
        final_msg = Text(
            "The PageRank vector is the steady-state probability\nof the random surfer being at each node.",
            font_size=28
        ).next_to(legend, DOWN, buff=0.8)
        
        self.play(Write(final_msg))
        self.wait(2)
