from typing import List
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser, AIMessage, HumanMessage, SystemMessage
from langserve import add_routes
from langchain.schema.runnable import RunnableParallel
from langchain.schema.runnable import RunnableBranch
import sys
import uvicorn
import re
import json
import logging
from urllib.parse import urlencode
from c2c.search import Search


template = """You are a chatbot assistant who infers details about a desired mountain outing from text provided by the user.
The user will provide text describing a desired outing. Your job is to infer the following details about the outing:
- the type of activity desired. possible values are: skitouring, rock_climbing, hiking, snowshoeing, ice_climbing, mountain_climbing, via_ferrata, ice_climbing, snow_ice_mixed
- the outing area, as a geographical location 
- the desired duration of the outing, in days
- the minimum and maximum levels of difficulty desired, using the following levels: F (easy), PD (not difficult), AD (quite difficult), D (difficult), TD (very difficult), and ED (extremely difficult).
- the minimum and maximum amount of ascent desired, in meters
You will try to infer these details from the text provided by the user. As long as any detail is missing, you will ask the 
user for additional information. 
Once all details have been inferred, you will ask the user for confirmation.
Upon confirmation from the user, you will return a json object, and only that, with the following attributes:
- act: the activity
- geo: an object with 'lat' and 'long' attributes corresponding to the geographical location of the outing area
- min_duration: minimum duration in days
- max_duration: maximum duration in days
- min_rating: minimum difficulty
- max_rating: maximum difficulty
- min_ascent: minimum elevation change
- max_ascent: maximum elevation change
"""

human_template = "{text}"

result_template = """you are an assistant who directs the user to navigate to the provided url in order to see outings 
matching the search criteria the user provided previously. The user will provide the url. After providing the link,
wish the user a fruitful search, and a safe outing"""
url_template = "{url}"

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template)
])
chain = prompt | ChatOpenAI()

result_prompt = ChatPromptTemplate.from_messages([
    ("system", result_template),
    ("human", url_template)
])
result_chain = result_prompt | ChatOpenAI()


chat = ChatOpenAI()

def is_json(message):
    #print(message)
    return message is not None and message.content[0] == '{'


messages = [
    SystemMessage(content=template)
]


if __name__ == "__main__":
    user_input = input("Describe the mountain adventure are you looking for\n>>> ")
    messages.append(HumanMessage(content=user_input))
    
    while True:
        response = chat(messages)
        # print(response)
    #    response = chain.invoke({"text": user_input})
        if is_json(response):
            # everything is inferred - json was returned
            # print(response)
            url = Search(response.content).url()
            print(url)
            response = result_chain.invoke({"url": url})
            print(response.content)
            break
        else:
            user_input = input(response.content + "\n>>> ")
            messages.append(HumanMessage(content=user_input))

# https://www.camptocamp.org/routes?bbox=704698.1100553134,5708130.511036872,824698.1100553134,5828130.511036872&act=skitouring&time=1,1&lrat=F,AD
