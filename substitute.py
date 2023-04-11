
"""
The script takes in three command line arguments: the name of the input JSON file, the depth for the substitution, 
and the name of the output file.

To run the script, you would call it from the command line like this:
python substitute.py input.json 2 output.json
"""

import json
import sys

def substitute_values(input_dict, depth=None):
    """
    Replaces values in a dictionary with a modified version of the value.

    For every key-value pair in the input, if the value is not a dictionary, the value is replaced
    with {'_content': old_value, '_type': str(type(old_value))}. If the value is a dictionary, the same
    substitution is applied recursively to that value, until the specified depth is reached.

    :param input_dict: The dictionary to modify
    :type input_dict: dict
    :param depth: The maximum depth of recursion for substituting values. If None, recurse until all
                  values have been substituted.
    :type depth: int or None
    :return: The modified dictionary
    :rtype: dict
    """
    if depth is None:
        depth = float('inf')

    if not isinstance(input_dict, dict) or depth == 0:
        return input_dict

    result_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, dict):
            result_dict[key] = substitute_values(value, depth - 1)
        else:
            result_dict[key] = {'_content': value, '_type': str(type(value))}

    return result_dict


def main():
    # parse command line arguments
    input_file = sys.argv[1]
    depth = int(sys.argv[2])
    output_file = sys.argv[3]

    # load input file
    with open(input_file, 'r') as f:
        input_dict = json.load(f)

    # modify input dictionary
    output_dict = substitute_values(input_dict, depth)

    # write output file
    with open(output_file, 'w') as f:
        json.dump(output_dict, f, indent=4)


if __name__ == '__main__':
    main()
