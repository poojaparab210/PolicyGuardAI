
from app.services.llm_service import answer_policy_question

policy_context = """
Company Leave Policy:
- Employees receive 18 days of annual leave per year.
- Employees can take up to 8 days of paid sick leave.
- The company holiday calendar is shared at the beginning of each year.
"""

question = "How many days of paid sick leave can employees take?"

try:
    answer = answer_policy_question(question, policy_context)
    print("\nQuestion:", question)
    print("\nPolicy-grounded answer:\n")
    print(answer)
except RuntimeError as exc:
    print(f"Error: {exc}")
