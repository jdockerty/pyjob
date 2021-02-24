# PyJob

PyJob is an abstraction around the [Reed](https://reed.co.uk) API for job searching.

After providing an API key you can interact with the API for finding jobs that have been posted to Reed, either by companies or agencies, as well as the various other functionality that they provide.

You can:
* **Search** for jobs
* Find **details** of particular jobs using their IDs.


## TODO

* Finish **Search** class for API interaction. [WIP]
* Add CI pipeline.
* Add custom exceptions for raising errors, currently just exiting on error and printing a log message with `sys.exit`.
* Build out a **Detail** class for finding more information around a job with the ID.
* Create CLI wrapper for this API for job searches on the command line.