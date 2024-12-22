import plotly.graph_objects as go
from ...models import Vector3, DataModel
from .display import Display


class Simulation2DDisplay(Display):
    """
    A 2D animated display for visualizing the simulation turns as seen from above with balloons, coverage, and targets.

    Attributes:
        balloon_positions (List[List[Vector3]]): Precomputed positions of balloons for each turn.
    """

    def __init__(self, data_model: DataModel, balloon_positions: list[list[Vector3]], score_history: list[int]) -> None:
        """
        Initializes the Simulation2DDisplay.

        Parameters:
            data_model (DataModel): The simulation data model.
            balloon_positions (List[List[Vector3]]): Precomputed positions of balloons for each turn.
        """
        super().__init__(data_model)
        self.balloon_positions = balloon_positions
        self.score_history = score_history

    def render(self) -> None:
        """
        Renders the 2D animated simulation using Plotly.
        """
        # Extract target positions
        target_cells = [[target.x, target.y] for target in self.data_model.target_cells]
        radius = self.data_model.coverage_radius
        frames = []

        # Initialize the figure
        fig = go.Figure()

        # Add targets as scatter points with persistent display
        targets_trace = go.Scatter(
            x=[target[1] for target in target_cells],
            y=[target[0] for target in target_cells],
            mode='markers',
            marker=dict(color='orange', size=10, symbol='x'),
            name='Targets',
            showlegend=True
        )
        fig.add_trace(targets_trace)


        initial_score_annotation = go.layout.Annotation(
            text="Score: 0",
            xref="paper",
            yref="paper",
            x=0.02,
            y=0.98,
            showarrow=False,
            font=dict(size=16, color="black"),
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        )
        starting_x = self.data_model.starting_cell.x
        starting_y = self.data_model.starting_cell.y
        initial_shapes = [
            dict(
                type="circle",
                xref="x",
                yref="y",
                x0=starting_y - radius,
                y0=starting_x - radius,
                x1=starting_y + radius,
                y1=starting_x + radius,
                fillcolor=f'rgba(0, 200, 200, 0.2)',
                line=dict(color='rgba(0, 0, 255, 1)', width=2)
            ) for _ in range(self.data_model.num_balloons)
        ]

        frames.append(go.Frame(
            data=[targets_trace],
            name="0",
            layout=go.Layout(annotations=[initial_score_annotation], shapes=initial_shapes)
        ))

        # Generate frames for each turn
        for turn in range(self.data_model.turns):
            frame_data = [targets_trace]  # Always include targets 
            current_positions = self.balloon_positions[turn]
            shapes = []

            for balloon in current_positions:
                # Add coverage circle as a shape
                shapes.append(dict(
                    type="circle",
                    xref="x",
                    yref="y",
                    x0=balloon.y - radius,
                    y0=balloon.x - radius,
                    x1=balloon.y + radius,
                    y1=balloon.x + radius,
                    fillcolor=f'rgba(0, 200, 200, 0.2)',
                    line=dict(color='rgba(0, 0, 255, 1)', width=2)
                ))

            # Create annotation for the score
            score_annotation = go.layout.Annotation(
                text=f"Score: {self.score_history[turn]}",
                xref="paper",
                yref="paper",
                x=0.02,
                y=0.98,
                showarrow=False,
                font=dict(size=16, color="black"),
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            )

            # Append the frame with the updated annotation and shapes
            frames.append(go.Frame(
                data=frame_data,
                name=str(turn + 1),
                layout=go.Layout(annotations=[score_annotation], shapes=shapes)
            ))

        # Add frames to the figure
        fig.frames = frames

        # Dynamic axis scaling and tick intervals
        x_tick_interval = max(1, self.data_model.cols // 10)
        y_tick_interval = max(1, self.data_model.rows // 10)

        # Configure layout
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}]
                        ),
                        dict(
                            label="Pause",
                            method="animate",
                            args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]
                        )
                    ]
                )
            ],
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
                range=[-0.5, self.data_model.cols + 0.5],
                title="Cols",
                showgrid=True,
                dtick=x_tick_interval,
                automargin=True,
                scaleratio=1
            ),
            yaxis=dict(
                range=[-0.5, self.data_model.rows + 0.5],   
                title="Rows",
                showgrid=True,
                dtick=y_tick_interval,
                automargin=True,
                scaleratio=1
            ),
            title="Simulation 2D Display",
            showlegend=True,
            xaxis_scaleanchor="y",
            yaxis_scaleanchor="x",
        )

        # Render the figure
        fig.show()