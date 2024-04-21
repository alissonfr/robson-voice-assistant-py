
def validate_token(tokens, assistant_name, actions):
    print(tokens)
    if len(tokens) < 3 or tokens[0] != assistant_name:
        return False, None, None
    action = tokens[1]
    actionObject = tokens[2]

    for planned_action in actions:
        if action == planned_action["name"] and actionObject in planned_action["objects"]:
            return True, action, actionObject
    return False, None, None