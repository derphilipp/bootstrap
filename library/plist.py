#!/usr/bin/env python3
from ansible.module_utils.basic import *
import delegator


def _get_value(path, file):
    escaped_path = path.replace(" ", r"\ ")
    result = delegator.run('/usr/libexec/PlistBuddy -c "Print:{}" {}'.format(escaped_path, file))
    return result.return_code, result.out.rstrip(), result.err


def _set_value(path, file, value):
    escaped_path = path.replace(" ", r"\ ")
    escaped_value = value.replace(" ", r"\ ")
    result = delegator.run('/usr/libexec/PlistBuddy -c "Set:{} {}" {}'.format(escaped_path, escaped_value, file))
    return result.return_code, result.out.rstrip(), result.err


def plist_present(data):
    success_code, current_value, error_output = _get_value(data["path"], data["file"])
    if success_code == 0:
        if current_value == data["value"]:
            result = {}
            return False, False, result
        else:
            change_success, change_output, change_stderr = _set_value(data["path"], data["file"], data["value"])
            result = {"stderr": change_stderr, "set_to": data["value"], "set_from": current_value}
            return change_success != 0, True, result
    else:
        result = {"stderr": error_output}
        return True, False, result


def plist_absent(data=None):
    result = {"Error": "Not implemented yet"}
    return True, True, result


def main():
    fields = {
        "path": {"required": True, "type": "str"},
        "value": {"required": True, "type": "str"},
        "file": {"required": True, "type": "str"},
        "state": {"default": "present", "choices": ["present", "absent"], "type": "str"},
    }

    choice_map = {"present": plist_present, "absent": plist_absent}

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = choice_map.get(module.params["state"])(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error setting variable", meta=result)


if __name__ == "__main__":
    main()
