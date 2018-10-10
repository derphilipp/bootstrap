# coding=utf8
from ansible.module_utils.basic import *
import delegator
import re

REGEX = r"^  Package \"(.*)\":$"


def _install(name):
    return delegator.run("pipsi install {}".format(name))


def _list():
    elements = []
    result = delegator.run("pipsi list")
    matches = re.finditer(REGEX, result.out, re.MULTILINE)
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            elements.append(match.group(groupNum))
    return elements


def _is_installed(name):
    all_elements = _list()
    return name in all_elements


def pipsi_present(data):
    is_installed = _is_installed(data["name"])
    if not is_installed:
        call_result = _install(data["name"])
        installation_result = call_result.return_code == 0
        return installation_result, True, {
            "stdout": call_result.out,
            "stderr": call_result.err
        }
    else:
        return False, False, {}


def pipsi_absent(data=None):
    result = {"Error": "Not implemented yet"}
    return True, True, result


def main():
    fields = {
        "name": {
            "required": True,
            "type": "str"
        },
        "state": {
            "default": "present",
            "choices": ["present", "absent"],
            "type": "str"
        },
    }

    choice_map = {"present": pipsi_present, "absent": pipsi_absent}

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = choice_map.get(module.params["state"])(
        module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error setting variable", meta=result)


if __name__ == "__main__":
    main()
