from Module import version

# khbr uses unsafe yaml loading which triggers a warning that clutters up production log files
if not version.debug_mode():
    import yaml
    yaml.warnings({"YAMLLoadWarning": False})
