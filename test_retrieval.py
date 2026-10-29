
from app.services.retrieval import index_policy, search_policy

sample_policy = """
Annual Leave: Eligible employees receive 18 days of annual leave
per calendar year. Requests should be submitted five working days
before the planned leave whenever possible.

Sick Leave: Employees may take up to 8 days of paid sick leave
per calendar year.

Public Holidays: The company publishes its holiday calendar
at the beginning of each year.
"""

policy_id = "sample_leave_policy"

count = index_policy(policy_id, sample_policy)
print(f"Indexed {count} chunks.")

results = search_policy(
    policy_id,
    "How many days of paid sick leave are available?",
)

print("\nRetrieved passages:")
for result in results:
    print(result["text"])
    print("Distance:", result["distance"])
    print("---")
