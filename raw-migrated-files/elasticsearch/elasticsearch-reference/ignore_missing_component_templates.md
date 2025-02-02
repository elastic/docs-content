# Config ignore_missing_component_templates [ignore_missing_component_templates]

The configuration option `ignore_missing_component_templates` can be used when an index template references a component template that might not exist. Every time a data stream is created based on the index template, the existence of the component template will be checked. If it exists, it will used to form the index’s composite settings. If it does not exist, it is ignored.


