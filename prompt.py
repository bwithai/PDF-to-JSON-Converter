PROMPT_CLAUSES = '''{
    "clauses": [
        {
            "clause_no": "",
            "clause_title": "",
            "clause_date": ""
        },
        {
            "clause_no": "",
            "clause_title": "",
            "clause_date": ""
        },
        ...
    ]
}'''


PROMPT_ITEMS = """
            Summarize the text below into a JSON with exactly the following structure:
            {
                "Items": [
                    {
                        "item_no": "",
                        "supplies_or_services": "",
                        "quantity": "",
                        "unit": "",
                        "unit_price": "",
                        "amount": "",
                        "clauses": []
                    },
                    {
                        "item": "",
                        "supplies_or_services": "",
                        "quantity": "",
                        "unit": "",
                        "unit_price": "",
                        "amount": "",
                        "clauses": []
                    },
                    ...
                ]
            }
        """