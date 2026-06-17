def zero_shot_prompt(task):
    return task

def few_shot_prompt(task):
    return f"""Example 1:
Q: What is the capital of Japan?
A: The capital of Japan is Tokyo.

Example 2:
Q: What is the boiling point of water?
A: The boiling point of water is 100°C at sea level.

Now answer this question:
Q: {task}
A:"""

def cot_prompt(task):
    return f"""{task}

Let's think step by step before giving the final answer."""


def judge_prompt(task, resp1, resp2, resp3):
    return f"""You are an expert evaluator. Here is the original task:
{task}

Here are three responses generated using different prompting techniques:

Response A (Zero-shot): {resp1}

Response B (Few-shot): {resp2}

Response C (Chain-of-Thought): {resp3}

Judge each response on relevance, factual accuracy, and completeness. 
Score each from 0 to 100, 
then decide which technique performed best and explain why in one or two sentences
Return ONLY valid JSON with these exact fields:

{{
  "zero_shot_score": integer,
  "few_shot_score": integer,
  "cot_score": integer,
  "best_technique": string,
  "reasoning": string
}}

Do not include markdown.
Do not include anything before after or outside the JSON."""