prompts = {
    "question": """Be very brief, no unnecessary comments. Give me three short interview questions where each question starts on a new line. Follow this format:
Content of the 1st question?
Content of the 2nd question?
Content of the 3rd question?
    """,
    "evaluation": """Q: {questions[0]}
A: {responses[0]}

Q: {questions[1]}
A: {responses[1]}

Q: {questions[2]}
A: {responses[2]}

Be very brief, no unnecessary comments. Familiarise yourself with the answers to the questions. Next, score your answers from 1 to 5 for each answer to the interview question. Each score starts on a new line. Follow this format:
5
3
4""",
    "validation": """Q: {questions[0]}
A: {responses[0]}
Score: {scores[0]}

Q: {questions[1]}
A: {responses[1]}
Score: {scores[1]}

Q: {questions[2]}
A: {responses[2]}
Score: {scores[2]}
Be very brief, no unnecessary comments. Read the answers to the questions and their scores. Below, simply put your score from 1 to 5 for each answer to the interview question. Each score starts on a new line. Afterwards, write your brief overall summary. Follow this format:
5
3
4
Brief general summary"""
}

mock_response = """5
4
3
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable.
The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.
The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested.
Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.
"""