#!/usr/bin/env python

from distutils.core import setup

setup(name='GenAiChatbot',
      version='1.0',
      description='Example of a ChatBot using OpenAi',
      author='kperun',
      url='https://github.com/kperun/genAiChatbot',
      install_requires=['openai','python-dotenv',
                        'llama-index',# RAG
                        'pypdf',# pdf management
                        'sentence_transformers' # embeds pdfs into vectors
                        ],
     )