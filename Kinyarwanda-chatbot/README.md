**Mbaza chatbot Rasa Language Model Kinyarwanda**

This is a Kinyarwanda Rasa based chatbot that can have text as input. It includes pre-built intents, actions, and stories for handling conversation flows of interest regarding Covid-19.

**Install dependencies**

Run:

`pip install -r requirements.txt`

To install development dependencies:

`python -m spacy download xx_ent_wiki_sm`

**Run the bot**

Use `rasa train` to train a model.

To run, first set up your action server in another terminal window.

To talk to the bot, run:

`rasa shell`

If you want to understand how the bot is working under the hood; run:

`rasa shell --debug`

Note that `--debug` mode will produce a lot of output. To simply talk to the bot, you can remove this flag.

**Overview of the files**

`data/nlu.yml` - contains NLU training data

`data/rules.yml` - contains rules training data

`data/stories.yml` - contains stories training data

`actions.py` - contains custom action/api code

`domain.yml` - the domain file, including bot response templates

`config.yml` - training configurations for the NLU pipeline and policy ensemble

`tests/tests_stories` - end-to-end tests

**Things you can ask the bot**

The bot currently has 4 skills. You can ask about:
1. Vaccination
2. testing procedures
3. testing centers in Kigali
4. testing validity  


