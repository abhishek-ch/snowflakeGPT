import os

import openai
from langchain import OpenAI, PromptTemplate, SQLDatabase, SQLDatabaseChain
from langchain.chains import SQLDatabaseSequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import AzureOpenAI, OpenAI
from langchain.llms.openai import BaseOpenAI

from snowgpt.prompt import *

gpt_models_dict = {"gpt-35-turbo":"gpt-3.5-turbo",
                   "gpt-4_8k_ascent":"gpt-4-0314",
                   "gpt-4_32k_ascent":"gpt-4-32k-0314"}

def get_model(model_name:str) -> BaseOpenAI:
    if openai.api_type == "azure":
        return ChatOpenAI(engine=model_name, model_name=gpt_models_dict.get(model_name), temperature=0.7)
    else:
        return OpenAI(temperature=0.7)


def verify_prompt(example_input:str,model:str="gpt-35-turbo") -> None:
    llm = get_model(model)
    prompt = get_prompt_template()
    print(
        prompt.format(
            input=example_input, chat_history=None
        )
)


def execute(query: str, model:str="gpt-35-turbo") -> str:
    assert os.environ.get("SNOWFLAKE_URL") is not None,"Snowflake URL must be configured as Env variable SNOWFLAKE_URL"
    llm = get_model(model)
    snowflake_prompt_template = get_prompt_template()
    database = SQLDatabase.from_uri(os.environ.get("SNOWFLAKE_URL"),sample_rows_in_table_info=1)

    seq_chain = SQLDatabaseSequentialChain.from_llm(llm, database, verbose=True,
                                                query_prompt=snowflake_prompt_template,
                                                decider_prompt=SNOWFLAKE_DECIDER_PROMPT,
                                                return_intermediate_steps=True)

    result = seq_chain(query)
    # print(result["intermediate"])