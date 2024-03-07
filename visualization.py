import plotly.express as px
graph_dict = {
    'autoregressive.py': ['__call__', 'one_step_prediction', 'loss', 'one_step_loss', '_get_flat_arrays_and_single_timestep_treedef', 'Predictor', '__init__', '_get_and_validate_constant_inputs', '_validate_targets_and_forcings'],
    '_get_flat_arrays_and_single_timestep_treedef': ['autoregressive.py', '__call__', 'loss'],
    '__init__': ['autoregressive.py', '__call__', 'loss', 'one_step_prediction', 'one_step_loss', 'Predictor', '_get_and_validate_constant_inputs', '_validate_targets_and_forcings']
}
# print(graph_dict.values())
parent = []
children = []
for key, value in graph_dict.items():
    parent_key = (" " + key) * len(value)
    parent.append(parent_key)
    children.extend(value)
print(parent)
print(children)
    # print("Key:", key, "Value:", value)


fig = px.treemap(
    names=['autoregressive.py', 'one_step_prediction', 'loss', 'one_step_loss', '_get_flat_arrays_and_single_timestep_treedef', 'Predictor', '__init__', '_get_and_validate_constant_inputs', '_validate_targets_and_forcings'],
    parents=["", 'autoregressive.py', 'autoregressive.py', 'autoregressive.py', 'autoregressive.py', 'autoregressive.py', 'autoregressive.py', 'autoregressive.py', 'autoregressive.py']
)
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
# fig.show()



fig = px.treemap(
    names = ["autoregressive.py","__call__", "one_step_prediction", "loss", "one_step_loss", "_get_flat_arrays_and_single_timestep_treedef", "Predictor", "__init__", 
             "_get_and_validate_constant_inputs", '_get_flat_arrays_and_single_timestep_treedef', 'Predictor', '__call__'],

    parents = ['', "autoregressive.py", "autoregressive.py", "autoregressive.py", "autoregressive.py", "autoregressive.py", "autoregressive.py", "autoregressive.py", 
               "autoregressive.py", '', '_get_flat_arrays_and_single_timestep_treedef',  '_get_flat_arrays_and_single_timestep_treedef']
)
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
# fig.show()


fig = px.treemap(
    names = ["Eve","Cain", "Luke","Seth", "Enos", 'Mark', 'Jonah', "Noam", "Abel", "Awan", "Enoch", "Azura", 'John', 'Matthew', 'John', 'Enoch'],
    parents = ["", "Eve", "Cain","Eve", "Seth", 'Seth' , "Enos","Seth", "Eve", "Eve", "Awan", "Eve", 'Azura', 'Azura', 'Mark', 'Mark', 'Abel']
)
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
# fig.show()
