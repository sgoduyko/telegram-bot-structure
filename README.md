# Description
a little telegram-bot with understandable structure of the project.

# Interesting features
1) handler collector. It is beta version, but anyway he allows you to put handlers in more understandable way, to have good structure of your service.
2) FMS(Finite Machine State) Pipelines

# Handler collector
It is beta version of this feature and some things wasn't implemented
How to use
1) put file with handlers by location telegram_bot/bot/handlers
2) use special decorator add_handler_with_filters for registration the handler
3) add_handler_with_filters in first param takes order number by that handler will be added to application

at this moment available just MessageHandler and CallbackQueryHandler types.
when you want to recognize type of the handler you need to write specific prefix by type of the handler
| Handler    | prefix for function of handler |
| -------- | ------- |
| MessageHandler  | message_    |
| CallbackQueryHandler | callback_query_     |

When you wrote incorrect prefix you will see error message in logs about that

# FMS(Finite Machine State) Pipelines
You need to FMS Pipeline when you have a task to save intermediate results of creating entry.
How to use
1) implement enumb of state of a process. Implement must from base class FMSStateBaseEnum from bot/enums/base.py
2) implement manager of states that know what state is next and what is current state. Implement must from base class BaseFMSState from bot/modules/fms_state/base.py
3) implement pipeline where you write logic of 1) validating; 2) saving data; 3) switching state. Implement must from base class BaseFMSDataPipeline from bot/modules/fms_data_pipeline.py. Use LoggingMethodCallingOrderMixin for checking of calling requiring methods

# use .env file to run on local machine
for run from local machine to use .env file where you can set secret params and won't push them to remote repository by mistake)
1) create .env file and put there is all env variables(check docker-compose.yml file for list of the variables). File .env put on same level with bot and db directory
2) set ISRUNFROMLOCAL=1 in local environment
