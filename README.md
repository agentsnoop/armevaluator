# armevaluator
Azure ARM template and policy evaluator

## Usage

### Template
from armevalutator.template import Template
t = Template(arm, "resource_group", "subscription")
t.load_template("/test/arm_template.json")
t.load_parameters("/test/arm_template.parameters.json")
t.whatif()
t.show()

### Policy
from armevalutator.policy import Policy
p = Policy(arm, "resource_group", "subscription")
p.load_policy("/test/policy.json")
p.whatif()
result = p.audit(resource)