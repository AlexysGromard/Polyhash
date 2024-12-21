import math
import plotly.graph_objects as go
from ...models import Vector3, DataModel
from .display import Display


class Simulation2DDisplay(Display):
    """
    A 2D animated display for visualizing the simulation turns as seen from above with ballons, coverage and targets.

    Attributes:
        balloon_positions (List[List[Vector3]]): Precomputed positions of balloons for each turn.
    """

    def __init__(self, data_model: DataModel, balloon_positions: list[list[Vector3]]):
        """
        Initializes the Simulation2DDisplay.

        Parameters:
            data_model (DataModel): The simulation data model.
            balloon_positions (List[List[Vector3]]): Precomputed positions of balloons for each turn.
        """
        super().__init__(data_model)
        self.balloon_positions = balloon_positions

    def render(self) -> None:
        """
        Renders the 2D animated simulation using Plotly.
        """
        # Extract target positions
        target_cells = [[target.x, target.y] for target in self.data_model.target_cells]
        frames = []

        # Initialize the figure
        fig = go.Figure()

        # Add targets as scatter points with persistent display
        targets_trace = go.Scatter(
            x=[target[0] for target in target_cells],
            y=[target[1] for target in target_cells],
            mode='markers',
            marker=dict(color='orange', size=10, symbol='x'),
            name='Targets',
            showlegend=True
        )
        fig.add_trace(targets_trace)

        # Balloon and coverage traces that will be updated in frames
        balloon_traces = []
        coverage_traces = []

        # Initialize balloon and coverage traces (empty to start)
        for i in range(self.data_model.num_balloons):
            balloon_trace = go.Scatter(
                x=[],
                y=[],
                mode='markers',
                marker=dict(size=12, color='red'),
                name=f'Balloon {i}'
            )
            balloon_traces.append(balloon_trace)
            fig.add_trace(balloon_trace)

            coverage_trace = go.Scatter(
                x=[],
                y=[],
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.1)',
                line=dict(color='rgba(255, 0, 0, 0)'),
                name=f'Coverage {i}',
                showlegend=False
            )
            coverage_traces.append(coverage_trace)
            fig.add_trace(coverage_trace)

        # Generate frames for each turn
        for turn in range(self.data_model.turns):
            frame_data = [targets_trace]  # Always include targets
            current_positions = self.balloon_positions[turn]

            for i, balloon in enumerate(current_positions):
                # Add balloon position
                balloon_trace = go.Scatter(
                    x=[balloon.x],
                    y=[balloon.y],
                    mode='markers',
                    marker=dict(size=12, color='red')
                )
                frame_data.append(balloon_trace)

                # Add coverage circle
                radius = self.data_model.coverage_radius
                theta = [2 * math.pi * t / 100 for t in range(100)]  # Generate 100 points
                coverage_x = [balloon.x + radius * math.cos(angle) for angle in theta]
                coverage_y = [balloon.y + radius * math.sin(angle) for angle in theta]
                coverage_trace = go.Scatter(
                    x=coverage_x,
                    y=coverage_y,
                    fill='toself',
                    fillcolor='rgba(255, 0, 0, 0.1)',
                    line=dict(color='rgba(255, 0, 0, 0)')
                )
                frame_data.append(coverage_trace)

            # Append the frame
            frames.append(go.Frame(data=frame_data, name=str(turn)))

        # Add frames to the figure
        fig.frames = frames

        # Configure layout and animation controls
        fig.update_layout(
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                buttons=[dict(
                    label="Play",
                    method="animate",
                    args=[None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]
                ),
                dict(
                    label="Pause",
                    method="animate",
                    args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]
                )]
            )],
            sliders=[dict(
                steps=[
                    dict(
                        method="animate",
                        args=[[frame.name], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                        label=f"Turn {frame.name}"
                    ) for frame in frames
                ],
                active=0
            )],
            xaxis=dict(
                range=[-0.5, self.data_model.cols - 0.5],  # Adjust range to show full grid cells
                title="X Coordinate",
                showgrid=True,
                dtick=1,  # Show grid lines for each coordinate
                scaleanchor="y"  # Locking X axis scale to Y for uniformity
            ),
            yaxis=dict(
                range=[self.data_model.rows - 0.5, -0.5],  # Invert Y to match typical grid coordinates
                title="Y Coordinate", 
                showgrid=True,
                dtick=1  # Show grid lines for each coordinate
            ),
            title="Simulation 2D Display",
            showlegend=True,
            width=800,  # Wider display
            height=800,  # Square display
            plot_bgcolor='white',  # White background
        )

        # Show the figure
        fig.show()