from typing import List
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
from testrail import APIClient  # Assuming you've named your TestRail API module "testrail"

class TestRailReader(BaseReader):
    def __init__(self, testrail_url: str, testrail_user: str, testrail_password: str) -> None:
        """Initialize TestRail reader."""
        self.client = APIClient(testrail_url)
        self.client.user = testrail_user
        self.client.password = testrail_password

    def load_data(self, project_id: str) -> List[Document]:
        """Load data from the workspace.

        Args:
            project_id (str): Project ID.
        Returns:
            List[Document]: List of documents.
        """
        results = []
        offset = 0
        limit = 250
        finished = False

        while not finished:
            try:
                response = self.client.send_get(f"get_cases/{project_id}&offset={offset}&limit={limit}")
                cases = response['cases']  # Corrected here. Get the actual test cases from the response

                if not cases:
                    finished = True
                else:
                    offset += limit

                for case in cases:
                    try:
                        case_title = case["title"] if case["title"] else ''

                        extra_info = {
                            "case_id": case["id"] if case["id"] else '',
                            "priority_id": case["priority_id"] if case["priority_id"] else '',
                            "custom_preconds": case["custom_preconds"] if case["custom_preconds"] else '',
                            "custom_steps": case["custom_steps"] if case["custom_steps"] else '',
                            "custom_expected": case["custom_expected"] if case["custom_expected"] else '',
                        }

                        results.append(Document(case_title + " ", extra_info=extra_info))
                    except Exception as e:
                        print(f"Failed to process case: {e}")

            except Exception as e:
                print(f"Failed to get cases from TestRail: {e}")
                finished = True
                
        print(f"Number of test cases fetched: {len(results)}")
        return results


# Your TestRail details
testrail_url = 'https://honeycomblabs.testrail.io'
testrail_user = 'workerbee@honeycomb-labs.com'
testrail_password = '>qWA4QVsC'

# The ID of the project you want to read data from
project_id = '2'

# Create an instance of TestRailReader
reader = TestRailReader(testrail_url, testrail_user, testrail_password)

# Use the reader to load data from your project
documents = reader.load_data(project_id)

# Now, 'documents' is a list of Document objects containing your TestRail data.
for doc in documents:
    print(doc.text)
    print(doc.extra_info)
