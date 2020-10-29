# armevaluator
Azure ARM template and policy evaluator

## Usage
from armevalutator.template import Template
t = Template(arm, "resource_group", "subscription")
t.load_template("/test/arm_template.json")
t.load_parameters("/test/arm_template.parameters.json")
t.whatif()
t.show()