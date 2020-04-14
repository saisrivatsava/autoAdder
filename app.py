import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html

import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# app = dash.Dash(__name__)

# scores =[]
navbar = dbc.NavbarSimple(
    # children=[
    #     # dbc.NavItem(dbc.NavLink("Page 1", href="#")),
    #     dbc.DropdownMenu(
    #         children=[
    #             dbc.DropdownMenuItem("More pages", header=True),
    #             dbc.DropdownMenuItem("Page 2", href="#"),
    #             dbc.DropdownMenuItem("Page 3", href="#"),
    #         ],
    #         nav=True,
    #         in_navbar=True,
    #         label="More",
    #     ),
    # ],
    brand="AutoAdder",
    brand_href="#",
    color="dark",
    dark=True,
)

form = dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Add Player", className="mr-2"),
                dbc.Input(type="text", placeholder="Enter name", id='adding-rows-name'),
            ],
            className="mr-3",
        ),
      
        dbc.Button('Add',color="primary", id='adding-rows-button', n_clicks=0, className="mr-3"),
    ],
    inline=True,
)

app.layout = dbc.Container(
    
    html.Div([

    navbar,
    html.Br(),

    form,
    html.Br(),
    
    dash_table.DataTable(
        id='adding-rows-table',
        columns=[{
            'name': 'Player {}'.format(i),
            'id': 'column-{}'.format(i),
            'deletable': True,
            'renamable': True
        } for i in range(1, 3)],
        data=[
            {'column-{}'.format(i): (0) for i in range(0,5)}
            for j in range(1)
        ],
        editable=True,
        row_deletable=True
    ),
    html.Br(),

    dbc.Button('Add Row',color="success", id='editing-rows-button', n_clicks=0, className="mr-3"),
    html.Br(),

    # dash_table.DataTable(
    html.Br(),
    # print("++++++", scores),
    dash_table.DataTable(
        id='scores-sum-table',
        columns= [],
        data= [],
        editable=False,
        row_deletable=False
    ),

    html.Br(),

]),

className="p-5",
)


@app.callback(
    Output('adding-rows-table', 'data'),
    [Input('editing-rows-button', 'n_clicks')],
    [State('adding-rows-table', 'data'),
     State('adding-rows-table', 'columns')])
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        # print([sum([int(row.get(c['id'], 0)) for row in rows]) for c in columns])
        rows.append({c['id']: 0 for c in columns}),
        
    return rows



@app.callback(
    Output('adding-rows-table', 'columns'),
    [Input('adding-rows-button', 'n_clicks')],
    [State('adding-rows-name', 'value'),
     State('adding-rows-table', 'columns')])
def update_columns(n_clicks, value, existing_columns):
    if n_clicks > 0:
        existing_columns.append({
            'id': value, 'name': value,
            'renamable': True, 'deletable': True
        })
    return existing_columns


@app.callback(
    [Output('scores-sum-table', 'data'),Output('scores-sum-table', 'columns')],
    [Input('adding-rows-table', 'data'),
     Input('adding-rows-table', 'columns')])
def display_output(rows, columns):
    scores = [sum([int(row.get(c['id'], 0)) for row in rows]) for c in columns]

    data=[
            {col['id']: (scores[i]) for i, col in enumerate(columns)}
            # for j in range(1)
        ]
    # print("++++",data)
    # print(columns)

    return data, columns


if __name__ == '__main__':
    app.run_server(debug=True)
