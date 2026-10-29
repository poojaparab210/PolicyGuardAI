
from pathlib import Path

from app.services.policy_qa import (
    index_uploaded_policy,
    ask_policy_question,
)

policy_file = Path(
    "data/uploads/c35e6fed-30f9-4dcd-8e2e-6f9bb672342d.docx"
)

if not policy_file.exists():
    print("Sample DOCX policy file not found.")
else:
    policy_id = policy_file.stem

    print(f"Indexing policy: {policy_file.name}")

    chunks = index_uploaded_policy(policy_id, str(policy_file))
    print(f"Indexed {chunks} chunks.")

    question = "How many days of paid sick leave can employees take?"
    result = ask_policy_question(policy_id, question)

    print("\nQuestion:", result["question"])
    print("\nAnswer:", result["answer"])
    print("\nRetrieved sources:")

    for source in result["sources"]:
        print(
            f"- Chunk {source['chunk_index']}: "
            f"{source['text'][:250]}"
        )
