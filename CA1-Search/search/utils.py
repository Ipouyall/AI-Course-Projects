import os
from pandas import DataFrame, concat, options, ExcelWriter
from IPython.display import display, HTML

from .types import State, Graph


def find_files_with_extension(directory, extension):
    """find files with extension in directory"""
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(extension)]


def create_df():
    """create dataframe from result"""
    df = DataFrame(columns=['visited_states', 'result_time', 'algorithm_time', 'path'])
    return df


def add_to_df(df: DataFrame, state: State, visited_states: int, path: tuple, time):
    """add to dataframe"""
    df.loc[len(df)] = [visited_states, state.time, time, path]
    return df


def convert_to_world_df(save_to=None, names=None, **dataframes):
    """generate dataframe based on worlds from algorithm based dataframes"""
    options.mode.chained_assignment = None
    columns = list(dataframes.values())[0].columns
    df_columns = ['algorithm name'] + list(columns)
    world_dataframes = []

    for i in range(len(dataframes[list(dataframes.keys())[0]])):
        world_dataframes.append(DataFrame(columns=df_columns))
        for algorithm_name, dataframe in dataframes.items():
            row = dataframe.iloc[i]
            row['algorithm name'] = algorithm_name
            world_dataframes[i] = concat([world_dataframes[i], row.to_frame().T], ignore_index=True)
    if save_to is not None:
        with ExcelWriter(save_to) as writer:
            if names is None:
                for i, dataframe in enumerate(world_dataframes, start=1):
                    dataframe.to_excel(writer, sheet_name=f'testcase{i}', index=False)
            else:
                for name, dataframe in zip(names, world_dataframes):
                    dataframe.to_excel(writer, sheet_name=name, index=False)
    return world_dataframes


def display_df_as_html(*df):
    """display dataframe as html"""
    for dataframe in df:
        display(HTML(dataframe.to_html(index=False)))


def prepare_graph(graph: Graph):
    """prepare graph"""
    return {
        "start_state": graph.get_start_state(),
        "goal_test": graph.generate_goal_tester(),
        "transition_function": graph.get_transition_function(),
    }
